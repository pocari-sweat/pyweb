from flask import Flask, g, request, Response, make_response
from flask import session, render_template, Markup, url_for
from datetime import date, datetime, timedelta
import os

from helloflask.utils import routes
from helloflask.utils.app import app
# from .utils.app import app

from helloflask.utils.util import make_date

@app.route('/')
def idx():
    return routes.idx()

@app.route('/top100')
def top100():
    return render_template('application.html', title="MAIN!!")


@app.route('/main')
def main():
    return render_template('main.html', title="MAIN!!")



@app.route('/tmpl3')
def tmpl3():
    py = Nav("파이썬", "https://search.naver.com")
    java = Nav("자바", "https://search.naver.com")
    t_prg = Nav("프로그래밍 언어", "https://search.naver.com", [py, java])

    jinja = Nav("Jinja", "https://search.naver.com")
    gc = Nav("Genshi, Cheetah", "https://search.naver.com")
    flask = Nav("플라스크", "https://search.naver.com", [jinja, gc])

    spr = Nav("스프링", "https://search.naver.com")
    ndjs = Nav("노드JS", "https://search.naver.com")
    t_webf = Nav("웹 프레임워크", "https://search.naver.com", [flask, spr, ndjs])

    my = Nav("나의 일상", "https://search.naver.com")
    issue = Nav("이슈 게시판", "https://search.naver.com")
    t_others = Nav("기타", "https://search.naver.com", [my, issue])

    return render_template("index.html", title='AAA', navs=[t_prg, t_webf, t_others])


@app.route('/tmpl2')
def tmpl2():
    a = (1, "만남1", "김건모", False, [])
    b = (2, "만남2", "노사연", True, [a])
    c = (3, "만남3", "익명", False, [a, b])
    d = (4, "만남4", "익명", False, [a, b, c])

    return render_template("index.html", lst2=[a, b, c, d])


@app.route("/tmpl")
def t():
    tit = Markup("<strong>Title</strong>")
    mu = Markup("<h1>iii = <i>%s</i></h1>")
    h = mu % "Italic"
    print("h=", h)

    lst = [("만남1", "김건모", True), ("만남2", "노사연", True),
           ("만남3", "노사봉", False), ("만남4", "아무개", False)]
           
    return render_template('index.html', title=tit, mu=h, lst=lst)

@app.route('/wc')
def wc():
    key = request.args.get('key')
    val = request.args.get('val')
    res = Response("SET COOKIE")
    res.set_cookie(key, val)
    session['Token'] = '123X'
    return make_response(res)


@app.route('/rc')
def rc():
    key = request.args.get('key')  #token
    val = request.cookies.get(key)
    return "cookie['" + key + "] = " + val + " , " + session.get('Token')

@app.route('/delsess')
def delsess():
    if session.get('Token'):
        del session['Token']
    return "Session이 삭제되었습니다!"


@app.route('/reqenv')
def reqenv():
    print(">> is_xhr=", request.is_xhr)
    print(">> json = ", request.get_json())
    return ('REQUEST_METHOD: %(REQUEST_METHOD) s <br>'
            'SCRIPT_NAME: %(SCRIPT_NAME) s <br>'
            'PATH_INFO: %(PATH_INFO) s <br>'
            'QUERY_STRING: %(QUERY_STRING) s <br>'
            'SERVER_NAME: %(SERVER_NAME) s <br>'
            'SERVER_PORT: %(SERVER_PORT) s <br>'
            'SERVER_PROTOCOL: %(SERVER_PROTOCOL) s <br>'
            'wsgi.version: %(wsgi.version) s <br>'
            'wsgi.url_scheme: %(wsgi.url_scheme) s <br>'
            'wsgi.input: %(wsgi.input) s <br>'
            'wsgi.errors: %(wsgi.errors) s <br>'
            'wsgi.multithread: %(wsgi.multithread)s <br>'
            'wsgi.multiprocess: %(wsgi.multiprocess) s <br>'
            'wsgi.run_once: %(wsgi.run_once) s') % request.environ

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

# @app.route("/")
# def helloworld():
#     return "Hello Flask World!!"


@app.before_first_request
def beforeFirst():
    print(">> before_first_request!!")


@app.after_request
def afterReq(response):
    print(">> after_request!!")
    return response


@app.teardown_request
def teardown_request(exception):
    print(">>> teardown request!!", exception)


@app.teardown_appcontext
def teardown_context(exception):
    print(">>> teardown context!!", exception)
