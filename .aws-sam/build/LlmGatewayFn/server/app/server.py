import os, json, time, hashlib
from mangum import Mangum
from fastapi import FastAPI, HTTPException
import boto3
import requests
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
dynamodb = boto3.resource('dynamodb')

REQUEST_TABLE = os.getenv("REQUEST_TABLE")
USAGE_TABLE = os.getenv("USAGE_TABLE")

# Get table references
tbl_req = dynamodb.Table(REQUEST_TABLE)
tbl_usage = dynamodb.Table(USAGE_TABLE)

def body_hash(b): return hashlib.sha256(json.dumps(b, sort_keys=True).encode()).hexdigest()

def call_openai(model, msgs):
    r = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers={
            'Authorization': f'Bearer {os.getenv("OPENAI_API_KEY")}',
            'Content-Type': 'application/json',
        },
        json={
            'model': model,
            'messages': msgs,
        },
    )
    r.raise_for_status(); return r.json()

def call_bedrock(model, msgs):
    br = boto3.client('bedrock-runtime')
    # map msgs -> provider format
    paylod = {"messages": msgs, "temperature": 0.2}
    out = br.invoke_model(modelId=model, body=json.dumps(paylod).encode())
    return json.loads(out["body"].read())

@app.post("/v1/chat/completions")
def complete(req: dict):
    start = time.time()
    model = req.get("model", "gpt-4o-mini")
    messages = req["messages"]

    # simple routing example
    provider = "openai" if model.startswith("gpt") else "bedrock"

    # (optional) semantic/req cache would go here

    try:
        resp = call_openai(model, messages) if provider=="openai" else call_bedrock(model, messages)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))

    latency_ms = int((time.time()-start)*1000)
    usage = resp.get("usage", {})  # depends on provider

    rid = body_hash({"model": model, "messages": messages})
    tbl_req.put_item(Item={
        "request_id": rid,
        "ts": int(time.time()),
        "model": model,
        "provider": provider,
        "latency_ms": latency_ms,
        "messages_len": len(messages),
    })
    tbl_usage.update_item(
        Key={"date": time.strftime("%Y-%m-%d"), "model": model},
        UpdateExpression="ADD calls :c, prompt_tokens :p, completion_tokens :q",
        ExpressionAttributeValues={":c": 1, ":p": usage.get("prompt_tokens", 0), ":q": usage.get("completion_tokens", 0)},
    )
    return resp

handler = Mangum(app)