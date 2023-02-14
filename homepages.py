from newapp import app
from flask import Flask, redirect, render_template, request, url_for, render_template_string




# The Home page is accessible to anyone
@app.route('/')
def home():
    return render_template('home.html')

if __name__=='__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)
