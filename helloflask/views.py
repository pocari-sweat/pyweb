from flask import render_template, request, Response
from datetime import datetime, date
from sqlalchemy.exc import SQLAlchemyError
from helloflask import app
from helloflask.classes import FormInput
from helloflask.init_db import db_session
from helloflask.models import User

@app.route('/')
def idx():
    try:
        u = User('abc@efg.com', 'hong')
        db_session.add(u)
        db_session.commit()

        ret = "aaa"
        ret = User.query.all()
        
    except SQLAlchemyError as sqlerr:
        db_session.rollback()
        print("SqlError>>", sqlerr)

    except:
        print("Error!!")

    # return "RET=" + str(ret)
    return render_template('main.html', userlist=ret)
