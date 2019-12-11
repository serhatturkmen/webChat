'''
#!/bin/env python
'''
#!"C:\Program Files (x86)\Python38\python.exe"
from app import create_app, socketio

app = create_app(debug=True)

if __name__ == '__main__':
    socketio.run(app)
