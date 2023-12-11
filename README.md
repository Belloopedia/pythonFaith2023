## Getting Started
You need to install the required packages, initially you were importing from the wrong package; now i've installed the right packages and you find them in the requirements.txt file, i also removed the secret keys of which is bad to keep it open here, because you may be maliciously attack by anyone that could have does keys, so you can replace the "xxxxxxxxxx" with the keys.

### To setup the project.
Clone the project.
```console

git clone <git-url>
```

Enter the directory
```console

cd pythonFaith2023
```

Install the required packages
```console

pip install -r requirements.txt
```

### Run
Describe how you use it here.
```console

python app3.py
```

## Built With
Explain which technologies you've used here.

### Flask (3.0.0):

- Flask is a lightweight web framework for Python.
- It provides a simple and easy-to-use interface for building web applications.
- Flask follows the WSGI (Web Server Gateway Interface) specification and is designed to be extensible and modular.
- It includes features for routing, handling requests and responses, and working with templates.

### Flask-Mail (0.9.1):

- Flask-Mail is an extension for Flask that simplifies email sending in Flask applications.
- It provides a Mail class that you can use to send emails from your application.
- Flask-Mail integrates with Flask's configuration system, making it easy to set up email settings.

### Flask-SQLAlchemy (3.1.1):

- Flask-SQLAlchemy is an extension for Flask that simplifies database integration using SQLAlchemy.
- SQLAlchemy is a powerful SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- Flask-SQLAlchemy simplifies the configuration and integration of SQLAlchemy with Flask applications.
- It provides a SQLAlchemy object that you can use to interact with your database using SQLAlchemy models.

### Flask-WTF (1.2.1):

- Flask-WTF is an extension for Flask that integrates with the WTForms library.
- WTForms is a library for handling web forms in Flask applications.
- Flask-WTF simplifies form handling and validation in Flask applications.
- It includes features for form rendering, data validation, and CSRF protection.

These technologies together provide a robust foundation for developing web applications with Flask, including features for handling emails, working with databases, and managing web forms.