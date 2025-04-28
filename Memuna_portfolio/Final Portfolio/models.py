from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.utils import secure_filename
import os

db = SQLAlchemy()

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image_path = db.Column(db.String(200))
    cv_path = db.Column(db.String(200))
    github_url = db.Column(db.String(200))
    linkedin_url = db.Column(db.String(200))
    kaggle_url = db.Column(db.String(200))  # Changed from twitter_url

    def save_image(self, image_file):
        if image_file:
            filename = secure_filename(image_file.filename)
            filepath = os.path.join('static', 'images', 'profile', filename)
            image_file.save(filepath)
            self.image_path = os.path.join('images', 'profile', filename)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200))
    tech_used = db.Column(db.String(200))
    github_link = db.Column(db.String(200))
    preview_link = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def save_image(self, image_file):
        if image_file:
            filename = secure_filename(image_file.filename)
            filepath = os.path.join('static', 'images', 'projects', filename)
            image_file.save(filepath)
            self.image_url = os.path.join('images', 'projects', filename)

class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    period = db.Column(db.String(50))
    title = db.Column(db.String(100))
    company = db.Column(db.String(100))
    description = db.Column(db.Text)

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    icon = db.Column(db.String(50))
    level = db.Column(db.Integer)

class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    period = db.Column(db.String(50))
    degree = db.Column(db.String(100))
    institution = db.Column(db.String(100))
    description = db.Column(db.Text)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)