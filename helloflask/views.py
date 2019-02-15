from flask import render_template, request, Response
from datetime import datetime, date
from helloflask import app
from helloflask.classes import FormInput

@app.route('/')
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


@app.route('/top100')
def top100():
    return render_template('application.html', title="MAIN!!")


@app.route('/main')
def main():
    return render_template('main.html', title="MAIN!!")
