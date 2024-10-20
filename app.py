from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# In-memory storage for logs and admin credentials
work_logs = []
admin_password = None  # Placeholder for storing the admin password

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_work_log():
    data = request.json
    name = data['name']
    wo_number = data['wo_number']
    ticket_number = data['ticket_number']
    week_start = data['week_start']
    week_end = data['week_end']
    hours = data['hours']  # Should be a list
    not_applicable = data['not_applicable']  # Should be a list

    # Store logs
    for i, date in enumerate(get_dates(week_start, week_end)):
        work_logs.append({
            'name': name,
            'wo_number': wo_number,
            'ticket_number': ticket_number,
            'date': date,
            'hours': hours[i],
            'not_applicable': not_applicable[i]
        })

    return jsonify({'message': 'Work log submitted successfully!'})

@app.route('/get_logs', methods=['GET'])
def get_logs():
    name = request.args.get('name')
    password = request.args.get('password')

    # Check if the admin password is correct
    if password != admin_password:
        return jsonify({'error': 'Invalid password'}), 403

    if name:  # Basic check for name
        filtered_logs = [log for log in work_logs if log['name'].lower() == name.lower()]
        return jsonify(filtered_logs)
    return jsonify([])

@app.route('/set_admin_password', methods=['POST'])
def set_admin_password():
    global admin_password
    data = request.json
    admin_password = data['password']
    return jsonify({'message': 'Admin password set successfully!'})

def get_dates(start_date, end_date):
    """ Generate a list of dates between start_date and end_date """
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    return [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end - start).days + 1)]

if __name__ == '__main__':
    app.run(debug=True)
