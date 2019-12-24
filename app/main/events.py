# -*- coding: utf-8 -*-
from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio
import  sqlite3
from datetime import datetime
kullanicilar=list()

@socketio.on('joined', namespace='/chat')
def joined(message):
    """Müşteriler bir odaya girdiklerinde gönderilir.
     Odadaki tüm kullanıcılara bir durum mesajı yayınlanır."""
    room = session.get('room')
    name = session.get('name')
    if(name in kullanicilar):
        join_room(room)
        emit('users', {'user': kullanicilar}, room=room)
        eskiMesajlar(room)
    else:
        join_room(room)
        emit('status', {'msg': name + ' adlı kullanıcı odaya katıldı.','name':name}, room=room)
        mesaj=name+' '+'adlı kullanıcı odaya katıldı.'
        kullanicilar.append(name)
        tarihsaat = datetime.now().strftime("%d-%m-%Y %H:%M")
        ekle(mesaj,room,'',tarihsaat)
        emit('users', {'user': kullanicilar}, room=room)
        eskiMesajlar(room)

def eskiMesajlar(room):
    room = session.get('room')
    vt=sqlite3.connect('database.db')
    im=vt.cursor()
    veriler=im.execute("SELECT * FROM mesajlar WHERE oda=?",[room])
    for veri in veriler:
        emit('message', {'msg': veri[1] ,'name':veri[3],'tarih':veri[4]}, room=room)
    vt.close()

def ekle(mesaj,room,name,tarih):
    vt=sqlite3.connect('database.db')
    im=vt.cursor()
    im.execute("INSERT INTO mesajlar(mesaj,oda,isim,tarih) VALUES(?,?,?,?)",[mesaj,room,name,tarih])
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
    tarihsaat = datetime.now().strftime("%d-%m-%Y %H:%M")
    emit('message', {'msg': mesaj,'name':session.get('name'),'tarih':tarihsaat}, room=room)
    isim=session.get('name')
    ekle(mesaj,room,isim,tarihsaat)

@socketio.on('left', namespace='/chat')
def left(message):
    """Bir odadan çıktıklarında istemciler tarafından gönderilir.
     Odadaki tüm insanlara bir durum mesajı yayınlanır."""
    room = session.get('room')
    name = session.get('name')
    leave_room(room)
    tarihsaat = datetime.now().strftime("%d-%m-%Y %H:%M")
    mesaj=name+' '+' adlı kullanıcı odadan ayrıldı.'
    emit('status', {'msg': mesaj}, room=room)
    kullanicilar.remove(name)
    emit('users', {'user': kullanicilar}, room=room)
    ekle(mesaj,room,'',tarihsaat)
