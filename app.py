from flask import Flask, render_template, jsonify, request
import subprocess  # For running external Python scripts

app = Flask(__name__)  # Initialize the Flask application

@app.route('/')
def index():
    return render_template('index.html')  # Render the HTML file

@app.route('/run_hand', methods=['POST'])  # Route for running hand gesture recognition
def run_hand():
    try:
        subprocess.run(['python', 'hand.py'], check=True)  # Run the hand.py script
        return jsonify({"status": "success", "message": "Hand gesture recognition launched!"})  # Success response
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})  # Error response

@app.route('/run_combo', methods=['POST'])  # Route for running text-to-avatar
def run_combo():
    try:
        word_input = request.json.get('word', '').strip().upper()  # Get word input from frontend
        if not word_input:  # Check if input is empty
            return jsonify({"status": "error", "message": "No word or phrase provided!"})

        # Run combo.py and pass the word input
        process = subprocess.Popen(['python', 'combo.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate(input=word_input)  # Communicate input to the script

        if process.returncode == 0:  # Check if the script ran successfully
            return jsonify({"status": "success", "message": stdout})  # Success response
        else:
            return jsonify({"status": "error", "message": stderr.strip()})  # Error response
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})  # Handle other exceptions

@app.route('/run_speech', methods=['POST'])  # Route for running speech-to-avatar
def run_speech():
    try:
        subprocess.run(['python', 'speech.py'], check=True)  # Run the speech.py script
        return jsonify({"status": "success", "message": "Speech-to-Avatar recognized and video played!"})  # Success response
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})  # Error response

if __name__ == '__main__':
    app.run(debug=True)
