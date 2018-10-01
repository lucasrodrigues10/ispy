from gevent import monkey
monkey.patch_all()
from flask_socketio import SocketIO
from flask import Flask, render_template, request
from time import sleep
from time import strftime
from threading import Thread, Event
from grovepi import *
import threading
import time
from flask_mail import Mail, Message
from grove_rgb_lcd import *

__author__ = 'tio levon'

#configuracao do servidor
app = Flask(__name__)

app.config['SECRET_KEY'] = 'pinkguy'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'fsociety3141@gmail.com'
app.config['MAIL_PASSWORD'] = '!2x75O3b0&iy'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

# Grove PI
socketio = SocketIO(app)
global data_total
def monitor_presenca():
	while dht_event.is_set():
		delay=1
		dist = ultrasonicRead(7) #sensor na porta 7
		presenca = False;   		
		
		if (dist <= 130):
			presenca = True

		data = {
			'dist' : dist,
			'presenca':presenca
		}
		
		'''
		data['tempo'].append(round(time.time() % 60,1))
		data['temp'].append(temp)
		data['hum'].append(hum)
		'''
		print('Tem Alguem??: ',presenca,'Distancia:  ',dist)
		socketio.emit('dht_measure', data, namespace='/monitor')
		sleep(delay)


@app.route("/email", methods=['GET', 'POST'])
def email():
    if request.method == 'POST':
        email_str = request.form['email']
        msg = Message('Hello', sender='fsociety3141@gmail.com', recipients=[email_str])
        msg.body = "This is the email body"
        mail.send(msg)
        return 'Sent'
    else:
        return "Get-Error"


@app.route("/escreve/<text>", methods=['GET', 'POST'])
def write(text):
	setText(text)
	return 'Sent'

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
	try:
		dht_event= Event()
		dht_event.set()

		dht_thread = threading.Thread(target= monitor_presenca)
		dht_thread.start()

		setRGB(255,255,255)
		#setText('LCD ta funfano meo!')

	        print('Iniciando servidor na porta 5000.')
		socketio.run(app, debug=True, host='0.0.0.0')
		while True:
			pass
	except:
		dht_event.clear()
		dht_thread.join()
	finally:
		print('Desligando...')
		if dht_thread.isAlive():
			thread_stop_event.clear()
            		dht_thread.join()
		print('Servidor terminado.')	
    #app.run(debug=True)
