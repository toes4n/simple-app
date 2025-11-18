from flask import Flask, render_template_string, jsonify
import os
import socket
import datetime

app = Flask(__name__)

# Get environment variables for deployment info
VERSION = os.getenv('APP_VERSION', '1.0.0')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

# Base HTML template
BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DevOps Learning App</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
        }
        nav {
            background: rgba(255, 255, 255, 0.95);
            padding: 1rem 2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        nav ul {
            list-style: none;
            display: flex;
            gap: 2rem;
            align-items: center;
            flex-wrap: wrap;
        }
        nav a {
            text-decoration: none;
            color: #667eea;
            font-weight: 600;
            transition: color 0.3s;
        }
        nav a:hover { color: #764ba2; }
        .badge {
            display: inline-block;
            padding: 0.3rem 0.8rem;
            background: #667eea;
            color: white;
            border-radius: 20px;
            font-size: 0.85rem;
            margin-left: auto;
        }
        .container {
            max-width: 1200px;
            margin: 2rem auto;
            padding: 2rem;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin-top: 2rem;
        }
        .card {
            padding: 2rem;
            background: #f8f9fa;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }
        .card h3 { margin: 1rem 0 0.5rem 0; color: #333; }
        .card p { color: #666; }
        .icon { font-size: 3rem; }
        .concept-card {
            padding: 2rem;
            background: #f8f9fa;
            border-left: 5px solid #667eea;
            border-radius: 5px;
            margin-bottom: 1.5rem;
        }
        .concept-card h2 { color: #667eea; margin-bottom: 1rem; }
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
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 1rem;
        }
        tr { border-bottom: 1px solid #ddd; }
        td {
            padding: 1rem;
        }
        td:first-child {
            font-weight: 600;
            color: #667eea;
            text-transform: capitalize;
        }
        .hero {
            text-align: center;
            padding: 3rem 0;
        }
        .hero h1 {
            font-size: 3rem;
            color: #667eea;
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
            border-radius: 10px;
        }
        .highlight h2 { margin-bottom: 1rem; }
        .highlight ul {
            text-align: left;
            margin: 1.5rem auto;
            max-width: 600px;
            line-height: 2;
        }
    </style>
</head>
<body>
    <nav>
        <ul>
            <li><a href="/">🏠 Home</a></li>
            <li><a href="/devops-concepts">📚 DevOps Concepts</a></li>
            <li><a href="/info">ℹ️ Deployment Info</a></li>
            <li><a href="/health">❤️ Health</a></li>
            <li class="badge">v{{ version }} | {{ environment }}</li>
        </ul>
    </nav>
    <div class="container">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
"""

HOME_PAGE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
<div class="hero">
    <h1>🚀 Welcome to DevOps Learning Platform</h1>
    <p>Learn DevOps Concepts Through Hands-On Practice</p>
    
    <div class="grid">
        <div class="card">
            <div class="icon">☸️</div>
            <h3>Kubernetes Deployed</h3>
            <p>Running on K8s cluster</p>
        </div>
        
        <div class="card">
            <div class="icon">📦</div>
            <h3>Containerized</h3>
            <p>Docker multi-platform image</p>
        </div>
        
        <div class="card">
            <div class="icon">🔄</div>
            <h3>GitOps Ready</h3>
            <p>Deployed via ArgoCD</p>
        </div>
        
        <div class="card">
            <div class="icon">⚡</div>
            <h3>CI/CD Pipeline</h3>
            <p>GitHub Actions automated</p>
        </div>
    </div>
    
    <div class="highlight">
        <h2>🎯 This Application Demonstrates:</h2>
        <ul>
            <li>✅ Multi-platform Docker builds (AMD64/ARM64)</li>
            <li>✅ Kubernetes deployment with HPA</li>
            <li>✅ ArgoCD GitOps workflow</li>
            <li>✅ GitHub Actions CI/CD</li>
            <li>✅ Health checks and monitoring endpoints</li>
            <li>✅ Container registry integration (GHCR)</li>
        </ul>
    </div>
</div>
""")

CONCEPTS_PAGE = """
<h1 style="color: #667eea; margin-bottom: 2rem; text-align: center;">📚 DevOps Concepts & Tools</h1>

<div class="concept-card">
    <h2>🔄 CI/CD</h2>
    <p style="color: #666; font-size: 1.1rem;">Continuous Integration & Continuous Deployment</p>
    <div class="tools">
        <span class="tool-badge">GitHub Actions</span>
        <span class="tool-badge">Jenkins</span>
        <span class="tool-badge">GitLab CI</span>
        <span class="tool-badge">ArgoCD</span>
    </div>
</div>

<div class="concept-card">
    <h2>📦 Containerization</h2>
    <p style="color: #666; font-size: 1.1rem;">Package applications with dependencies</p>
    <div class="tools">
        <span class="tool-badge">Docker</span>
        <span class="tool-badge">Podman</span>
        <span class="tool-badge">Buildah</span>
    </div>
</div>

<div class="concept-card">
    <h2>☸️ Orchestration</h2>
    <p style="color: #666; font-size: 1.1rem;">Manage containerized applications at scale</p>
    <div class="tools">
        <span class="tool-badge">Kubernetes</span>
        <span class="tool-badge">Docker Swarm</span>
        <span class="tool-badge">Nomad</span>
    </div>
</div>

<div class="concept-card">
    <h2>🏗️ Infrastructure as Code</h2>
    <p style="color: #666; font-size: 1.1rem;">Manage infrastructure through code</p>
    <div class="tools">
        <span class="tool-badge">Terraform</span>
        <span class="tool-badge">Ansible</span>
        <span class="tool-badge">Pulumi</span>
    </div>
</div>

<div class="concept-card">
    <h2>📊 Monitoring</h2>
    <p style="color: #666; font-size: 1.1rem;">Observe system health and performance</p>
    <div class="tools">
        <span class="tool-badge">Prometheus</span>
        <span class="tool-badge">Grafana</span>
        <span class="tool-badge">ELK Stack</span>
    </div>
</div>

<div class="concept-card">
    <h2>🔀 GitOps</h2>
    <p style="color: #666; font-size: 1.1rem;">Git as the single source of truth</p>
    <div class="tools">
        <span class="tool-badge">ArgoCD</span>
        <span class="tool-badge">Flux</span>
        <span class="tool-badge">Rancher Fleet</span>
    </div>
</div>
"""

@app.route('/')
def home():
    """Main landing page"""
    return render_template_string(HOME_PAGE, version=VERSION, environment=ENVIRONMENT)

@app.route('/health')
def health():
    """Health check endpoint for Kubernetes"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat(),
        'version': VERSION,
        'hostname': socket.gethostname()
    }), 200

@app.route('/info')
def info():
    """Display deployment information"""
    deployment_info = {
        'hostname': socket.gethostname(),
        'version': VERSION,
        'environment': ENVIRONMENT,
        'platform': os.uname().sysname,
        'architecture': os.uname().machine,
        'python_version': os.sys.version.split()[0],
        'timestamp': datetime.datetime.now().isoformat()
    }
    
    info_html = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', f"""
    <h1 style="color: #667eea; margin-bottom: 2rem; text-align: center;">ℹ️ Deployment Information</h1>
    <div style="background: #f8f9fa; padding: 2rem; border-radius: 10px;">
        <table>
            {''.join([f'<tr><td>{key.replace("_", " ")}</td><td>{value}</td></tr>' for key, value in deployment_info.items()])}
        </table>
    </div>
    <div style="margin-top: 2rem; padding: 1.5rem; background: #e8f5e9; border-left: 5px solid #4caf50; border-radius: 5px;">
        <strong style="color: #2e7d32;">✅ Status:</strong> Application is running successfully!
    </div>
    """)
    
    return render_template_string(info_html, version=VERSION, environment=ENVIRONMENT)

@app.route('/devops-concepts')
def devops_concepts():
    """Display DevOps concepts and tools"""
    concepts_html = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', CONCEPTS_PAGE)
    return render_template_string(concepts_html, version=VERSION, environment=ENVIRONMENT)

@app.route('/api/metrics')
def metrics():
    """Expose metrics for monitoring"""
    return jsonify({
        'requests_total': 100,
        'uptime_seconds': 3600,
        'memory_usage_mb': 128,
        'cpu_usage_percent': 5.2
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
