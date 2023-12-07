from flask import Flask, render_template, request, redirect, url_for, session
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
import os

from werkzeug.security import check_password_hash

app = Flask(__name__)
app = Flask(__name__, static_folder='static')
# Configuration de la base de données MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3306/dbtest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Clé secrète pour gérer la session

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
    return render_template('Home.html')
@app.route('/connexion')
def connexion():
    return render_template('index.html')
@app.route('/details')
def details():
    return render_template('details.html')
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

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            # Si l'utilisateur existe et que le mot de passe correspond, connectez l'utilisateur
            session['user_id'] = user.id
            return redirect(url_for('home'))  # Redirection vers la page d'accueil après connexion

    return render_template('index.html')

@app.route('/home')
def home():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        return render_template('home.html', user=user)
    else:
        return redirect(url_for('index'))





if __name__ == '__main__':
    db.create_all()  # Création des tables dans la base de données
    app.run(debug=True)



