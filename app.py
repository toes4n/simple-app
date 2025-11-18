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
        
        tr:hover {
            background: #f8f9fa;
            transform: scale(1.01);
        }
        
        .comparison-table td:first-child {
            font-weight: 600;
            color: #667eea;
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
            animation: fadeIn 1.2s ease-out;
        }
        
        .hero p {
            font-size: 1.3rem;
            color: #666;
            margin-bottom: 2rem;
            animation: fadeIn 1.4s ease-out;
        }
        
        .highlight {
            margin-top: 3rem;
            padding: 2rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 15px;
            animation: fadeIn 1.6s ease-out;
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
            animation: fadeIn 0.8s ease-out;
        }
        
        pre code {
            background: transparent;
            color: #f8f8f2;
            padding: 0;
        }
        
        .kong-logo {
            display: inline-block;
            font-size: 2.5rem;
            animation: pulse 2s ease-in-out infinite;
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

HOME_PAGE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
<div class="hero">
    <h1>🦸🏻‍♂️ Welcome to SRE KT Kitty Session 🤪</h1>
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
""")

KONG_PAGE = """
<h1 style="color: #667eea; margin-bottom: 2rem; text-align: center;"><span class="kong-logo">🦍</span> Kong Gateway & Ingress Controller</h1>

<div class="concept-card">
    <h2>📖 What is Kong Gateway?</h2>
    <p>Kong Gateway is a lightweight, fast, and flexible cloud-native API gateway built for hybrid and multi-cloud environments, optimized for microservices and distributed architectures. It runs in front of any RESTful API and can be extended through modules and plugins.</p>
    
    <h3>Key Features</h3>
    <ul>
        <li>🚀 High-performance API gateway with low latency</li>
        <li>🔌 60+ plugins for authentication, security, traffic control, and more</li>
        <li>🤖 Advanced AI Gateway capabilities for LLM and MCP traffic</li>
        <li>☸️ Native Kubernetes Ingress Controller support</li>
        <li>🌐 Multi-cloud and hybrid deployment support</li>
        <li>📊 Real-time analytics and monitoring</li>
        <li>🔐 Enterprise-grade security and authentication</li>
    </ul>
</div>

<div class="concept-card">
    <h2>☸️ Kong Ingress Controller (KIC)</h2>
    <p>Kong Ingress Controller allows you to run Kong Gateway as a Kubernetes Ingress to handle inbound requests for a Kubernetes cluster. It takes Kubernetes resources such as <code>Ingress</code> and <code>HTTPRoute</code> and converts them into valid Kong Gateway configuration.</p>
    
    <h3>Why Use Kong Ingress Controller?</h3>
    <ul>
        <li><strong>Kubernetes-native</strong>: Configure Kong Gateway using Kubernetes CRDs</li>
        <li><strong>Rich functionality</strong>: Access all Kong Gateway features through Kubernetes resources</li>
        <li><strong>Protocol support</strong>: HTTP, HTTPS, gRPC, TCP, and UDP</li>
        <li><strong>Advanced routing</strong>: Path-based, header-based, and method-based routing</li>
        <li><strong>Plugin system</strong>: Apply Kong plugins at ingress, service, or route level</li>
        <li><strong>Service mesh integration</strong>: Works with Istio and other service meshes</li>
    </ul>
</div>

<div class="architecture-diagram">
    <h3 style="color: #667eea; margin-bottom: 1.5rem;">Kong Ingress Controller Architecture</h3>
    <div style="margin: 2rem 0; text-align: center;">
        <div style="background: #fff3e0; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
            <strong style="color: #e65100;">🌐 External Traffic (Internet)</strong>
        </div>
        <div style="font-size: 2rem;">⬇️</div>
        <div style="background: #e1f5fe; padding: 1.5rem; border-radius: 8px; margin: 1rem 0;">
            <strong style="color: #01579b;">Kong Gateway (Data Plane)</strong><br><br>
            <div class="component-box" style="border-color: #01579b;">Load Balancer</div>
            <div class="component-box" style="border-color: #01579b;">Plugins</div>
            <div class="component-box" style="border-color: #01579b;">Routing Engine</div>
        </div>
        <div style="font-size: 2rem;">⬅️ Configures ➡️</div>
        <div style="background: #f3e5f5; padding: 1.5rem; border-radius: 8px; margin: 1rem 0;">
            <strong style="color: #4a148c;">Kong Ingress Controller</strong><br><br>
            <div class="component-box" style="border-color: #4a148c;">Watches K8s API</div>
            <div class="component-box" style="border-color: #4a148c;">Converts CRDs</div>
        </div>
        <div style="font-size: 2rem;">⬇️</div>
        <div style="background: #e8f5e9; padding: 1.5rem; border-radius: 8px; margin: 1rem 0;">
            <strong style="color: #1b5e20;">Kubernetes Services & Pods</strong><br><br>
            <div class="component-box" style="border-color: #1b5e20;">Service A</div>
            <div class="component-box" style="border-color: #1b5e20;">Service B</div>
            <div class="component-box" style="border-color: #1b5e20;">Service C</div>
        </div>
    </div>
</div>

<div class="concept-card">
    <h2>📝 Kong Ingress Resource Example</h2>
    <p>Standard Kubernetes Ingress with Kong-specific annotations:</p>
    <pre><code>
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: flask-ingress
  annotations:
    konghq.com/strip-path: "true"
    konghq.com/plugins: rate-limiting, cors
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
    <h2>🚀 Kong Gateway API Support</h2>
    <p>Kong supports the modern Kubernetes Gateway API for more expressive traffic management:</p>
    
    <h3>Gateway Resource</h3>
    <pre><code>
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: kong-gateway
spec:
  gatewayClassName: kong
  listeners:
  - name: http
    protocol: HTTP
    port: 80
  - name: https
    protocol: HTTPS
    port: 443
    tls:
      mode: Terminate
      certificateRefs:
      - name: flask-tls-cert</code></pre>
    
    <h3>HTTPRoute with Kong</h3>
    <pre><code>
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: flask-route
  annotations:
    konghq.com/plugins: rate-limiting, key-auth
spec:
  parentRefs:
  - name: kong-gateway
  hostnames:
  - "flask.example.com"
  rules:
  - matches:
    - path:
        type: PathPrefix
        value: /api/v1
    backendRefs:
    - name: flask-service
      port: 5000
      weight: 90
    - name: flask-service-canary
      port: 5000
      weight: 10  # 10% canary traffic
    filters:
    - type: RequestHeaderModifier
      requestHeaderModifier:
        add:
        - name: X-Kong-Route
          value: "production"</code></pre>
</div>

<div class="concept-card">
    <h2>🔌 Kong Plugins</h2>
    <p>Kong's plugin architecture provides powerful functionality:</p>
    
    <h3>Popular Plugins</h3>
    <table>
        <tr>
            <th>Category</th>
            <th>Plugin</th>
            <th>Purpose</th>
        </tr>
        <tr>
            <td>🔐 Authentication</td>
            <td>key-auth, jwt, oauth2, basic-auth</td>
            <td>Secure API access</td>
        </tr>
        <tr>
            <td>🚦 Traffic Control</td>
            <td>rate-limiting, request-size-limiting, response-ratelimiting</td>
            <td>Control API usage</td>
        </tr>
        <tr>
            <td>🔄 Transformation</td>
            <td>request-transformer, response-transformer</td>
            <td>Modify requests/responses</td>
        </tr>
        <tr>
            <td>📊 Analytics</td>
            <td>prometheus, datadog, zipkin</td>
            <td>Monitor and trace</td>
        </tr>
        <tr>
            <td>🛡️ Security</td>
            <td>cors, ip-restriction, bot-detection</td>
            <td>Protect APIs</td>
        </tr>
        <tr>
            <td>⚡ Performance</td>
            <td>proxy-cache, gzip</td>
            <td>Optimize performance</td>
        </tr>
    </table>
    
    <h3>Applying Plugins with CRDs</h3>
    <pre><code>
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: rate-limiting
config:
  minute: 100
  hour: 10000
  policy: local
plugin: rate-limiting
---
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: cors
config:
  origins:
  - "*"
  methods:
  - GET
  - POST
  headers:
  - Accept
  - Authorization
  exposed_headers:
  - X-Auth-Token
  credentials: true
  max_age: 3600
plugin: cors</code></pre>
</div>

<div class="concept-card">
    <h2>⚙️ Kong Deployment Models</h2>
    
    <h3>1. DB-less Mode (Declarative)</h3>
    <ul>
        <li>No database required</li>
        <li>Configuration via declarative YAML files</li>
        <li>Perfect for Kubernetes with GitOps</li>
        <li>Lower operational complexity</li>
    </ul>
    
    <h3>2. Database Mode (PostgreSQL)</h3>
    <ul>
        <li>Uses PostgreSQL for configuration storage</li>
        <li>Supports Admin API for dynamic configuration</li>
        <li>Better for dynamic environments</li>
        <li>Enables Kong Manager UI</li>
    </ul>
    
    <h3>3. Hybrid Mode (Control/Data Plane Separation)</h3>
    <ul>
        <li>Control Plane manages configuration</li>
        <li>Data Planes handle traffic</li>
        <li>Ideal for multi-region deployments</li>
        <li>Enhanced security and scalability</li>
    </ul>
</div>

<div class="concept-card">
    <h2>🎯 Kong vs Other Ingress Controllers</h2>
    <table class="comparison-table">
        <tr>
            <th>Feature</th>
            <th>Kong</th>
            <th>NGINX</th>
            <th>Traefik</th>
        </tr>
        <tr>
            <td>Plugin Ecosystem</td>
            <td>60+ plugins, extensible</td>
            <td>Limited, module-based</td>
            <td>Middleware system</td>
        </tr>
        <tr>
            <td>API Gateway Features</td>
            <td>Full-featured API gateway</td>
            <td>Basic ingress functionality</td>
            <td>Good ingress features</td>
        </tr>
        <tr>
            <td>Gateway API Support</td>
            <td>Full support</td>
            <td>Partial support</td>
            <td>Full support</td>
        </tr>
        <tr>
            <td>Performance</td>
            <td>High (OpenResty/LuaJIT)</td>
            <td>Very High</td>
            <td>High (Go-based)</td>
        </tr>
        <tr>
            <td>AI/LLM Gateway</td>
            <td>Native support</td>
            <td>Not available</td>
            <td>Not available</td>
        </tr>
        <tr>
            <td>Management UI</td>
            <td>Kong Manager</td>
            <td>Third-party only</td>
            <td>Dashboard available</td>
        </tr>
    </table>
</div>

<div class="concept-card">
    <h2>💡 Kong Best Practices</h2>
    <ul>
        <li>Use DB-less mode with Kubernetes for GitOps workflows</li>
        <li>Apply plugins at the appropriate level (global, service, route)</li>
        <li>Enable rate
