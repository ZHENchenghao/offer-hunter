import sys, os, asyncio

# Add paths
sys.path.insert(0, '/home/zelond123/.local/lib/python3.13/site-packages')
sys.path.insert(0, '/home/zelond123/offer-hunter')
os.chdir('/home/zelond123/offer-hunter')

from app import app as fastapi_app
from starlette.testclient import TestClient
from starlette.types import ASGIApp, Scope, Receive, Send

# Convert FastAPI/ASGI to WSGI using Starlette's TestClient
class ASGIToWSGI:
    def __init__(self, asgi_app):
        self.client = TestClient(asgi_app, raise_server_exceptions=False)
    
    def __call__(self, environ, start_response):
        headers = {}
        # Extract headers from environ
        for key, value in environ.items():
            if key.startswith('HTTP_'):
                headers[key[5:].replace('_', '-').title()] = value
            elif key in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
                hname = key.replace('_', '-').title()
                headers[hname] = value
        
        # Build URL
        scheme = environ.get('wsgi.url_scheme', 'http')
        host = environ.get('HTTP_HOST', 'localhost')
        path = environ.get('PATH_INFO', '/')
        qs = environ.get('QUERY_STRING', '')
        url = f"{scheme}://{host}{path}"
        if qs:
            url += '?' + qs
        
        method = environ.get('REQUEST_METHOD', 'GET')
        body = environ.get('wsgi.input', None)
        content = body.read(int(environ.get('CONTENT_LENGTH', 0))) if body else None
        
        try:
            response = self.client.request(
                method=method,
                url=url,
                headers=headers,
                content=content,
            )
            status_code = response.status_code
            resp_headers = [(k.encode(), v.encode()) for k, v in response.headers.items()]
            start_response(f"{status_code} {response.reason_phrase or ''}", resp_headers)
            return [response.content]
        except Exception as e:
            start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
            return [f"Internal Error: {e}".encode()]

application = ASGIToWSGI(fastapi_app)
