from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from flask import Flask  # , url_for, render_template, redirect, request
from Controllers import MainController


engine = create_engine("sqlite:///Assets/Baza.db",
                       connect_args={"check_same_thread": False})
DBSession = sessionmaker(bind=engine)
sesija = DBSession()

app = Flask(__name__, static_folder="Assets", template_folder="Views")

MainController.setup(app, sesija)  # Paljenje setaup-a iz Controllera

if __name__ == '__main__':
    app.run(debug=True)
