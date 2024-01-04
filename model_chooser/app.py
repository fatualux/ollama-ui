from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO
import subprocess
import json
import os

app = Flask(__name__)
socketio = SocketIO(app)


def get_models():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    models_path = os.path.join(current_dir, 'models.json')

    with open(models_path) as json_file:
        models = json.load(json_file)
    return models


@app.route('/')
def index():
    models = get_models()
    return render_template('index.html', models=models)


@app.route('/run_model', methods=['POST'])
def run_model():
    selected_model = request.form['model']
    if selected_model:
        command = ["ollama", "run", selected_model]
        debug_message = f"Executing command: {' '.join(command)}"
        print(debug_message)
        subprocess.Popen(command)
        socketio.emit('model_execution_started', {'message':
                                                  'Model execution started.'})
        return redirect(url_for('execution'))
    else:
        return "Error: Model not selected"


@app.route('/execution')
def execution():
    return render_template('execution.html')


@app.route('/list_models', methods=['POST'])
def list_models():
    command = ["ollama", "list"]
    result = subprocess.run(command, capture_output=True, text=True)
    return render_template('result.html', result=result.stdout)


@app.route('/show_model', methods=['POST'])
def show_model():
    selected_model = request.form['model']
    selected_option = request.form.get('option')

    if selected_model:
        command = ["ollama", "show", selected_model]

        if selected_option:
            command.extend(["--" + selected_option])

        result = subprocess.run(command, capture_output=True, text=True)
        return render_template('result.html', result=result.stdout)
    else:
        return "Error: Model not selected"


@app.route('/remove_model', methods=['POST'])
def remove_model():
    selected_model = request.form['model']
    if selected_model:
        command = ["ollama", "rm", selected_model]
        subprocess.run(command)
        return "Model removed successfully."
    else:
        return "Error: Model not selected"


if __name__ == '__main__':
    socketio.run(app, debug=True)
