from flask import Flask, g, request, Response, make_response
from datetime import date, datetime

app = Flask(__name__)
app.debug = True


def ymd(fmt):
    def trans(date_str):
        return datetime.strptime(date_str, fmt)
    return trans


@app.route('/dt')
def dt():
    datestr = request.values.get('date', date.today(), type=ymd('%Y-%m-%d'))
    return "우리나라 시간 형식: " + str(datestr)

# app.config['SERVER_NAME'] = 'local.com:5000'

# @app.route("/sd")
# def helloworld_local():
#     return "Hello Local.com!"


# @app.route("/sd", subdomain="g")
# def helloworld22():
#     return "Hello G.Local.com!!!"

@app.route('/rp')
def rp():
    # q = request.args.get('q')
    q = request.args.getlist('q')
    return "q= %s" % str(q)

@app.route('/test_wsgi')
def wsgi_test():
    def application(environ, start_response):
        body = 'The request method was %s' % environ['REQUEST_METHOD']
        headers = [('Content-Type', 'text/plain'),
                   ('Content-Length', str(len(body)))]
        start_response('200 OK', headers)
        return [body]

    return make_response(application)

@app.route('/res1')
def res1():
    custom_res = Response("Custom Response", 201, {'test': 'ttt'})
    return make_response(custom_res)


# @app.before_request
# def before_request():
#     print("before_request!!!")
#     g.str = "한글"

@app.route("/gg")
def helloworld2():
    return "Hello World!" + getattr(g, 'str', '111')

@app.route("/")
def helloworld():
    return "Hello Flask World!!"
