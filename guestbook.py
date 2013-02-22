#!/usr/bin/env python
from datetime import datetime

from flask import Flask, request, redirect, render_template, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form, TextField, TextAreaField, validators

app = Flask(__name__)
app.config.from_pyfile('settings.py')
db = SQLAlchemy(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(80))
    author = db.Column(db.String(80))
    contents = db.Column(db.Text)
    date = db.Column(db.DateTime)

    def __init__(self, subject, author, contents):
        self.subject = subject
        self.author = author
        self.contents = contents
        self.date = datetime.now()

    def __repr__(self):
        return '<Message %r>' % self.subject


class PostForm(Form):
    subject = TextField(u'Subject', validators=[
        validators.Required(),
        validators.Length(max=80)])
    author = TextField(u'Your Name', validators=[
        validators.Required(),
        validators.Length(max=80)])
    content = TextAreaField(u'Content', validators=[validators.Required()])


@app.route('/')
def guestbook():
    post_url = url_for('post')
    messages = Message.query.all()
    return render_template('guestbook.html',
                           post_url=post_url,
                           messages=messages)


@app.route('/post', methods=['GET', 'POST'])
def post():
    form = PostForm(request.form)
    if request.method == 'POST' and form.validate():
        message = Message(form.subject.data, form.author.data,
                          form.content.data)
        db.session.add(message)
        db.session.commit()
        return redirect(url_for('guestbook'))
    action_url = url_for('post')
    return render_template('post.html', action_url=action_url, form=form)


if __name__ == '__main__':
    app.run()
