from flask import redirect, url_for, request, flash, render_template, Flask
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_user, logout_user, LoginManager
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import FileField
from flask_wtf.file import FileAllowed  # Changed import
from models import db, Project, Experience, Skill, Education, User, Profile
from forms import LoginForm
from werkzeug.utils import secure_filename
import os


class BaseModelView(ModelView):
    can_delete = True
    can_create = True
    can_edit = True
    can_export = True

class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin.login_view', next=request.url))

class ProfileView(SecureModelView):
    column_list = ['name', 'title', 'description', 'image_path', 'cv_path']
    form_columns = ['name', 'title', 'description', 'image_path', 'cv_path', 
                   'github_url', 'linkedin_url', 'kaggle_url']  # Changed from twitter_url
    form_extra_fields = {
        'image_path': FileField('Profile Image', validators=[
            FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
        ])
    }

    def on_model_change(self, form, model, is_created):
        if form.image_path.data:
            model.save_image(form.image_path.data)
        
        if form.cv_path.data:
            filename = secure_filename(form.cv_path.data.filename)
            form.cv_path.data.save(os.path.join('static', 'files', filename))
            model.cv_path = f'files/{filename}'

class ProjectView(SecureModelView):
    column_searchable_list = ['title', 'description']
    column_filters = ['tech_used', 'created_at']
    column_list = ['title', 'description', 'tech_used', 'created_at']
    form_columns = ['title', 'description', 'image_url', 'tech_used', 
                   'github_link', 'preview_link']
    form_extra_fields = {
        'image_url': FileField('Project Image', validators=[
            FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
        ])
    }

    def on_model_change(self, form, model, is_created):
        if form.image_url.data:
            model.save_image(form.image_url.data)

class ExperienceView(SecureModelView):
    column_searchable_list = ['title', 'company']
    column_filters = ['period']
    column_list = ['period', 'title', 'company', 'description']

class SkillView(SecureModelView):
    column_list = ['name', 'icon', 'level']
    column_filters = ['level']

class EducationView(SecureModelView):
    column_list = ['period', 'degree', 'institution', 'description']
    column_searchable_list = ['institution', 'degree']

class UserView(SecureModelView):
    column_list = ['username']
    form_columns = ['username', 'password']

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.password = generate_password_hash(form.password.data)

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        
        stats = {
            'projects': Project.query.count(),
            'skills': Skill.query.count(),
            'experiences': Experience.query.count(),
            'education': Education.query.count()
        }
        
        recent_projects = Project.query.order_by(Project.created_at.desc()).limit(5).all()
        
        return self.render('admin/index.html', stats=stats, recent_projects=recent_projects)

    @expose('/login', methods=['GET', 'POST'])
    def login_view(self):
        if current_user.is_authenticated:
            return redirect(url_for('.index'))
            
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and check_password_hash(user.password, form.password.data):
                login_user(user)
                flash('Logged in successfully.', 'success')
                next_url = request.args.get('next')
                if next_url and next_url.startswith('/'):
                    return redirect(next_url)
                return redirect(url_for('.index'))
            flash('Invalid username or password', 'error')
        return render_template('admin/login.html', form=form)

    @expose('/logout')
    def logout_view(self):
        logout_user()
        flash('Logged out successfully.', 'success')
        return redirect(url_for('.login_view'))

def init_admin(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login_view'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    admin = Admin(
        app,
        name='Portfolio Admin',
        template_mode='bootstrap4',
        index_view=MyAdminIndexView(),
        base_template='admin/master.html'
    )

    # Add views
    admin.add_view(ProfileView(Profile, db.session, name='Profile'))
    admin.add_view(ProjectView(Project, db.session, name='Projects'))
    admin.add_view(ExperienceView(Experience, db.session, name='Experience'))
    admin.add_view(SkillView(Skill, db.session, name='Skills'))
    admin.add_view(EducationView(Education, db.session, name='Education'))
    admin.add_view(UserView(User, db.session, name='Users'))

    return admin

# Run this code once to create directories
def create_upload_dirs():
    dirs = [
        'static/images/profile',
        'static/images/projects'
    ]
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)

# Add this to your app.py
app = Flask(__name__)

# Create upload directories
create_upload_dirs()