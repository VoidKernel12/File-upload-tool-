import os
import json
import random
import string
from flask import Flask, render_template_string, request, jsonify, send_from_directory, redirect, url_for

app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters + string.digits, k=24))

# Configurations
UPLOAD_FOLDER = 'vault_files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

METADATA_FILE = 'vault_metadata.json'

# --- Load Existing Rooms from Disk on Startup (Auto-Recovery) ---
def load_rooms():
    if os.path.exists(METADATA_FILE):
        try:
            with open(METADATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

# --- Save Rooms to Disk ---
def save_rooms():
    try:
        with open(METADATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(ROOMS, f, indent=4)
    except Exception as e:
        print(f"Error saving metadata: {e}")

ROOMS = load_rooms()

# --- HTML TEMPLATES ---

HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HeartKiller - Cloud Vault</title>
    <style>
        :root {
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --accent: #ef4444;
            --accent-hover: #dc2626;
            --text: #f8fafc;
            --text-muted: #94a3b8;
            --border: #334155;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            color: var(--text);
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 90vh;
        }
        .container {
            width: 100%;
            max-width: 450px;
            background: var(--card-bg);
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
            border: 1px solid var(--border);
            box-sizing: border-box;
            text-align: center;
        }
        h2 { color: var(--accent); margin-top: 0; }
        p { color: var(--text-muted); font-size: 14px; }
        .btn-group {
            display: flex;
            flex-direction: column;
            gap: 15px;
            margin-top: 25px;
        }
        .btn {
            background: var(--accent);
            color: white;
            padding: 14px;
            border-radius: 8px;
            border: none;
            font-size: 16px;
            font-weight: bold;
            text-decoration: none;
            cursor: pointer;
            transition: background 0.2s;
            display: block;
        }
        .btn:hover { background: var(--accent-hover); }
        .btn-secondary { background: #334155; }
        .btn-secondary:hover { background: #475569; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🔥 HeartKiller Vault</h2>
        <p>Secure Global Real-Time File Sharing & Storage</p>
        
        <div class="btn-group">
            <a href="/upload" class="btn">🚀 Upload Files (Create Room)</a>
            <a href="/access" class="btn btn-secondary">📥 Access Room & Download</a>
        </div>
    </div>
</body>
</html>
"""

UPLOAD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HeartKiller - Upload Portal</title>
    <style>
        :root {
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --accent: #ef4444;
            --accent-hover: #dc2626;
            --text: #f8fafc;
            --text-muted: #94a3b8;
            --border: #334155;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            color: var(--text);
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .container {
            width: 100%;
            max-width: 450px;
            background: var(--card-bg);
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
            border: 1px solid var(--border);
            box-sizing: border-box;
        }
        h2 { color: var(--accent); text-align: center; margin-top: 0; }
        input, button, label, select {
            width: 100%;
            padding: 12px;
            margin: 8px 0;
            border-radius: 8px;
            border: 1px solid var(--border);
            background: #0f172a;
            color: var(--text);
            font-size: 16px;
            box-sizing: border-box;
        }
        button { background: var(--accent); border: none; font-weight: bold; cursor: pointer; }
        button:hover { background: var(--accent-hover); }
        .file-input-label {
            display: block;
            text-align: center;
            background: #334155;
            cursor: pointer;
            border: 2px dashed var(--accent);
            font-weight: bold;
            margin-top: 10px;
        }
        .option-box {
            background: #0f172a;
            padding: 12px;
            border-radius: 8px;
            border: 1px solid var(--border);
            margin-bottom: 12px;
        }
        .radio-label {
            display: flex;
            align-items: center;
            gap: 10px;
            cursor: pointer;
            font-size: 14px;
            margin: 5px 0;
        }
        .alert {
            background: rgba(239, 68, 68, 0.2);
            border: 1px solid var(--accent);
            padding: 10px;
            border-radius: 6px;
            color: #fca5a5;
            margin-bottom: 15px;
            text-align: center;
            font-size: 14px;
        }
        .success {
            background: rgba(16, 185, 129, 0.2);
            border: 1px solid #10b981;
            color: #6ee7b7;
        }
        .center { text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🚀 Upload Portal</h2>
        <p class="center" style="color: var(--text-muted); font-size: 13px;">Choose your auth method to create/join a room</p>

        <div id="status-msg"></div>

        <form id="upload-form">
            <div class="option-box">
                <label style="font-size: 13px; color: var(--text-muted); margin-bottom: 5px; display: block;">Select Authentication Method:</label>
                <label class="radio-label">
                    <input type="radio" name="auth_type" value="number" checked onclick="toggleInput('number')"> Use Custom Number (e.g. 1234)
                </label>
                <label class="radio-label">
                    <input type="radio" name="auth_type" value="token" onclick="toggleInput('token')"> Use Secure Access Token
                </label>
            </div>

            <div id="input-container">
                <input type="text" id="room-code" placeholder="Enter Custom Number (e.g. 1234)" required>
            </div>

            <label class="file-input-label" for="file-picker">
                📁 Click to Select Files
            </label>
            <input type="file" id="file-picker" multiple style="display: none;">

            <div id="selected-info" class="center" style="color: var(--text-muted); font-size: 14px; margin: 10px 0;">No files selected</div>

            <button type="submit">Start Upload</button>
        </form>

        <div class="center" style="margin-top: 15px;">
            <a href="/" style="color: var(--text-muted); text-decoration: none; font-size: 14px;">← Back to Home</a>
        </div>
    </div>

    <script>
        function generateToken() {
            const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
            let token = 'HK-ACC-';
            for(let i=0; i<8; i++) token += chars.charAt(Math.floor(Math.random() * chars.length));
            return token;
        }

        const autoToken = generateToken();

        function toggleInput(type) {
            const container = document.getElementById('input-container');
            if (type === 'number') {
                container.innerHTML = '<input type="text" id="room-code" placeholder="Enter Custom Number (e.g. 1234)" required>';
            } else {
                container.innerHTML = `<input type="text" id="room-code" value="${autoToken}" readonly style="color: #38bdf8; font-family: monospace;" required><p style="font-size: 11px; color: var(--text-muted); margin: 2px 0;">Auto-generated secure access token</p>`;
            }
        }

        const filePicker = document.getElementById('file-picker');
        const selectedInfo = document.getElementById('selected-info');
        const uploadForm = document.getElementById('upload-form');
        const statusMsg = document.getElementById('status-msg');

        filePicker.addEventListener('change', () => {
            const count = filePicker.files.length;
            if (count > 0) {
                selectedInfo.innerText = `${count} file(s) selected.`;
                selectedInfo.style.color = '#34d399';
            } else {
                selectedInfo.innerText = 'No files selected';
                selectedInfo.style.color = '#94a3b8';
            }
        });

        uploadForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const roomCode = document.getElementById('room-code').value.trim();
            const files = filePicker.files;

            if (files.length === 0) {
                statusMsg.innerHTML = '<div class="alert">Please select files first!</div>';
                return;
            }

            const formData = new FormData();
            formData.append('room_code', roomCode);

            for (let i = 0; i < files.length; i++) {
                formData.append('files', files[i]);
            }

            statusMsg.innerHTML = '<div class="alert" style="border-color: #3b82f6; color: #93c5fd;">Uploading files... Please wait.</div>';

            try {
                const response = await fetch('/upload-endpoint', {
                    method: 'POST',
                    body: formData
                });
                const result = await response.json();

                if (response.ok) {
                    statusMsg.innerHTML = `<div class="alert success">${result.message} <br><a href="/room/${roomCode}" style="color: #fff; font-weight: bold; text-decoration: underline;">Open Room Dashboard →</a></div>`;
                    uploadForm.reset();
                    if(document.querySelector('input[value="token"]').checked) {
                        document.getElementById('room-code').value = generateToken();
                    }
                    selectedInfo.innerText = 'No files selected';
                    selectedInfo.style.color = '#94a3b8';
                } else {
                    statusMsg.innerHTML = `<div class="alert">Error: ${result.error}</div>`;
                }
            } catch (err) {
                statusMsg.innerHTML = `<div class="alert">Upload failed: Network connection error.</div>`;
            }
        });
    </script>
</body>
</html>
"""

ACCESS_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HeartKiller - Access Room</title>
    <style>
        :root {
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --accent: #ef4444;
            --accent-hover: #dc2626;
            --text: #f8fafc;
            --text-muted: #94a3b8;
            --border: #334155;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            color: var(--text);
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 90vh;
        }
        .container {
            width: 100%;
            max-width: 400px;
            background: var(--card-bg);
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
            border: 1px solid var(--border);
            box-sizing: border-box;
        }
        h2 { color: var(--accent); text-align: center; margin-top: 0; }
        input, button {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            border-radius: 8px;
            border: 1px solid var(--border);
            background: #0f172a;
            color: var(--text);
            font-size: 16px;
            box-sizing: border-box;
        }
        button { background: var(--accent); border: none; font-weight: bold; cursor: pointer; }
        button:hover { background: var(--accent-hover); }
        .alert {
            background: rgba(239, 68, 68, 0.2);
            border: 1px solid var(--accent);
            padding: 10px;
            border-radius: 6px;
            color: #fca5a5;
            margin-bottom: 15px;
            text-align: center;
            font-size: 14px;
        }
        .center { text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <h2>📥 Access Room</h2>
        <p class="center" style="color: var(--text-muted); font-size: 13px;">Enter Number or Access Token to Recover & Download</p>
        
        {% if error %}
            <div class="alert">{{ error }}</div>
        {% endif %}

        <form method="POST" action="/access-room">
            <input type="text" name="room_code" placeholder="Enter Number or Access Token..." required>
            <button type="submit">Open Dashboard</button>
        </form>

        <div class="center" style="margin-top: 15px;">
            <a href="/" style="color: var(--text-muted); text-decoration: none; font-size: 14px;">← Back to Home</a>
        </div>
    </div>
</body>
</html>
"""

ROOM_DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Room Dashboard - {{ room_code }}</title>
    <style>
        :root {
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --accent: #ef4444;
            --accent-hover: #dc2626;
            --text: #f8fafc;
            --text-muted: #94a3b8;
            --border: #334155;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            color: var(--text);
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .container {
            width: 100%;
            max-width: 500px;
            background: var(--card-bg);
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
            border: 1px solid var(--border);
            box-sizing: border-box;
        }
        h2, h3 { color: var(--accent); text-align: center; margin-top: 0; }
        .badge {
            background: var(--accent);
            color: white;
            padding: 6px 16px;
            border-radius: 20px;
            font-weight: bold;
            display: inline-block;
            word-break: break-all;
            font-size: 16px;
            text-align: center;
        }
        .file-item {
            background: #0f172a;
            padding: 12px;
            margin: 10px 0;
            border-radius: 8px;
            border: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .file-info {
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            margin-right: 10px;
            font-size: 14px;
            max-width: 300px;
        }
        .download-btn {
            background: #10b981;
            padding: 6px 12px;
            font-size: 14px;
            width: auto;
            margin: 0;
            text-decoration: none;
            color: white;
            border-radius: 6px;
            display: inline-block;
        }
        .download-btn:hover { background: #059669; }
        button {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            border-radius: 8px;
            border: none;
            background: #3b82f6;
            color: white;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
        }
        button:hover { background: #2563eb; }
        .center { text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🔥 Room Dashboard</h2>
        <div class="center" style="margin-bottom: 20px;">
            <p style="margin: 5px 0; color: var(--text-muted);">Active Key / Room Code:</p>
            <div class="badge">{{ room_code }}</div>
        </div>

        <h3>📥 Uploaded Files</h3>
        <div id="file-list">
            {% if files %}
                {% for f in files %}
                <div class="file-item">
                    <div class="file-info" title="{{ f.filename }}">📁 {{ f.filename }}</div>
                    <a href="/download/{{ room_code }}/{{ f.id }}" class="download-btn">Download</a>
                </div>
                {% endfor %}
            {% else %}
                <p class="center" style="color: var(--text-muted); font-size: 14px;">No files found or expired in this room.</p>
            {% endif %}
        </div>

        <div style="margin-top: 20px; display: flex; gap: 10px; flex-direction: column;">
            <button onclick="location.reload()">Refresh Real-Time List</button>
            <a href="/access" style="text-decoration: none;"><button style="background: #475569;">Switch / Exit Room</button></a>
        </div>
    </div>
</body>
</html>
"""

# --- FLASK ROUTES ---

@app.route('/')
def index():
    return render_template_string(HOME_TEMPLATE)

@app.route('/upload')
def upload_page():
    return render_template_string(UPLOAD_TEMPLATE)

@app.route('/access')
def access_page():
    error = request.args.get('error')
    return render_template_string(ACCESS_TEMPLATE, error=error)

@app.route('/access-room', methods=['POST'])
def access_room():
    room_code = request.form.get('room_code', '').strip()
    if not room_code:
        return redirect(url_for('access_page', error="Please enter a valid number or access token!"))
    return redirect(url_for('room_dashboard', room_code=room_code))

@app.route('/room/<room_code>')
def room_dashboard(room_code):
    files = ROOMS.get(room_code, [])
    return render_template_string(ROOM_DASHBOARD_TEMPLATE, room_code=room_code, files=files)

@app.route('/upload-endpoint', methods=['POST'])
def upload_endpoint():
    room_code = request.form.get('room_code', '').strip()
    if not room_code:
        return jsonify({"error": "Room code or token is required!"}), 400

    uploaded_files = request.files.getlist('files')
    if not uploaded_files or len(uploaded_files) == 0:
        return jsonify({"error": "No files received."}), 400

    if room_code not in ROOMS:
        ROOMS[room_code] = []

    count = 0
    for file in uploaded_files:
        if file and file.filename:
            filename = file.filename.replace('/', '_').replace('\\', '_')
            file_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            
            # Safe filename for storage
            safe_prefix = "".join([c if c.isalnum() else "_" for c in room_code])
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{safe_prefix}_{file_id}_{filename}")
            file.save(save_path)
            
            ROOMS[room_code].append({
                "id": file_id,
                "filename": filename,
                "filepath": save_path
            })
            count += 1

    # Save to JSON metadata file for auto-recovery on restart
    save_rooms()

    return jsonify({"message": f"Successfully uploaded {count} file(s)!"}), 200

@app.route('/download/<room_code>/<file_id>')
def download_file(room_code, file_id):
    files = ROOMS.get(room_code, [])
    for f in files:
        if f['id'] == file_id:
            directory = os.path.dirname(f['filepath'])
            filename = os.path.basename(f['filepath'])
            return send_from_directory(directory, filename, as_attachment=True, download_name=f['filename'])
    
    return "File not found", 404

if __name__ == '__main__':
    print("\n" + "="*50)
    print(" [🔥] HEARTKILLER CLOUD VAULT WITH AUTO-RECOVERY STARTED!")
    print(f" [🌐] RUNNING LOCALLY : http://127.0.0.1:5000")
    print("="*50 + "\n")
    app.run(host='0.0.0.0', port=5000, debug=False)
