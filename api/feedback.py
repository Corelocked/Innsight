from .response_utils import json_response, preflight_response

def handler(request):
    """Vercel serverless handler for feedback endpoint."""
    if request.method == 'OPTIONS':
        return preflight_response('POST, OPTIONS')

    if request.method != 'POST':
        return json_response({"error": "Method not allowed"}, 405)

    try:
        data = request.get_json(silent=True) or {}
    except Exception:
        return json_response({"error": "Invalid JSON payload"}, 400)

    user_feedback = data.get('feedback', '').strip()
    if not user_feedback:
        return json_response({"error": "No feedback provided"}, 400)

    if len(user_feedback) > 2000:
        return json_response({"error": "Feedback too long (max 2000 characters)"}, 400)

    print(f"Feedback received: {user_feedback[:100]}...")

    return json_response({"message": "Thank you for your feedback!"}, 200)
