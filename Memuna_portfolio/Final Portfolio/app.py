from flask import Flask, render_template, request, jsonify, url_for, redirect, flash
from flask_mail import Mail, Message
from flask_babel import Babel
from werkzeug.utils import secure_filename
from models import db, Profile, Project, Experience, Skill, Education, User
from werkzeug.security import generate_password_hash
from config import Config
import os
from admin import init_admin
from flask_login import login_required, logout_user, LoginManager

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
mail = Mail(app)
babel = Babel(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin.login_view'

# Configure Babel locale
@babel.localeselector
def get_locale():
    # Try to guess the language from the user accept
    # header the browser transmits
    return request.accept_languages.best_match(['en'])

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create database tables
def init_db():
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Create default admin user if not exists
        if not User.query.filter_by(username='admin').first():
            admin_user = User(
                username='admin',
                password=generate_password_hash('admin123')
            )
            db.session.add(admin_user)
            
        # Create default profile if not exists
        if not Profile.query.first():
            default_profile = Profile(
                name='Memuna Gul',
                title='AI and ML Engineer',
                description='Experienced AI and ML Engineer passionate about innovation',
                image_path='images/profile.png',
                cv_path='files/cv.pdf',
                github_url='https://github.com/yourusername',
                linkedin_url='https://linkedin.com/in/yourusername',
                kaggle_url='https://kaggle.com/yourusername'
            )
            db.session.add(default_profile)
        
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error during initialization: {e}")

# Initialize database first
if not os.path.exists('instance/portfolio.db'):
    init_db()

# Initialize admin after database is ready
init_admin(app)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Update the index route with error handling
@app.route('/')
def index():
    profile = Profile.query.first()
    if not profile:
        # If no profile exists, create a default one
        profile = Profile(
            name='Memuna Gul ',
            title='AI and ML Engine',
            description='Experienced AI and ML Engineer passionate about innovation',
            image_path='images/profile.png',
            cv_path='files/cv.pdf',
            github_url='https://github.com/yourusername',
            linkedin_url='https://linkedin.com/in/yourusername',
            kaggle_url='https://kaggle.com/yourusername'
        )
        try:
            db.session.add(profile)
            db.session.commit()
        except Exception as e:
            print(f"Error creating default profile: {e}")
            db.session.rollback()
    
    # Debug print to verify profile data
    print("Profile data:", {
        'id': profile.id if profile else None,
        'github': profile.github_url if profile else None,
        'linkedin': profile.linkedin_url if profile else None,
        'kaggle': profile.kaggle_url if profile else None
    })
    
    projects = Project.query.order_by(Project.created_at.desc()).all()
    experiences = Experience.query.all()
    skills = Skill.query.all()
    education = Education.query.all()
    
    return render_template('index.html',
                         profile=profile,
                         projects=projects,
                         experiences=experiences,
                         skills=skills,
                         education=education,
                         active_page='home')

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        msg = Message(
            subject=f'Portfolio Contact from {name}',
            sender=email,
            recipients=[app.config['MAIL_USERNAME']],
            body=f'''
            From: {name}
            Email: {email}
            Message: {message}
            '''
        )
        mail.send(msg)
        
        return jsonify({'status': 'success', 'message': 'Message sent successfully!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)