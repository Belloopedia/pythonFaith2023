from flask import Flask
from flask import Mail, Message
from flask import render_template, request, redirect, url_for, flash
from flask import SQLAlchemy
from twilio.rest import Client

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'f9bf78b9a18ce6d46a0cd2b0b86df9da'
app.config['MAIL_SERVER'] = 'smtp.YourMapper.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'myfreelancehotline@gmail.com'
app.config['MAIL_PASSWORD'] = 'oluwadamilola$1'
app.config['TWILIO_SID'] = 'AC5b81922e71cda6617342143004b44ca8'
app.config['TWILIO_AUTH_TOKEN'] = '362bc3175dcf84ff1fb76d3db7fb80f7'
app.config['TWILIO_PHONE_NUMBER'] = '+2348144945940'

db = SQLAlchemy(app)
mail = Mail(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False, unique=True)
    meter_number = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        phone_number = request.form['phone_number']
        meter_number = request.form['meter_number']
        email = request.form['email']
        password = request.form['password']

        user = User(name=name, address=address, phone_number=phone_number,
                    meter_number=meter_number, email=email, password=password)

        db.session.add(user)
        db.session.commit()

        send_email(user.email)
        send_sms(user.phone_number)

        flash('Registration successful! Check your email and phone for confirmation.')
        return redirect(url_for('login'))

    return render_template('register.html')


def send_email(email):
    message = Message('Registration Confirmation', sender='myfreelancehotline@gmail.com', recipients=[email])
    message.body = 'Thank you for registering with our electricity payment system!'
    mail.send(message)


def send_sms(phone_number):
    account_sid = app.config['AC5b81922e71cda6617342143004b44ca8']
    auth_token = app.config['362bc3175dcf84ff1fb76d3db7fb80f7']
    client = Client(account_sid, auth_token)

    client.messages.create(
        body='Thank you for registering with our electricity payment system!',
        from_=app.config['TWILIO_PHONE_NUMBER'],
        to=phone_number
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Add login logic here
    return render_template('login.html')


@app.route('/billing')
def billing():
    # Add billing logic here
    return render_template('billing.html')


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(use_reloader=False, debug=False)
