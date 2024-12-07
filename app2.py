from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app) # Allow cross-origin requests from the frontend

DB_PATH = 'data.db' # Path to your SQLite database


# Helper function to query the database
def query_db(query, args=(), one=False):
connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()
cursor.execute(query, args)
rows = cursor.fetchall()
connection.close()
return (rows[0] if rows else None) if one else rows


# Endpoint: Get all contacts
@app.route('/contacts', methods=['GET'])
def get_contacts():
rows = query_db("SELECT name, phone_number FROM Contacts;")
return jsonify([{"name": row[0], "phone": row[1]} for row in rows])


# Endpoint: Get SMS messages for a specific contact
@app.route('/sms/<contact_name>', methods=['GET'])
  def get_sms(contact_name):
  rows = query_db("""
  SELECT sms_type, time, text
  FROM SMS
  WHERE from_to LIKE ?
  ORDER BY time DESC;
  """, (f"%{contact_name}%",))
  return jsonify([{"type": row[0], "time": row[1], "text": row[2]} for row in rows])


  # Endpoint: Get archived calls for a specific contact
  @app.route('/calls/<contact_name>', methods=['GET'])
    def get_calls(contact_name):
    rows = query_db("""
    SELECT call_type, time, duration
    FROM Calls
    WHERE from_to LIKE ?
    ORDER BY time DESC;
    """, (f"%{contact_name}%",))
    return jsonify([{"type": row[0], "time": row[1], "duration": row[2]} for row in rows])


    # Endpoint: Get all installed apps
    @app.route('/installed_apps', methods=['GET'])
    def get_installed_apps():
    rows = query_db("SELECT application_name, install_date FROM InstalledApps;")
    return jsonify([{"name": row[0], "installed_on": row[1]} for row in rows])


    # Endpoint: Get user settings
    @app.route('/settings', methods=['GET'])
    def get_settings():
    # Static settings as an example
    settings = {
    "account": {
    "name": "Austin Clayton",
    "avatar": "avatar3.jpg"
    },
    "activeStatus": True,
    "notifications": {
    "notificationSounds": True,
    "doNotDisturb": False
    },
    "darkMode": "off"
    }
    return jsonify(settings)


    if __name__ == '__main__':
    app.run(debug=True)