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

@app.route('/messages',methods=['GET'])
def messages():
    messages = Message.query.all()
    if not messages:
        return jsonify({'message':'Messages not found'}),404
    return jsonify([message.to_dict() for message in messages])

@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    new_message = Message(body=data['body'],username=data['username'])
    db.session.add(new_message)
    db.session.commit()
    return jsonify(new_message.to_dict()),201

@app.route('/messages/<int:id>',methods=['PATCH'])
def messages_by_id(id):
    data= request.get_json()
    message = Message.query.get(id)
    if not message:
        return jsonify({'message':'Message not found'}),404
    message.body= data['body']
    #message.username= data['username']
    db.session.commit()
    return jsonify(message.to_dict()),201

@app.route('/messages/<int:id>',methods=['DELETE'])
def delete_message(id):
    message = Message.query.get(id)
    if not message:
        return jsonify({'message':'The message you want to delete does not exist'}),404
    db.session.delete(message)
    db.session.commit()
    return jsonify({'message':'Message delated successfully'}),201

if __name__ == '__main__':
    app.run(port=5555)
