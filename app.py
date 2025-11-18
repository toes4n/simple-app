from flask import Flask, render_template_string, jsonify
import os
import socket
import datetime

app = Flask(__name__)

VERSION = os.getenv('APP_VERSION', '1.0.0')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DevOps Learning App</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes slideIn {
            from { transform: translateX(-100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
            color: #333;
            min-height: 100vh;
        }
        
        nav {
            background: rgba(255, 255, 255, 0.95);
            padding: 1rem 2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
            animation: slideIn 0.6s ease-out;
        }
        
        nav ul {
            list-style: none;
            display: flex;
            gap: 1.5rem;
            align-items: center;
            flex-wrap: wrap;
        }
        
        nav a {
            text-decoration: none;
            color: #667eea;
            font-weight: 600;
            transition: all 0.3s ease;
            position: relative;
        }
        
        nav a::after {
            content: '';
            position: absolute;
            bottom: -5px;
            left: 0;
            width: 0;
            height: 2px;
            background: #667eea;
            transition: width 0.3s ease;
        }
        
        nav a:hover::after {
            width: 100%;
        }
        
        nav a:hover {
            color: #764ba2;
            transform: translateY(-2px);
        }
        
        .badge {
            display: inline-block;
            padding: 0.3rem 0.8rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 20px;
            font-size: 0.85rem;
            margin-left: auto;
            animation: pulse 2s ease-in-out infinite;
        }
        
        .container {
            max-width: 1400px;
            margin: 2rem auto;
            padding: 2rem;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            animation: fadeIn 0.8s ease-out;
            backdrop-filter: blur(10px);
        }
        
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin-top: 2rem;
        }
        
        .card {
            padding: 2rem;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            text-align: center;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            animation: fadeIn 0.6s ease-out backwards;
        }
        
        .card:nth-child(1) { animation-delay: 0.1s; }
        .card:nth-child(2) { animation-delay: 0.2s; }
        .card:nth-child(3) { animation-delay: 0.3s; }
        .card:nth-child(4) { animation-delay: 0.4s; }
        
        .card:hover {
            transform: translateY(-10px) scale(1.02);
            box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
        }
        
        .card h3 { margin: 1rem 0 0.5rem 0; color: #333; }
        .card p { color: #666; }
        .icon {
            font-size: 3rem;
            animation: float 3s ease-in-out infinite;
        }
        
        .concept-card {
            padding: 2rem;
            background: linear-gradient(135deg, #f8f9fa 0%, #fff 100%);
            border-left: 5px solid #667eea;
            border-radius: 10px;
            margin-bottom: 1.5rem;
            transition: all 0.3s ease;
            animation: fadeIn 0.6s ease-out backwards;
        }
        
        .concept-card:hover {
            transform: translateX(5px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
        }
        
        .concept-card h2 { color: #667eea; margin-bottom: 1rem; }
        .concept-card h3 { color: #555; margin: 1.5rem 0 1rem 0; }
        .concept-card p, .concept-card li { color: #666; line-height: 1.8; }
        .concept-card ul { margin: 1rem 0 1rem 2rem; }
        
        .tools {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
            margin-top: 1rem;
        }
        
        .tool-badge {
            padding: 0.4rem 1rem;
            background: white;
            border: 2px solid #667eea;
            border-radius: 20px;
            color: #667eea;
            font-weight: 600;
            font-size: 0.9rem;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .tool-badge:hover {
            background: #667eea;
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }
        
        .architecture-diagram {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 2rem;
            border-radius: 15px;
            margin: 2rem 0;
            text-align: center;
            animation: fadeIn 0.8s ease-out;
        }
        
        .component-box {
            display: inline-block;
            padding: 1rem 1.5rem;
            margin: 0.5rem;
            background: white;
            border: 2px solid #667eea;
            border-radius: 10px;
            font-weight: 600;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .component-box:hover {
            transform: scale(1.05) rotate(-2deg);
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        }
        
        .link-button {
            display: inline-block;
            padding: 0.8rem 1.5rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 25px;
            margin: 0.5rem;
            transition: all 0.3s ease;
            font-weight: 600;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }
        
        .link-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
            animation: fadeIn 0.8s ease-out;
        }
        
        th, td {
            padding: 1rem;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        
        th {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-weight: 600;
        }
        
        tr {
            transition: all 0.3s ease;
        }
        
        tbody tr:hover {
            background: #f8f9fa;
            transform: scale(1.01);
        }
        
        .hero {
            text-align: center;
            padding: 3rem 0;
            animation: fadeIn 1s ease-out;
        }
        
        .hero h1 {
            font-size: 3rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 1rem;
        }
        
        .hero p {
            font-size: 1.3rem;
            color: #666;
            margin-bottom: 2rem;
        }
        
        .highlight {
            margin-top: 3rem;
            padding: 2rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 15px;
        }
        
        .highlight h2 { margin-bottom: 1rem; }
        .highlight ul {
            text-align: left;
            margin: 1.5rem auto;
            max-width: 600px;
            line-height: 2;
        }
        
        code {
            background: #2d2d2d;
            padding: 0.2rem 0.6rem;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            color: #f8f8f2;
            font-size: 0.9em;
        }
        
        pre {
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 1.5rem;
            border-radius: 10px;
            overflow-x: auto;
            margin: 1rem 0;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        pre code {
            background: transparent;
            color: #f8f8f2;
            padding: 0;
        }
    </style>
</head>
<body>
    <nav>
        <ul>
            <li><a href="/">🏠 Home</a></li>
            <li><a href="/devops-concepts">📚 DevOps</a></li>
            <li><a href="/kubernetes">☸️ Kubernetes</a></li>
            <li><a href="/ingress-gateway">🚪 Ingress & Gateway</a></li>
            <li><a href="/kong">🦍 Kong</a></li>
            <li><a href="/alibaba-ack">☁️ Alibaba ACK</a></li>
            <li><a href="/info">ℹ️ Info</a></li>
            <li class="badge">v{{ version }} | {{ environment }}</li>
        </ul>
    </nav>
    <div class="container">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
"""

HOME_PAGE = """
<div class="hero">
    <h1>🐈 Welcome SRE Team KT Kitty Lay Myr Session</h1>
    <p>Learn DevOps, Kubernetes, and Cloud-Native Concepts</p>
    
    <div class="grid">
        <div class="card">
            <div class="icon">☸️</div>
            <h3>Kubernetes</h3>
            <p>Architecture & Components</p>
        </div>
        
        <div class="card">
            <div class="icon">🚪</div>
            <h3>Ingress & Gateway</h3>
            <p>Traffic Management</p>
        </div>
        
        <div class="card">
            <div class="icon">🦍</div>
            <h3>Kong Gateway</h3>
            <p>API Gateway & Ingress</p>
        </div>
        
        <div class="card">
            <div class="icon">☁️</div>
            <h3>Alibaba ACK</h3>
            <p>Managed Kubernetes</p>
        </div>
    </div>
    
    <div class="highlight">
        <h2>🎯 This Application Demonstrates:</h2>
        <ul>
            <li>✅ Multi-platform Docker builds (AMD64/ARM64)</li>
            <li>✅ Kubernetes deployment with HPA</li>
            <li>✅ ArgoCD GitOps workflow</li>
            <li>✅ GitHub Actions CI/CD</li>
            <li>✅ Kong Ingress Controller integration</li>
            <li>✅ Gateway API with HTTPRoute</li>
        </ul>
    </div>
</div>
"""

KONG_PAGE = """
<h1 style="color: #667eea; margin-bottom: 2rem; text-align: center;">🦍 Kong Gateway & Ingress Controller</h1>

<div class="concept-card">
    <h2>📖 What is Kong Gateway?</h2>
    <p>Kong Gateway is a lightweight, fast, and flexible cloud-native API gateway optimized for microservices and distributed architectures. It runs in front of any RESTful API and can be extended through plugins.</p>
    
    <h3>Key Features</h3>
    <ul>
        <li>🚀 High-performance API gateway with low latency</li>
        <li>🔌 60+ plugins for authentication, security, and traffic control</li>
        <li>☸️ Native Kubernetes Ingress Controller support</li>
        <li>🌐 Multi-cloud and hybrid deployment support</li>
        <li>🔐 Enterprise-grade security and authentication</li>
    </ul>
</div>

<div class="concept-card">
    <h2>📝 Kong Ingress Example</h2>
    <pre><code>
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: flask-ingress
  annotations:
    konghq.com/strip-path: "true"
    konghq.com/plugins: rate-limiting
spec:
  ingressClassName: kong
  rules:
  - host: flask.example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: flask-service
            port:
              number: 5000</code></pre>
</div>

<div class="concept-card">
    <h2>🔗 Official Resources</h2>
    <div style="margin-top: 1rem;">
        <a href="https://docs.konghq.com/" target="_blank" class="link-button">Kong Documentation</a>
        <a href="https://github.com/Kong/kubernetes-ingress-controller" target="_blank" class="link-button">Kong Ingress GitHub</a>
    </div>
</div>
"""

# Routes
@app.route('/')
def home():
    html = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', HOME_PAGE)
    return render_template_string(html, version=VERSION, environment=ENVIRONMENT)

@app.route('/kong')
def kong():
    html = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', KONG_PAGE)
    return render_template_string(html, version=VERSION, environment=ENVIRONMENT)

@app.route('/devops-concepts')
def devops():
    return render_template_string(BASE_TEMPLATE.replace('{% block content %}{% endblock %}', '<h1 style="text-align:center;">📚 DevOps Concepts Coming Soon!</h1>'), version=VERSION, environment=ENVIRONMENT)

@app.route('/kubernetes')
def kubernetes():
    return render_template_string(BASE_TEMPLATE.replace('{% block content %}{% endblock %}', '<h1 style="text-align:center;">☸️ Kubernetes Coming Soon!</h1>'), version=VERSION, environment=ENVIRONMENT)

@app.route('/ingress-gateway')
def ingress():
    return render_template_string(BASE_TEMPLATE.replace('{% block content %}{% endblock %}', '<h1 style="text-align:center;">🚪 Ingress & Gateway Coming Soon!</h1>'), version=VERSION, environment=ENVIRONMENT)

@app.route('/alibaba-ack')
def ack():
    return render_template_string(BASE_TEMPLATE.replace('{% block content %}{% endblock %}', '<h1 style="text-align:center;">☁️ Alibaba ACK Coming Soon!</h1>'), version=VERSION, environment=ENVIRONMENT)

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat(),
        'version': VERSION,
        'hostname': socket.gethostname()
    }), 200

@app.route('/info')
def info():
    deployment_info = {
        'hostname': socket.gethostname(),
        'version': VERSION,
        'environment': ENVIRONMENT,
        'platform': os.uname().sysname,
        'architecture': os.uname().machine,
        'python_version': os.sys.version.split()[0],
        'timestamp': datetime.datetime.now().isoformat()
    }
    
    info_html = f"""
    <h1 style="color: #667eea; margin-bottom: 2rem; text-align: center;">ℹ️ Deployment Information</h1>
    <div style="background: #f8f9fa; padding: 2rem; border-radius: 10px;">
        <table>
            {''.join([f'<tr><td style="font-weight: 600; color: #667eea;">{key.replace("_", " ").title()}</td><td>{value}</td></tr>' for key, value in deployment_info.items()])}
        </table>
    </div>
    <div style="margin-top: 2rem; padding: 1.5rem; background: #e8f5e9; border-left: 5px solid #4caf50; border-radius: 5px;">
        <strong style="color: #2e7d32;">✅ Status:</strong> Application is running successfully!
    </div>
    """
    
    html = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', info_html)
    return render_template_string(html, version=VERSION, environment=ENVIRONMENT)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
