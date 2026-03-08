def handler(request):
    """Vercel serverless handler for feedback endpoint."""
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
    
    if request.method != 'POST':
        return (
            {"error": "Method not allowed"},
            405,
            {'Access-Control-Allow-Origin': '*'}
        )
    
    try:
        data = request.get_json(silent=True) or {}
    except Exception:
        return (
            {"error": "Invalid JSON payload"},
            400,
            {'Access-Control-Allow-Origin': '*'}
        )
    
    user_feedback = data.get('feedback', '').strip()
    if not user_feedback:
        return (
            {"error": "No feedback provided"},
            400,
            {'Access-Control-Allow-Origin': '*'}
        )
    
    # Limit feedback length
    if len(user_feedback) > 2000:
        return (
            {"error": "Feedback too long (max 2000 characters)"},
            400,
            {'Access-Control-Allow-Origin': '*'}
        )
    
    # TODO: Store feedback in database or logging service
    # For now, just acknowledge receipt
    print(f"Feedback received: {user_feedback[:100]}...")
    
    return (
        {"message": "Thank you for your feedback!"},
        200,
        {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'}
    )
