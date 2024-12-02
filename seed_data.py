from app import app, db
from models import Contact, Message, Call, Settings
from datetime import datetime, timedelta

def seed_database():
    with app.app_context():
        # Create sample contacts
        contacts = [
            Contact(name='Samuel Diamond', phone='+1234567890', avatar='https://via.placeholder.com/50'),
            Contact(name='Nigel Jackson', phone='+1987654321', avatar='https://via.placeholder.com/50'),
            Contact(name='Austin Clayton', phone='+1122334455', avatar='https://via.placeholder.com/50')
        ]
        db.session.add_all(contacts)
        db.session.commit()

        # Create sample messages
        messages = [
            Message(contact_id=1, text='How ya guys doing', timestamp=datetime.now() - timedelta(hours=3), is_sent=False),
            Message(contact_id=1, text='Hey buddy', timestamp=datetime.now() - timedelta(hours=2), is_sent=True),
            Message(contact_id=2, text='You: Hey buddy', timestamp=datetime.now() - timedelta(hours=11), is_sent=True)
        ]
        db.session.add_all(messages)

        # Create sample calls
        calls = [
            Call(contact_id=1, call_type='incoming', timestamp=datetime.now() - timedelta(days=1), duration=5),
            Call(contact_id=2, call_type='outgoing', timestamp=datetime.now() - timedelta(days=2), duration=10),
            Call(contact_id=3, call_type='missed', timestamp=datetime.now() - timedelta(days=3), duration=0)
        ]
        db.session.add_all(calls)

        # Create settings
        settings = Settings(
            name='Austin Clayton',
            avatar='https://via.placeholder.com/100',
            active_status=True,
            notification_sounds=True,
            do_not_disturb=False,
            dark_mode='off'
        )
        db.session.add(settings)
        
        db.session.commit()

if __name__ == '__main__':
    try:
        print("Starting database seeding...")
        seed_database()
        print("Database seeding completed successfully!")
    except Exception as e:
        print(f"Error seeding database: {str(e)}")
