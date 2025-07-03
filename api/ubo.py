import json
from handelsregister import main as hr_main

def handler(request, context):
    try:
        body = json.loads(request.body or "{}")
    except:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid JSON"}),
            "headers": {"Content-Type": "application/json"},
        }

    name = body.get("name", "").strip()
    if not name:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Kein Name angegeben"}),
            "headers": {"Content-Type": "application/json"},
        }

    try:
        result = hr_main(["-s", name, "-so", "all", "-f"])
        data = json.loads(result) if isinstance(result, str) else result
        return {
            "statusCode": 200,
            "body": json.dumps(data, ensure_ascii=False),
            "headers": {"Content-Type": "application/json"},
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {"Content-Type": "application/json"},
        }
