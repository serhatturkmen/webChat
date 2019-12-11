# -*- coding: utf-8 -*-
from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio
import  sqlite3

@socketio.on('joined', namespace='/chat')
def joined(message):
    """Müşteriler bir odaya girdiklerinde gönderilir.
     Odadaki tüm insanlara bir durum mesajı yayınlanır."""
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('name') + ' adlı kullanıcı odaya katıldı.'}, room=room)
    #mesaj=session.get('name')+' '+'adlı kullanıcı odaya katıldı.'
    #ekle(mesaj,room)

def ekle(mesaj,room):

    vt=sqlite3.connect('database.db')
    im=vt.cursor()
    im.execute("INSERT INTO mesajlar(mesaj,oda) VALUES(?,?)",[mesaj,room])
    vt.commit()
    vt.close()

@socketio.on('text', namespace='/chat')
def text(message):
    """Kullanıcı yeni bir mesaj girdiğinde bir istemci tarafından gönderilir.
    Mesaj odadaki tüm insanlara gönderilir."""
    room = session.get('room')
    emit('message', {'msg': message['msg'],'name':session.get('name')}, room=room)
    #mesaj=session.get('name') + ':' + message['msg']
    #ekle(mesaj,room)

@socketio.on('left', namespace='/chat')
def left(message):
    """Bir odadan çıktıklarında istemciler tarafından gönderilir.
     Odadaki tüm insanlara bir durum mesajı yayınlanır."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' adlı kullanıcı odadan ayrıldı.'}, room=room)
    #mesaj=session.get('name')+' '+' adlı kullanıcı odadan ayrıldı.'
    #ekle(mesaj,room)
