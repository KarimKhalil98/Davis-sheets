from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

work_logs = []  # List to store work logs

@app.route('/add_work_logs', methods=['POST'])
def add_work_logs():
    data = request.get_json()  # Get the JSON data sent from the frontend
    print(data)  # Print the received data for debugging

    work_logs.append(data)  # Append received data to the work_logs list

    return jsonify({'message': 'Work logs submitted successfully!'})

@app.route('/get_logs', methods=['GET'])
def get_logs():
    return jsonify(work_logs)  # Return all stored logs in JSON format

if __name__ == '__main__':
    app.run(debug=True)
