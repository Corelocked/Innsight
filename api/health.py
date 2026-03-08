from .response_utils import json_response, preflight_response

def handler(request):
    """Simple diagnostic endpoint to confirm API routing."""
    if request.method == 'OPTIONS':
        return preflight_response('GET, POST, OPTIONS')

    return json_response({'status': 'ok', 'message': 'health check'}, 200)
