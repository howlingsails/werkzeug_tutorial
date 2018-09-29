HELLO_WORLD = b"Hello world!\n"

def simple_app(env, start_res):
    status = '200 OK'
    response_headers = [('Content-Type', 'text/plain')]
    stat_res(status, response_headers)
    return [HELLO_WORLD]

