from flask import Flask, request, jsonify
from recognition.capture_image import capture_images
from recognition.train_model import train_model 

app = Flask(__name__)

@app.route('/start-setup', methods=['POST'])
def start_setup():
    data = request.get_json()
    if data['action'] == 'start_setup':
        user_name = data.get('user_name')
        if not user_name:
            return jsonify({'status': 'error', 'message': 'user_name is required'}), 400
        
        capture_images(user=user_name)
        train_model()
        return jsonify({'status': 'success'}), 200
    return jsonify({'status': 'error'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
