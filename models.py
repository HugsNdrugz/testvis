from datetime import datetime
from app import db

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    avatar = db.Column(db.String(200))
    messages = db.relationship('Message', backref='contact', lazy=True)
    calls = db.relationship('Call', backref='contact', lazy=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_sent = db.Column(db.Boolean, default=False)

class Call(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=False)
    call_type = db.Column(db.String(20))  # incoming, outgoing, missed
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    duration = db.Column(db.Integer)  # duration in minutes

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    avatar = db.Column(db.String(200))
    active_status = db.Column(db.Boolean, default=True)
    notification_sounds = db.Column(db.Boolean, default=True)
    do_not_disturb = db.Column(db.Boolean, default=False)
    dark_mode = db.Column(db.String(10), default='off')
