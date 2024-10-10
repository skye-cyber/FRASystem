import webview
import threading
import os
# pip install PyQt5
# pip install PySide2
# sudo apt-get install python3-gi
# pip install PyGObject

def start_django():
    os.system('python manage.py runserver')


if __name__ == '__main__':
    t = threading.Thread(target=start_django)
    t.daemon = True
    t.start()

    webview.create_window('Face Recognition Attendance System', 'http://127.0.0.1:8001')
    webview.start()
