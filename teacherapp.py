from flask import Flask, render_template, request, redirect
import sqlite3 as lite
app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('login.html')

@app.route('/login', methods = ['POST'])
def login():
    return redirect('/dashboard')



if __name__ == '__main__':
    app.run(debug = True)
