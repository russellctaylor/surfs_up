

#import dependencies 
from flask import Flask
#Create a New Flask App Instance

app = Flask(__name__)
#Variables with underscores before and after them are called magic methods in Python.
#Create Flask Routes
#@app.route('/')
#Next, create a function called hello_world(). 
@app.route('/')
def hello_world():
    return 'Hello world'
#set FLASK_APP=app.py
if __name__ == '__main__':
    app.run()


