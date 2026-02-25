from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET'])
def messages():
    """GET /messages: returns an array of all messages as JSON, ordered by created_at in ascending order"""
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([message.to_dict() for message in messages]), 200

@app.route('/messages', methods=['POST'])
def create_message():
    """POST /messages: creates a new message with a body and username from params"""
    data = request.get_json()
    
    # Validate required fields
    if not data or 'body' not in data or 'username' not in data:
        return jsonify({"error": "Body and username are required"}), 400
    
    new_message = Message(
        body=data['body'],
        username=data['username']
    )
    
    db.session.add(new_message)
    db.session.commit()
    
    return jsonify(new_message.to_dict()), 201

@app.route('/messages/<int:id>', methods=['GET'])
def messages_by_id(id):
    """GET /messages/<int:id>: returns a single message as JSON"""
    message = Message.query.filter_by(id=id).first()
    
    if message:
        return jsonify(message.to_dict()), 200
    else:
        return jsonify({"error": "Message not found"}), 404

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    """PATCH /messages/<int:id>: updates the body of the message using params"""
    message = Message.query.filter_by(id=id).first()
    
    if not message:
        return jsonify({"error": "Message not found"}), 404
    
    data = request.get_json()
    
    # Update only the body field (as per requirements)
    if data and 'body' in data:
        message.body = data['body']
    
    db.session.commit()
    
    return jsonify(message.to_dict()), 200

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    """DELETE /messages/<int:id>: deletes the message from the database"""
    message = Message.query.filter_by(id=id).first()
    
    if not message:
        return jsonify({"error": "Message not found"}), 404
    
    db.session.delete(message)
    db.session.commit()
    
    return jsonify({"message": "Message successfully deleted"}), 200

if __name__ == '__main__':
    app.run(port=5555)
    