import requests
from werkzeug.wrappers import Request, Response


@Request.application
def application(request):
    if request.host.startswith('localhost'):
        return _proxy(request)
    return Response('Hello, i am superhero!')


def _proxy(request):
    resp = requests.request(
        method=request.method,
        url=request.url.replace(
            'localhost:8000',
            'localhost:8001'),
        headers={key: value for (key, value) in request.headers
                 if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)

    excluded_headers = [
        'content-encoding',
        'content-length',
        'transfer-encoding',
        'connection'
    ]
    headers = filter(lambda i: i[0].lower() not in excluded_headers, 
                     resp.raw.headers.items())

    response = Response(resp.content, resp.status_code, headers)
    return response
