def handler(request):
    """Simple diagnostic endpoint to confirm API routing."""
    # CORS preflight
    if request.method == 'OPTIONS':
        return ('', 200, {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
        })

    return ({'status': 'ok', 'message': 'health check'}, 200, {'Access-Control-Allow-Origin': '*'})
