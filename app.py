import os
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "message_viewer_secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///messages.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

from models import Contact, Message, Call, Settings

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contacts')
def get_contacts():
    contacts = Contact.query.all()
    return jsonify([{
        'name': contact.name,
        'phone': contact.phone,
        'avatar': contact.avatar
    } for contact in contacts])

@app.route('/sms/<contact_name>')
def get_messages(contact_name):
    messages = Message.query.join(Contact).filter(Contact.name == contact_name).all()
    return jsonify([{
        'text': msg.text,
        'time': msg.timestamp.strftime('%I:%M %p'),
        'type': 'sent' if msg.is_sent else 'received'
    } for msg in messages])

@app.route('/calls')
def get_calls():
    calls = Call.query.join(Contact).all()
    return jsonify([{
        'type': call.call_type,
        'time': call.timestamp.strftime('%I:%M %p'),
        'duration': call.duration,
        'name': call.contact.name
    } for call in calls])

@app.route('/settings')
def get_settings():
    settings = Settings.query.first()
    if not settings:
        return jsonify({
            'account': {
                'name': 'User',
                'avatar': 'https://via.placeholder.com/100'
            },
            'activeStatus': True,
            'notifications': {
                'notificationSounds': True,
                'doNotDisturb': False
            },
            'darkMode': 'off'
        })
    return jsonify({
        'account': {
            'name': settings.name,
            'avatar': settings.avatar
        },
        'activeStatus': settings.active_status,
        'notifications': {
            'notificationSounds': settings.notification_sounds,
            'doNotDisturb': settings.do_not_disturb
        },
        'darkMode': settings.dark_mode
    })

with app.app_context():
    db.create_all()
