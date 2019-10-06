def application(environ, start_response):
    if environ.get('PATH_INFO') == '/':
        status = '200 OK'
        content = '<h1 align="center">python kfu project</h1>'
    else:
        status = '404 NOT FOUND'
        content = 'Page not found.'
    response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(content)))]
    start_response(status, response_headers)
    yield content.encode('utf8')
