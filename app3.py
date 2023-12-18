from flask import Flask
from flask_mail import Mail, Message
from flask import render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, SubmitField
from twilio.rest import Client
from wtforms.validators import InputRequired

app = Flask(__name__)
csrf = CSRFProtect(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'xxxxxxxxxxxxxxxxxxxxx'
app.config['MAIL_SERVER'] = 'xxxxxxxxxxxxxxxxxxxxxx'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'xxxxxxxxxxxxxxxxxxx'
app.config['MAIL_PASSWORD'] = 'xxxxxxxxxxxxxxxxxxxxx'
app.config['TWILIO_SID'] = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
app.config['TWILIO_AUTH_TOKEN'] = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
app.config['TWILIO_PHONE_NUMBER'] = 'xxxxxxxxxxx'

db = SQLAlchemy(app)
mail = Mail(app)


class RegisterForm(FlaskForm):
    name = StringField('Name')
    address = StringField('Address')
    phone_number = StringField('Phone Number')
    meter_number = StringField('Meter Number')
    email = StringField('Email')
    password = StringField('Password')
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email')
    password = StringField('Password')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    meter_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False) # Add unique=True for uniqueness
    password = db.Column(db.String(60), nullable=False)


@app.route('/')
def index():
    return render_template('index.html')
app.config['SERVE_STATIC'] = True

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Process the form data
        name = form.name.data
        address = form.address.data
        phone_number = form.phone_number.data
        meter_number = form.meter_number.data
        email = form.email.data
        password = form.password.data

        # Check if the email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email address already registered. Please use a different email.')
            return redirect(url_for('register'))

        user = User(name=name, address=address, phone_number=phone_number,
                    meter_number=meter_number, email=email, password=password)

        db.session.add(user)
        db.session.commit()

        # YOU CAN UNCOMMENT TO SEND THE EMAIL
        # send_email(user.email)
        # send_sms(user.phone_number)

        flash('Registration successful! Check your email and phone for confirmation.')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


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
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email, password=password).first()

        if user:
            # Log the user in by storing their email in the session
            session['email'] = user.email

            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')
    return render_template('login.html', form=form)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Add other user fields as needed

class Billing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.Date, nullable=False)

class BillingForm(FlaskForm):
    account_type = StringField('Account Type', validators=[InputRequired()])
    routing_number = StringField('Routing Number', validators=[InputRequired()])
    re_enter_routing = StringField('Re-enter Routing', validators=[InputRequired()])
    bank_account_number = StringField('Bank Account Number', validators=[InputRequired()])
    re_enter_bank_account = StringField('Re-enter Bank Account', validators=[InputRequired()])
    name = StringField('Name', validators=[InputRequired()])
    address = StringField('Address', validators=[InputRequired()])
    city = StringField('City', validators=[InputRequired()])
    meter_number = StringField('Meter Number', validators=[InputRequired()])
    state = StringField('State', validators=[InputRequired()])
    zip_code = StringField('Zip', validators=[InputRequired()])
    submit = SubmitField('Submit')

@app.route('/billing/<int:user_id>', methods=['GET', 'POST'])
def billing_route(user_id):
    user = User.query.get_or_404(user_id)
    billing_info = Billing.query.filter_by(user_id=user_id).first()

    form = BillingForm()

    if form.validate_on_submit():
        # Handle form submission and payment logic here
        # Update the payment status in the Billing model
        return redirect(url_for('billing_route', user_id=user_id))

    if billing_info:
        current_reading = get_current_reading()  # Replace with your logic to get current reading
        last_reading = get_last_reading()  # Replace with your logic to get last reading
        total_usage = current_reading - last_reading  # Replace with your logic to calculate total usage
        total_charges = calculate_total_charges(billing_info.amount)  # Replace with your logic to calculate total charges
        billing_total = total_charges + 5.00  # Assuming $5.00 adjustments, replace with your logic
        due_date = billing_info.due_date.strftime('%Y-%m-%d')  # Format due date as needed

        return render_template('billing_template.html',
                               current_user=user,
                               form=form,
                               current_reading=current_reading,
                               last_reading=last_reading,
                               total_usage=total_usage,
                               total_charges=total_charges,
                               billing_total=billing_total,
                               due_date=due_date)
    else:
        return render_template('billing_template.html', user=user, form=form, message='No billing information available.')

@app.route('/make_payment', methods=['POST'])
def make_payment():
    # Handle payment logic here
    # Update the payment status in the Billing model
    # You may use a payment gateway API or a payment form
    return redirect(url_for('billing_route', user_id=User.id))
    
@app.route('/dashboard')
def dashboard():

    if 'email' in session:
        user_email = session['email']
        return render_template('dashboard.html', user_email=user_email)
    else:
        flash('You need to login first.', 'warning')
        return redirect(url_for('login'))


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(use_reloader=True, debug=True)
