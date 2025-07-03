# api/ubo.py

import json
from handelsregister import main as hr_main

def handler(request, context):
    # Parse JSON body
    try:
        body = json.loads(request.body or "{}")
    except Exception:
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
        # Call the CLI entrypoint with: -s <search> -so all -f (JSON output)
        result = hr_main(["-s", name, "-so", "all", "-f"])
        # If hr_main prints JSON to stdout, it may return None: in that case,
        # you’d need to capture stdout instead. But ideally hr_main() returns a dict.
        if isinstance(result, str):
            data = json.loads(result)
        else:
            data = result

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
