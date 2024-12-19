from flask import Flask,render_template
from backend.models import db
from backend.api_controllers import *
app=None
def setup_app():
    app=Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///household.sqlite"
    db.init_app(app)
    api.init_app(app)
    app.app_context().push()
    app.debug=True

setup_app()


from backend.controllers import*



if __name__=="__main__":
    app.run()