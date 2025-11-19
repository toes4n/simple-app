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
    <title>DevOps Learning Platform</title>
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
        
        nav a:hover::after { width: 100%; }
        nav a:hover { color: #764ba2; transform: translateY(-2px); }
        
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
        
        tr { transition: all 0.3s ease; }
        
        tr:hover {
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
            padding: 0;
        }
    </style>
</head>
<body>
    <nav>
        <ul>
            <li><a href="/">🏠 Home</a></li>
            <li><a href="/kubernetes">☸️ Kubernetes</a></li>
            <li><a href="/ingress">🚪 Ingress & Gateway</a></li>
            <li><a href="/kong">🦍 Kong</a></li>
            <li><a href="/ack">☁️ Alibaba ACK</a></li>
            <li><a href="/info">ℹ️ Info</a></li>
            <li class="badge">v{{ version }} | {{ environment }}</li>
        </ul>
    </nav>
    <div class="container">
        {{ content|safe }}
    </div>
</body>
</html>
"""

HOME_CONTENT = """
<div class="hero">
    <h1> 🎮 Dev Platform 😎👌🔥 </h1>
    <p>Master Kubernetes, API Gateway, and Cloud-Native Technologies</p>
    
    <div class="grid">
        <div class="card">
            <div class="icon">☸️</div>
            <h3>Kubernetes</h3>
            <p>Container Orchestration</p>
        </div>
        <div class="card">
            <div class="icon">🚪</div>
            <h3>Ingress & Gateway</h3>
            <p>Traffic Management</p>
        </div>
        <div class="card">
            <div class="icon">🦍</div>
            <h3>Kong Gateway</h3>
            <p>API Management</p>
        </div>
        <div class="card">
            <div class="icon">☁️</div>
            <h3>Alibaba ACK</h3>
            <p>Managed K8s Service</p>
        </div>
    </div>
    
    <div class="highlight">
        <h2>🎯 Platform Features</h2>
        <ul>
            <li>✅ Multi-platform Docker builds (AMD64/ARM64)</li>
            <li>✅ Kubernetes deployment with HPA</li>
            <li>✅ ArgoCD GitOps workflow</li>
            <li>✅ GitHub Actions CI/CD</li>
            <li>✅ Kong Ingress Controller</li>
            <li>✅ Gateway API with HTTPRoute</li>
        </ul>
    </div>
</div>
"""

KUBERNETES_CONTENT = """
<h1 style="color: #667eea; text-align: center; margin-bottom: 2rem;">☸️ Kubernetes Architecture</h1>

<div class="concept-card">
    <h2>📖 Official Documentation</h2>
    <p>Kubernetes is an open-source container orchestration platform for automating deployment, scaling, and management.</p>
    <a href="https://kubernetes.io/docs/" target="_blank" class="link-button">Official Docs</a>
    <a href="https://kubernetes.io/docs/concepts/architecture/" target="_blank" class="link-button">Architecture Guide</a>
</div>

<div class="architecture-diagram">
    <h3 style="color: #667eea; margin-bottom: 1.5rem;">Kubernetes Cluster Architecture</h3>
    <div style="background: #e3f2fd; padding: 1.5rem; border-radius: 8px; margin-bottom: 1rem;">
        <strong style="color: #1976d2;">Control Plane</strong><br><br>
        <div class="component-box">API Server</div>
        <div class="component-box">etcd</div>
        <div class="component-box">Scheduler</div>
        <div class="component-box">Controller Manager</div>
    </div>
    <div style="font-size: 2rem; color: #667eea;">⬇️</div>
    <div style="background: #f3e5f5; padding: 1.5rem; border-radius: 8px; margin-top: 1rem;">
        <strong style="color: #7b1fa2;">Worker Nodes</strong><br><br>
        <div class="component-box">kubelet</div>
        <div class="component-box">kube-proxy</div>
        <div class="component-box">Container Runtime</div>
        <div class="component-box">Pods</div>
    </div>
</div>

<div class="concept-card">
    <h2>📦 Core Components</h2>
    <h3>Control Plane</h3>
    <ul>
        <li><code>kube-apiserver</code> - Exposes the Kubernetes HTTP API</li>
        <li><code>etcd</code> - Consistent key-value store for cluster data</li>
        <li><code>kube-scheduler</code> - Assigns Pods to nodes</li>
        <li><code>kube-controller-manager</code> - Runs controller processes</li>
    </ul>
    
    <h3>Worker Node Components</h3>
    <ul>
        <li><code>kubelet</code> - Ensures containers are running in Pods</li>
        <li><code>kube-proxy</code> - Network proxy for Service communication</li>
        <li><code>Container Runtime</code> - containerd, CRI-O, Docker</li>
    </ul>
</div>

<div class="concept-card">
    <h2>🔧 Essential kubectl Commands</h2>
    <pre><code># Cluster info
kubectl cluster-info
kubectl get nodes

# Pod operations
kubectl get pods -A
kubectl logs &lt;pod-name&gt;
kubectl exec -it &lt;pod-name&gt; -- /bin/bash

# Deployments
kubectl apply -f deployment.yaml
kubectl rollout status deployment/&lt;name&gt;</code></pre>
</div>
"""

INGRESS_CONTENT = """
<h1 style="color: #667eea; text-align: center; margin-bottom: 2rem;">🚪 Ingress & Gateway API</h1>

<div class="concept-card">
    <h2>📖 Kubernetes Ingress</h2>
    <p>Ingress manages external access to services in a cluster, typically HTTP/HTTPS.</p>
    
    <h3>Ingress Example</h3>
    <pre><code>
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: flask-ingress
spec:
  rules:
  - host: flask.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: flask-service
            port:
              number: 5000</code></pre>
</div>

<div class="architecture-diagram">
    <h3 style="color: #667eea;">Ingress Traffic Flow</h3>
    <div style="background: #fff3e0; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
        <strong>🌐 External Traffic</strong>
    </div>
    <div style="font-size: 2rem;">⬇️</div>
    <div style="background: #e3f2fd; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
        <strong>Ingress Controller</strong>
    </div>
    <div style="font-size: 2rem;">⬇️</div>
    <div style="background: #e8f5e9; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
        <strong>Service</strong>
    </div>
    <div style="font-size: 2rem;">⬇️</div>
    <div style="background: #f3e5f5; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
        <strong>Pods</strong>
    </div>
</div>

<div class="concept-card">
    <h2>🚀 Gateway API - Next Generation</h2>
    <p>Gateway API provides more expressive, extensible, and role-oriented API for traffic management.</p>
    
    <h3>HTTPRoute Example</h3>
    <pre><code>
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: flask-route
spec:
  parentRefs:
  - name: my-gateway
  hostnames:
  - "flask.example.com"
  rules:
  - matches:
    - path:
        type: PathPrefix
        value: /
    backendRefs:
    - name: flask-service
      port: 5000</code></pre>
</div>

<div class="concept-card">
    <h2>⚖️ Ingress vs Gateway API</h2>
    <table>
        <tr>
            <th>Feature</th>
            <th>Ingress</th>
            <th>Gateway API</th>
        </tr>
        <tr>
            <td>Architecture</td>
            <td>Flat (single resource)</td>
            <td>Layered (Gateway → Route)</td>
        </tr>
        <tr>
            <td>Protocol Support</td>
            <td>HTTP/HTTPS only</td>
            <td>HTTP, TCP, UDP, gRPC</td>
        </tr>
        <tr>
            <td>Extensibility</td>
            <td>Annotations</td>
            <td>CRD-based</td>
        </tr>
        <tr>
            <td>Traffic Management</td>
            <td>Basic routing</td>
            <td>Advanced (splitting, mirroring)</td>
        </tr>
    </table>
</div>
"""

KONG_CONTENT = """
<h1 style="color: #667eea; text-align: center; margin-bottom: 2rem;">🦍 Kong Gateway & Ingress Controller</h1>

<div class="concept-card">
    <h2>📖 What is Kong?</h2>
    <p>Kong Gateway is a cloud-native, fast, and flexible API gateway for microservices and distributed architectures.</p>
    
    <h3>Key Features</h3>
    <ul>
        <li>🚀 High-performance API gateway (OpenResty/LuaJIT)</li>
        <li>🔌 60+ plugins for auth, security, traffic control</li>
        <li>☸️ Native Kubernetes Ingress Controller</li>
        <li>🌐 Multi-cloud and hybrid deployment</li>
        <li>🤖 AI Gateway for LLM traffic management</li>
    </ul>
    
    <div style="margin-top: 1rem;">
        <a href="https://konghq.com" target="_blank" class="link-button">Kong Official</a>
        <a href="https://docs.konghq.com/kubernetes-ingress-controller" target="_blank" class="link-button">KIC Docs</a>
    </div>
</div>

<div class="architecture-diagram">
    <h3 style="color: #667eea;">Kong Ingress Controller Architecture</h3>
    <div style="background: #fff3e0; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
        <strong>🌐 External Traffic</strong>
    </div>
    <div style="font-size: 2rem;">⬇️</div>
    <div style="background: #e1f5fe; padding: 1.5rem; border-radius: 8px; margin: 1rem 0;">
        <strong>Kong Gateway (Data Plane)</strong><br>
        <div class="component-box">Load Balancer</div>
        <div class="component-box">Plugins</div>
        <div class="component-box">Router</div>
    </div>
    <div style="font-size: 2rem;">⬅️ Configures</div>
    <div style="background: #f3e5f5; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
        <strong>Kong Ingress Controller</strong>
    </div>
    <div style="font-size: 2rem;">⬇️</div>
    <div style="background: #e8f5e9; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
        <strong>Kubernetes Services & Pods</strong>
    </div>
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
    <h2>🔌 Popular Kong Plugins</h2>
    <table>
        <tr>
            <th>Category</th>
            <th>Plugins</th>
        </tr>
        <tr>
            <td>🔐 Authentication</td>
            <td>key-auth, jwt, oauth2, basic-auth</td>
        </tr>
        <tr>
            <td>🚦 Traffic Control</td>
            <td>rate-limiting, request-size-limiting</td>
        </tr>
        <tr>
            <td>🔄 Transformation</td>
            <td>request-transformer, response-transformer</td>
        </tr>
        <tr>
            <td>📊 Analytics</td>
            <td>prometheus, datadog, zipkin</td>
        </tr>
        <tr>
            <td>🛡️ Security</td>
            <td>cors, ip-restriction, bot-detection</td>
        </tr>
    </table>
</div>

<div class="concept-card">
    <h2>💡 Kong Best Practices</h2>
    <ul>
        <li>Use DB-less mode with Kubernetes for GitOps</li>
        <li>Apply plugins at appropriate levels (global/service/route)</li>
        <li>Enable rate limiting to protect backend services</li>
        <li>Use HTTPRoute for advanced Gateway API routing</li>
        <li>Monitor with Prometheus plugin integration</li>
        <li>Implement proper authentication for production APIs</li>
    </ul>
</div>
"""

ACK_CONTENT = """
<h1 style="color: #667eea; text-align: center; margin-bottom: 2rem;">☁️ Alibaba Cloud Container Service (ACK)</h1>

<div class="concept-card">
    <h2>📖 What is ACK?</h2>
    <p>Alibaba Cloud Container Service for Kubernetes (ACK) is a fully managed Kubernetes service with deep integration into Alibaba Cloud services.</p>
    
    <h3>Key Benefits</h3>
    <ul>
        <li>Fully managed control plane</li>
        <li>High availability across multiple zones</li>
        <li>Deep integration with VPC, SLB, OSS, NAS</li>
        <li>Built-in security and compliance</li>
        <li>Auto-scaling and disaster recovery</li>
    </ul>
    
    <a href="https://www.alibabacloud.com/product/kubernetes" target="_blank" class="link-button">ACK Product Page</a>
    <a href="https://www.alibabacloud.com/help/container-service-for-kubernetes" target="_blank" class="link-button">Documentation</a>
</div>

<div class="architecture-diagram">
    <h3 style="color: #667eea;">ACK Service Architecture</h3>
    <div style="background: #fff3e0; padding: 1.5rem; border-radius: 8px; margin: 1rem 0;">
        <strong>☁️ Alibaba Cloud Services</strong><br>
        <div class="component-box">VPC</div>
        <div class="component-box">SLB</div>
        <div class="component-box">OSS</div>
        <div class="component-box">NAS</div>
    </div>
    <div style="font-size: 2rem;">⬇️</div>
    <div style="background: #e3f2fd; padding: 1.5rem; border-radius: 8px; margin: 1rem 0;">
        <strong>ACK Managed Control Plane</strong><br>
        <div class="component-box">API Server (HA)</div>
        <div class="component-box">etcd (3 nodes)</div>
        <div class="component-box">Scheduler</div>
    </div>
    <div style="font-size: 2rem;">⬇️</div>
    <div style="background: #f3e5f5; padding: 1.5rem; border-radius: 8px; margin: 1rem 0;">
        <strong>Worker Nodes (ECS Instances)</strong><br>
        <div class="component-box">kubelet</div>
        <div class="component-box">Container Runtime</div>
        <div class="component-box">Your Apps</div>
    </div>
</div>

<div class="concept-card">
    <h2>🚀 ACK Cluster Types</h2>
    <table>
        <tr>
            <th>Type</th>
            <th>Description</th>
        </tr>
        <tr>
            <td><strong>Managed Kubernetes</strong></td>
            <td>Alibaba manages control plane</td>
        </tr>
        <tr>
            <td><strong>Serverless (ASK)</strong></td>
            <td>No node management, pay per pod</td>
        </tr>
        <tr>
            <td><strong>Dedicated Kubernetes</strong></td>
            <td>Full control over all components</td>
        </tr>
        <tr>
            <td><strong>Edge Kubernetes</strong></td>
            <td>Extends K8s to edge locations</td>
        </tr>
    </table>
</div>

<div class="concept-card">
    <h2>🔧 ACK Key Features</h2>
    
    <h3>Networking</h3>
    <ul>
        <li><strong>Terway</strong> - High-performance CNI plugin</li>
        <li><strong>Flannel</strong> - Standard overlay networking</li>
        <li>Network Policy support</li>
        <li>SLB integration for load balancing</li>
    </ul>
    
    <h3>Storage</h3>
    <ul>
        <li><strong>Cloud Disk</strong> - Block storage (SSD, ESSD)</li>
        <li><strong>NAS</strong> - Shared file storage</li>
        <li><strong>OSS</strong> - Object storage integration</li>
        <li>Dynamic volume provisioning</li>
    </ul>
    
    <h3>Auto Scaling</h3>
    <ul>
        <li>Horizontal Pod Autoscaler (HPA)</li>
        <li>Vertical Pod Autoscaler (VPA)</li>
        <li>Cluster Autoscaler</li>
        <li>Scheduled scaling</li>
    </ul>
</div>

<div class="concept-card">
    <h2>💡 ACK Best Practices</h2>
    <ul>
        <li>Use managed clusters for easier operations</li>
        <li>Deploy across multiple zones for HA</li>
        <li>Use Terway CNI for better performance</li>
        <li>Enable cluster autoscaling for cost optimization</li>
        <li>Use ACR (Alibaba Container Registry) for faster pulls</li>
        <li>Monitor with ARMS and Log Service</li>
        <li>Implement pod security policies</li>
    </ul>
</div>
"""

@app.route('/')
def home():
    return render_template_string(BASE_TEMPLATE, content=HOME_CONTENT, version=VERSION, environment=ENVIRONMENT)

@app.route('/kubernetes')
def kubernetes():
    return render_template_string(BASE_TEMPLATE, content=KUBERNETES_CONTENT, version=VERSION, environment=ENVIRONMENT)

@app.route('/ingress')
def ingress():
    return render_template_string(BASE_TEMPLATE, content=INGRESS_CONTENT, version=VERSION, environment=ENVIRONMENT)

@app.route('/kong')
def kong():
    return render_template_string(BASE_TEMPLATE, content=KONG_CONTENT, version=VERSION, environment=ENVIRONMENT)

@app.route('/ack')
def ack():
    return render_template_string(BASE_TEMPLATE, content=ACK_CONTENT, version=VERSION, environment=ENVIRONMENT)

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
    
    info_content = f"""
    <h1 style="color: #667eea; text-align: center; margin-bottom: 2rem;">ℹ️ Deployment Information</h1>
    <div style="background: #f8f9fa; padding: 2rem; border-radius: 10px;">
        <table>
            {''.join([f'<tr><td style="font-weight: 600; color: #667eea;">{key.replace("_", " ").title()}</td><td>{value}</td></tr>' for key, value in deployment_info.items()])}
        </table>
    </div>
    <div style="margin-top: 2rem; padding: 1.5rem; background: #e8f5e9; border-left: 5px solid #4caf50; border-radius: 5px;">
        <strong style="color: #2e7d32;">✅ Status:</strong> Application running successfully!
    </div>
    """
    
    return render_template_string(BASE_TEMPLATE, content=info_content, version=VERSION, environment=ENVIRONMENT)

@app.route('/api/metrics')
def metrics():
    return jsonify({
        'requests_total': 100,
        'uptime_seconds': 3600,
        'memory_usage_mb': 128,
        'cpu_usage_percent': 5.2
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
