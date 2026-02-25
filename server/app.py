from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Message

app = Flask(__name__)

# -----------------------------
# Configuration
# -----------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Enable CORS so React can access API
CORS(app)


# =========================================================
# GET /messages
# Returns all messages ordered by created_at ASC
# =========================================================
@app.route('/')
def home():
    return {"message": "Chatterbox API is running!"}

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([message.to_dict() for message in messages]), 200


# =========================================================
# POST /messages
# Creates a new message
# =========================================================
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()

    if not data or not data.get("body") or not data.get("username"):
        return jsonify({"error": "Body and username are required"}), 400

    new_message = Message(
        body=data["body"],
        username=data["username"]
    )

    db.session.add(new_message)
    db.session.commit()

    return jsonify(new_message.to_dict()), 201


# =========================================================
# PATCH /messages/<id>
# Updates message body
# =========================================================
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get_or_404(id)
    data = request.get_json()

    if not data or "body" not in data:
        return jsonify({"error": "Body is required to update"}), 400

    message.body = data["body"]
    db.session.commit()

    return jsonify(message.to_dict()), 200


# =========================================================
# DELETE /messages/<id>
# Deletes a message
# =========================================================
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get_or_404(id)

    db.session.delete(message)
    db.session.commit()

    return '', 204


# -----------------------------
# Run Server
# -----------------------------
if __name__ == '__main__':
    app.run(port=5000, debug=True)