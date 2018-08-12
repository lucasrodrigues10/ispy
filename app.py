from flask import Flask, render_template, request
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'fsociety3141@gmail.com'
app.config['MAIL_PASSWORD'] = '!2x75O3b0&iy'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)


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


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
