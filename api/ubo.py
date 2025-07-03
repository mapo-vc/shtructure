import json, traceback
from handelsregister import main as hr_main

def handler(request, context):
    try:
        body = json.loads(request.body or "{}")
        name = body.get("name","").strip()
        if not name:
            return {
                "statusCode": 400,
                "body": json.dumps({"error":"Kein Name angegeben"}),
                "headers":{"Content-Type":"application/json"},
            }
        # Call the CLI
        result = hr_main(["-s", name, "-so", "all", "-f"])
        # Normalize to dict
        data = json.loads(result) if isinstance(result, str) else result
        return {
            "statusCode": 200,
            "body": json.dumps(data, ensure_ascii=False),
            "headers":{"Content-Type":"application/json"},
        }
    except Exception as e:
        tb = traceback.format_exc()
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e),
                "traceback": tb
            }),
            "headers":{"Content-Type":"application/json"},
        }
