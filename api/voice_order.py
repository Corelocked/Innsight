from .backend import handle_user_input
from .response_utils import json_response, preflight_response


def handler(request):
    """Vercel serverless handler for voice order endpoint."""
    if request.method == 'OPTIONS':
        return preflight_response('POST, OPTIONS')

    if request.method != 'POST':
        return json_response({'error': 'Method not allowed'}, 405)

    try:
        data = request.get_json(silent=True) or {}
    except Exception:
        return json_response({'error': 'Invalid JSON payload'}, 400)

    user_input = data.get('input', '').strip()
    if not user_input:
        return json_response({'error': 'No input provided'}, 400)

    if len(user_input) > 1000:
        return json_response({'error': 'Input too long (max 1000 characters)'}, 400)

    try:
        response = handle_user_input(user_input)
        return json_response({'response': response}, 200)
    except Exception as e:
        print(f"Error in voice_order handler: {e}")
        return json_response({'error': 'Internal server error'}, 500)
