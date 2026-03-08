import json


BASE_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Content-Type': 'application/json',
}


def json_response(body, status_code=200, extra_headers=None):
    headers = dict(BASE_HEADERS)
    if extra_headers:
        headers.update(extra_headers)
    return {
        'statusCode': status_code,
        'headers': headers,
        'body': json.dumps(body) if body is not None else '',
    }


def preflight_response(methods='GET, POST, OPTIONS'):
    return json_response(
        '',
        200,
        {'Access-Control-Allow-Methods': methods},
    )
