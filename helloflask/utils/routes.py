from flask import render_template, request, Response
from helloflask.utils.classes import FormInput, Nav
from datetime import datetime, date
def idx():
    rds = []
    for i in [1, 2, 3]:
        id = 'r' + str(i)
        name = 'radiotest'
        value = i
        checked = ''
        if i == 2:
            checked = 'checked'
        text = 'RadioTest' + str(i)
        rds.append(FormInput(id, name, value, checked, text))

    # today = date.today()
    # today = datetime.now()
    # today = datetime.strptime('2019-02-14 09:22', '%Y-%m-%d %H:%M')
    today = '2019-02-14 09:22'
    # d = datetime.strptime("2019-03-01", "%Y-%m-%d")

    # year = 2019
    year = request.args.get('year', date.today().year, int)
    return render_template('app.html', year=year, ttt='TestTTT999', radioList=rds, today=today)

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