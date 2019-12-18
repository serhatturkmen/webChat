# -*- coding: utf-8 -*-
from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio
import  sqlite3
kullanicilar=list()
@socketio.on('joined', namespace='/chat')
def joined(message):
    """Müşteriler bir odaya girdiklerinde gönderilir.
     Odadaki tüm kullanıcılara bir durum mesajı yayınlanır."""
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('name') + ' adlı kullanıcı odaya katıldı.','name':session.get('name')}, room=room)
    mesaj=session.get('name')+' '+'adlı kullanıcı odaya katıldı.'
    kullanicilar.append(session.get('name'))
    emit('users', {'user': kullanicilar}, room=room)
    ekle(mesaj,room,'')
    eskiMesajlar(room)
def eskiMesajlar(room):
    room = session.get('room')
    vt=sqlite3.connect('database.db')
    im=vt.cursor()
    veriler=im.execute("SELECT * FROM mesajlar WHERE oda=?",[room])
    for veri in veriler:
        emit('message', {'msg': veri[1] ,'name':veri[3]}, room=room)
    vt.close()
def ekle(mesaj,room,name):
    vt=sqlite3.connect('database.db')
    im=vt.cursor()
    im.execute("INSERT INTO mesajlar(mesaj,oda,isim) VALUES(?,?,?)",[mesaj,room,name])
    vt.commit()
    vt.close()

@socketio.on('text', namespace='/chat')
def text(message):
    #gelen mesaj içeriğini odadaki kullanıcılara gönderiyor.
    """Kullanıcı yeni bir mesaj girdiğinde bir istemci tarafından gönderilir.
    Mesaj odadaki tüm insanlara gönderilir."""
    room = session.get('room')
    #türkçe karakter sorunu
    mesaj = message['msg'].encode('latin-1').decode('utf-8')
    emit('message', {'msg': mesaj,'name':session.get('name')}, room=room)
    isim=session.get('name')
    mesaj=mesaj
    ekle(mesaj,room,isim)

@socketio.on('left', namespace='/chat')
def left(message):
    """Bir odadan çıktıklarında istemciler tarafından gönderilir.
     Odadaki tüm insanlara bir durum mesajı yayınlanır."""
    room = session.get('room')
    name = session.get('name')
    leave_room(room)
    emit('status', {'msg': name + ' adlı kullanıcı odadan ayrıldı.'}, room=room)
    kullanicilar.remove(name)
    emit('users', {'user': kullanicilar}, room=room)
    mesaj=name+' '+' adlı kullanıcı odadan ayrıldı.'
    ekle(mesaj,room,'')
