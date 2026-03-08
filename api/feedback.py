import json

def handler(request):
    """Vercel serverless handler for feedback endpoint."""
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Content-Type': 'application/json',
            },
            'body': ''
        }
    
    if request.method != 'POST':
        return {
            'statusCode': 405,
            'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
            'body': json.dumps({"error": "Method not allowed"})
        }
    
    try:
        data = request.get_json(silent=True) or {}
    except Exception:
        return {
            'statusCode': 400,
            'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
            'body': json.dumps({"error": "Invalid JSON payload"})
        }
    
    user_feedback = data.get('feedback', '').strip()
    if not user_feedback:
        return {
            'statusCode': 400,
            'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
            'body': json.dumps({"error": "No feedback provided"})
        }
    
    # Limit feedback length
    if len(user_feedback) > 2000:
        return {
            'statusCode': 400,
            'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
            'body': json.dumps({"error": "Feedback too long (max 2000 characters)"})
        }
    
    # TODO: Store feedback in database or logging service
    # For now, just acknowledge receipt
    print(f"Feedback received: {user_feedback[:100]}...")
    
    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
        'body': json.dumps({"message": "Thank you for your feedback!"})
    }
