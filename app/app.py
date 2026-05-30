from flask import Flask, jsonify, render_template_string
import os
import socket
from datetime import datetime

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DevOps Demo App</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }
        .card {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px 50px;
            max-width: 600px;
            width: 90%;
            border: 1px solid rgba(255,255,255,0.2);
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        .badge {
            display: inline-block;
            background: #00d4aa;
            color: #000;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 700;
            margin-bottom: 20px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        h1 { font-size: 2rem; margin-bottom: 10px; }
        .subtitle { color: rgba(255,255,255,0.6); margin-bottom: 30px; font-size: 0.95rem; }
        .info-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-top: 20px;
        }
        .info-item {
            background: rgba(0,0,0,0.2);
            border-radius: 10px;
            padding: 15px;
        }
        .info-label { font-size: 11px; color: #00d4aa; text-transform: uppercase; letter-spacing: 1px; }
        .info-value { font-size: 14px; margin-top: 5px; word-break: break-all; }
        .status-dot {
            display: inline-block;
            width: 10px;
            height: 10px;
            background: #00d4aa;
            border-radius: 50%;
            margin-right: 8px;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.4; }
        }
        .endpoint {
            margin-top: 25px;
            padding: 15px;
            background: rgba(0,0,0,0.2);
            border-radius: 10px;
            font-size: 13px;
            color: rgba(255,255,255,0.7);
        }
        .endpoint code {
            color: #00d4aa;
            background: rgba(0,212,170,0.1);
            padding: 2px 6px;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="card">
        <div class="badge">&#x2713; Running</div>
        <h1>DevOps Demo App</h1>
        <p class="subtitle">Aplicación containerizada desplegada con CI/CD en AWS</p>

        <div>
            <span class="status-dot"></span>
            <span>Sistema operacional</span>
        </div>

        <div class="info-grid">
            <div class="info-item">
                <div class="info-label">Hostname (Container)</div>
                <div class="info-value">{{ hostname }}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Versión</div>
                <div class="info-value">{{ version }}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Ambiente</div>
                <div class="info-value">{{ environment }}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Timestamp</div>
                <div class="info-value">{{ timestamp }}</div>
            </div>
        </div>

        <div class="endpoint">
            Endpoints disponibles:<br>
            <code>GET /</code> — Esta página<br>
            <code>GET /health</code> — Health check<br>
            <code>GET /api/info</code> — Info del sistema (JSON)
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE,
        hostname=socket.gethostname(),
        version=os.environ.get('APP_VERSION', '1.0.0'),
        environment=os.environ.get('ENVIRONMENT', 'production'),
        timestamp=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    )

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "hostname": socket.gethostname()
    }), 200

@app.route('/api/info')
def info():
    return jsonify({
        "app": "DevOps Demo App",
        "version": os.environ.get('APP_VERSION', '1.0.0'),
        "environment": os.environ.get('ENVIRONMENT', 'production'),
        "hostname": socket.gethostname(),
        "timestamp": datetime.utcnow().isoformat()
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
