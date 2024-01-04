from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
import random
import string
import os
import mysql.connector
from werkzeug.security import check_password_hash









app = Flask(__name__)
app = Flask(__name__, static_folder='static')
app.secret_key = 'yasmine'






# Configuration de la connexion à la base de données MySQL
#db = mysql.connector.connect(
#    host="localhost",
#    user="root",
#    password="",
#    database="dbtest"
#)
#cursor = db.cursor()



# Configuration de la base de données MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3306/dbtest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Replace with your SMTP server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'khaldiyasmine27@gmail.com'  # Your email username
app.config['MAIL_PASSWORD'] = 'hcjo ivsr zbrs pusv'  # Your email password
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
# Initialisation des extensions
db = SQLAlchemy(app)
mail = Mail(app)




# Modèle de données pour la table User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    civility = db.Column(db.String(10))
    date_of_birth = db.Column(db.String(20))



@app.route('/')
def index():
    return render_template('home.html')


@app.route('/connexion')
def connexion():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']
        civility = request.form['civility']
        date_of_birth = request.form['dateOfBirth']
        cv = request.files['cv'] if 'cv' in request.files else None

        # Création d'un nouvel utilisateur et enregistrement dans la base de données
        new_user = User(
            name=name,
            email=email,
            password=password,
            civility=civility,
            date_of_birth=date_of_birth
            # Ajoutez d'autres champs au besoin
        )
        db.session.add(new_user)
        db.session.commit()
        # Perform your account creation logic here
        # ...

        # For now, let's just print the received data
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Password: {password}")
        print(f"Confirm Password: {confirm_password}")
        print(f"Civility: {civility}")
        print(f"Date of Birth: {date_of_birth}")
        if cv:
            cv_filename = cv.filename  # Retrieve the file name
            print(f"Uploaded CV: {cv_filename}")





        send_confirmation_email(name, email)  # Send confirmation email
        return redirect(url_for('success'))

    return render_template('index.html')

def send_confirmation_email(name, email):
    msg = Message('Account Created Successfully',
                  sender='your-email@example.com',  # Replace with your email address
                  recipients=[email])
    msg.body = f"Dear {name},\nYour account has been successfully created! Thank you."
    mail.send(msg)




@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Vérification des informations d'identification de l'utilisateur dans la base de données
        user = User.query.filter_by(email=email, password=password).first()

        if user:
            # Utilisateur trouvé, connecté avec succès

            return redirect(url_for('dashboard'))
        else:
            # Redirection vers la page de connexion en cas d'échec d'authentification
            return redirect(url_for('connexion'))

    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()

        if user:
            new_password = generate_new_password()
            user.password = new_password
            db.session.commit()

            # Envoi de l'e-mail avec le nouveau mot de passe
            send_password_reset_email(user.email, new_password)

            flash('Password reset successfully. Check your email for the new password.')
            return redirect(url_for('connexion'))
        else:
            flash("Email doesn't exist in our records.")

    return render_template('forgot_password.html')

def generate_new_password():
    import secrets
    import string
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(10))

def send_password_reset_email(email, new_password):
    msg = Message('Password Reset', sender='your_username@example.com', recipients=[email])
    msg.body = f'Your new password is: {new_password}'
    mail.send(msg)








if __name__ == '__main__':
    db.create_all()  # Création des tables dans la base de données
    app.run(debug=True)



