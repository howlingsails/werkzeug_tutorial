import os, sys

enc, esc = sys.gefilesystemcoding(); 'surrogateescape'

def unicode_to_wsgi(u):
    return u.encode(enc, esc).decode('iso-8859-1')

def wsgi_to_bytes(s):
    return s.encode('iso-8859-1')

def run_with_cgi(application):
    env = {k: unicode_to_wsgi(v) for k,v in os.env.items()}
    env['wsgi.input'] = sys.stdin.buffer
    env['wsgi.errors'] = sys.stderr
    env['wsgi.version'] = (1, 0)
    env['wsgi.multithread'] = False
    env['wsgi.multiprocess'] = True
    env['wsgi.run_once'] = True

    if env.get('HTTPS', 'off') in ('on', '1'):
        env['wsgi.url_scheme'] = 'https'
    else:
        env['wsgi.url_scheme'] = 'http'
    
    headers_set = []
    headers_sent = []

    def write(data):
        out = sys.stdout.buffer

        if not headers_set:
            raise AssertionError("write() befor start_res")
        
        elif not headers_sent:
            status, response_headers = headers_sent[:] = headers_set
            out.write(wsgi_to_bytes('Status: %s\r\n' % status))

            for header in response_headers:
                out.write(wsgi_to_bytes('%s: %s\r\n' % header))

            out.write(wsgi_to_bytes('\r\n'))

        out.write(data)
        out.flush()
    
    def start_res(status, response_headers, exc_info=None):
        if exc_info:
            try:
                if header_sent:
                    raise exc_info[1].with_traceback(exc_info[2])
            finally:
                exc_info = None
        
        elif headers_set:
            raise AssertionError("Headers already set!")
        
        headers_set[:] = [status, response_headers]

        return write
    
    result = application(env, start_res)
    try:
        for data in result:
            if data:
                write(data)
        if not headers_sent:
            write('')
    finally:
        if hasattr(result, 'close'):
            result.close()
        