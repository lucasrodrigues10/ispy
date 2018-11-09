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
global flag_msg
flag_msg = False
def monitor_presenca():
	global flag_msg

	while dht_event.is_set():
		delay=1
		
		dist = ultrasonicRead(8) #sensor na porta 7
		
		presenca = False;   		
		
		if (dist <= 130):
			presenca = True
			flag_msg = True
		
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
		#print('Rodando thread')
		socketio.emit('dht_measure', data, namespace='/monitor')
		sleep(delay)
		

def envia_msg():	
	global flag_msg
	print('vendo se ativou...')
	if flag_msg==True:
			setText('teste')
			print("ATIVOU")
			#avisar usuario e receber mensagem do usuario aqui
	sleep(delay)

@app.route("/email", methods=['GET', 'POST'])
def email():
    if request.method == 'POST':
        email_str = request.form['email']
        msg = Message('Hello', sender='fsociety3141@mail.com', recipients=[email_str])
        msg.body = "This is the email body"
        mail.send(msg)
        return 'Sent'
    else:
        return "Get-Error"


@app.route("/escreve/<text>", methods=['GET', 'POST'])
def write(text):
	if flag_msg==True:
		setText(text)
		return 'Sent'
	else: 
		return 'nao permitido'

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
	try:
		dht_event= Event()
		dht_event.set()
		
		#msg_event = Event()
		
		dht_thread = threading.Thread(target= monitor_presenca)

		dht_thread.start()

		setRGB(255,255,255)
		setText('iniciado a monitoracao')

	        print('Iniciando servidor na porta 5000.')
		socketio.run(app, debug=True, host='0.0.0.0')
				

		while True:
			pass
	except :
		pass
	finally:
		print('Desligando...')
		dht_event.clear()	
		
		dht_thread.join()
		'''
		if dht_thread.isAlive():
			thread_stop_event.clear()
            		dht_thread.join()

		if lcd_thread.isAlive():
			thread_stop_event.clear()

            		lcd_thread.join()
		'''
		setText('')
		print('Servidor terminado.')	
    #app.run(debug=True)
