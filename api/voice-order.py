from .backend import handle_user_input


def handler(request):
    """Vercel serverless handler for voice order endpoint."""
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return (
            '',
            200,
            {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            }
        )
    
    # Only accept POST requests
    if request.method != 'POST':
        return (
            {"error": "Method not allowed"},
            405,
            {'Access-Control-Allow-Origin': '*'}
        )
    
    try:
        data = request.get_json(silent=True) or {}
    except Exception as e:
        return (
            {"error": "Invalid JSON payload"},
            400,
            {'Access-Control-Allow-Origin': '*'}
        )
    
    user_input = data.get('input', '').strip()
    if not user_input:
        return (
            {"error": "No input provided"},
            400,
            {'Access-Control-Allow-Origin': '*'}
        )
    
    # Limit input length to prevent abuse
    if len(user_input) > 1000:
        return (
            {"error": "Input too long (max 1000 characters)"},
            400,
            {'Access-Control-Allow-Origin': '*'}
        )
    
    try:
        response = handle_user_input(user_input)
        return (
            {"response": response},
            200,
            {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'}
        )
    except Exception as e:
        print(f"Error in voice_order handler: {e}")
        return (
            {"error": "Internal server error"},
            500,
            {'Access-Control-Allow-Origin': '*'}
        )
