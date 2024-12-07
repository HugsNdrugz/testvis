from replit import db
import os
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "message_viewer_secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
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
    try:
        settings = Settings.query.first()
        return jsonify({
            'account': {
                'name': settings.name if settings else 'User',
                'avatar': settings.avatar if settings else 'https://via.placeholder.com/100'
            },
            'activeStatus': settings.active_status if settings else True,
            'notifications': {
                'notificationSounds': settings.notification_sounds if settings else True,
                'doNotDisturb': settings.do_not_disturb if settings else False
            },
            'darkMode': settings.dark_mode if settings else 'off'
        })
    except Exception as e:
        app.logger.error(f"Error in settings: {str(e)}")
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

with app.app_context():
    db.create_all()
