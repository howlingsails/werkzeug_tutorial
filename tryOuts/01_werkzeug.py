#!/usr/bin/env python

# # base wsgi app
# def application(env, start_res):
#     start_res('200 OK', [('Content-Type', 'text/html')])
#     return [b'Hello World!']

# # with werkzeug
from werkzeug.wrappers import Response

# def application(env, start_res):
#     response = Response("Hello World  !", mimetype='text/plain')
#     return response(env, start_res)

# expanded version (closer look at URL)
def application(env, start_res):
    request = Request(env)
    text = 'Hello %s!' % request.args.get('name', 'World')
    response = Response(text, mimetype='text/plain')
    return response(env, start_res)
    

