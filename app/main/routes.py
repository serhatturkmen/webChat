# -*- coding: utf-8 -*-
from flask import session, redirect, url_for, render_template, request
from . import main
from .forms import LoginForm
from .events import kullanicilar

@main.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        if(form.name.data in kullanicilar):
            uyari='Kullanıcı adı mevcut. Lütfen başka bir kullanıcı adı deneyiniz.'
            return render_template('index.html', form=form,uyari=uyari)
        else:
            session['name'] = form.name.data
            session['room'] = form.room.data
            return redirect(url_for('.chat'))
    elif request.method == 'GET':
        form.name.data = session.get('name', '')
        form.room.data = session.get('room', '')
    return render_template('index.html', form=form)


@main.route('/chat')
def chat():
    name = session.get('name', '')
    room = session.get('room', '')
    if name == '' or room == '':
        return redirect(url_for('.index'))
    return render_template('chat.html', name=name, room=room)
