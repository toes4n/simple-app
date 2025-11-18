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
            gap: 1.5rem;
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
            max-width: 1400px;
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
        }
        .architecture-diagram {
            background: #f8f9fa;
            padding: 2rem;
            border-radius: 10px;
            margin: 2rem 0;
            text-align: center;
        }
        .component-box {
            display: inline-block;
            padding: 1rem 1.5rem;
            margin: 0.5rem;
            background: white;
            border: 2px solid #667eea;
            border-radius: 8px;
            font-weight: 600;
        }
        .link-button {
            display: inline-block;
            padding: 0.6rem 1.2rem;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin: 0.5rem;
            transition: background 0.3s;
        }
        .link-button:hover { background: #764ba2; }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
        }
        th, td {
            padding: 1rem;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background: #667eea;
            color: white;
            font-weight: 600;
        }
        .comparison-table td:first-child {
            font-weight: 600;
            color: #667eea;
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
        code {
            background: #f4f4f4;
            padding: 0.2rem 0.5rem;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            color: #e83e8c;
        }
        pre {
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 1.5rem;
            border-radius: 8px;
            overflow-x: auto;
            margin: 1rem 0;
        }
        pre code {
            background: transparent;
            color: #f8f8f2;
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
    <h1>🦸🏻‍♂️ SRE Team PowerRangers KT Kitty Session</h1>
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
            <div class="icon">☁️</div>
            <h3>Alibaba ACK</h3>
            <p>Managed Kubernetes</p>
        </div>
        
        <div class="card">
            <div class="icon">⚡</div>
            <h3>CI/CD Pipeline</h3>
            <p>GitHub Actions + ArgoCD</p>
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

KUBERNETES_PAGE = """
<h1 style="color: #667eea; margin-bottom: 2rem; text-align: center;">☸️ Kubernetes Architecture & Concepts</h1>

<div class="concept-card">
    <h2>📖 Official Documentation</h2>
    <p>Kubernetes is an open-source container orchestration platform for automating deployment, scaling, and management of containerized applications.</p>
    <div style="margin-top: 1rem;">
        <a href="https://kubernetes.io/docs/concepts/architecture/" target="_blank" class="link-button">Official Architecture Docs</a>
        <a href="https://kubernetes.io/docs/concepts/" target="_blank" class="link-button">Kubernetes Concepts</a>
        <a href="https://kubernetes.io/docs/tutorials/" target="_blank" class="link-button">Tutorials</a>
    </div>
</div>

<div class="concept-card">
    <h2>🏗️ Kubernetes Architecture</h2>
    <p>A Kubernetes cluster consists of <strong>Control Plane</strong> nodes and <strong>Worker</strong> nodes.</p>
    
    <h3>Control Plane Components</h3>
    <ul>
        <li><code>kube-apiserver</code> - Core component that exposes the Kubernetes HTTP API</li>
        <li><code>etcd</code> - Consistent and highly-available key-value store for all cluster data</li>
        <li><code>kube-scheduler</code> - Assigns Pods to nodes based on resource requirements</li>
        <li><code>kube-controller-manager</code> - Runs controllers to implement Kubernetes API behavior</li>
        <li><code>cloud-controller-manager</code> - Integrates with cloud provider APIs (optional)</li>
    </ul>
    
    <h3>Worker Node Components</h3>
    <ul>
        <li><code>kubelet</code> - Agent that ensures containers are running in a Pod</li>
        <li><code>kube-proxy</code> - Network proxy maintaining network rules for Service communication</li>
        <li><code>Container Runtime</code> - Software for running containers (containerd, CRI-O, Docker)</li>
    </ul>
</div>

<div class="architecture-diagram">
    <h3 style="color: #667eea; margin-bottom: 1.5rem;">Kubernetes Cluster Architecture</h3>
    <div style="margin: 2rem 0;">
        <div style="background: #e3f2fd; padding: 1.5rem; border-radius: 8px; margin-bottom: 1rem;">
            <strong style="color: #1976d2;">Control Plane</strong><br><br>
            <div class="component-box" style="border-color: #1976d2;">API Server</div>
            <div class="component-box" style="border-color: #1976d2;">etcd</div>
            <div class="component-box" style="border-color: #1976d2;">Scheduler</div>
            <div class="component-box" style="border-color: #1976d2;">Controller Manager</div>
        </div>
        <div style="font-size: 2rem; color: #667eea;">⬇️</div>
        <div style="background: #f3e5f5; padding: 1.5rem; border-radius: 8px; margin-top: 1rem;">
            <strong style="color: #7b1fa2;">Worker Nodes</strong><br><br>
            <div class="component-box" style="border-color: #7b1fa2;">kubelet</div>
            <div class="component-box" style="border-color: #7b1fa2;">kube-proxy</div>
            <div class="component-box" style="border-color: #7b1fa2;">Container Runtime</div>
            <div class="component-box" style="border-color: #7b1fa2;">Pods</div>
        </div>
    </div>
</div>

<div class="concept-card">
    <h2>📦 Core Kubernetes Objects</h2>
    <table>
        <tr>
            <th>Object</th>
            <th>Purpose</th>
        </tr>
        <tr>
            <td><code>Pod</code></td>
            <td>Smallest deployable unit, contains one or more containers</td>
        </tr>
        <tr>
            <td><code>Deployment</code></td>
            <td>Manages ReplicaSets and provides declarative updates</td>
        </tr>
        <tr>
            <td><code>Service</code></td>
            <td>Exposes applications running on Pods as network services</td>
        </tr>
        <tr>
            <td><code>ConfigMap</code></td>
            <td>Stores configuration data in key-value pairs</td>
        </tr>
        <tr>
            <td><code>Secret</code></td>
            <td>Stores sensitive data like passwords and tokens</td>
        </tr>
        <tr>
            <td><code>Namespace</code></td>
            <td>Provides virtual clusters for resource isolation</td>
        </tr>
        <tr>
            <td><code>StatefulSet</code></td>
            <td>Manages stateful applications with persistent identity</td>
        </tr>
        <tr>
            <td><code>DaemonSet</code></td>
            <td>Ensures all nodes run a copy of a Pod</td>
        </tr>
    </table>
</div>

<div class="concept-card">
    <h2>🔧 Kubectl Common Commands</h2>
    <pre><code># Get cluster info
kubectl cluster-info
kubectl get nodes

# Pod operations
kubectl get pods -A
kubectl describe pod &lt;pod-name&gt;
kubectl logs &lt;pod-name&gt;

# Deployment operations
kubectl get deployments
kubectl apply -f deployment.yaml
kubectl rollout status deployment/&lt;name&gt;

# Service operations
kubectl get services
kubectl expose deployment &lt;name&gt; --port=80

# Debug
kubectl exec -it &lt;pod-name&gt; -- /bin/bash
kubectl port-forward &lt;pod-name&gt; 8080:80</code></pre>
</div>
"""

INGRESS_GATEWAY_PAGE = """
<h1 style="color: #667eea; margin-bottom: 2rem; text-align: center;">🚪 Kubernetes Ingress & Gateway API</h1>

<div class="concept-card">
    <h2>📖 What is Ingress?</h2>
    <p>Ingress is a Kubernetes API object that manages external access to services in a cluster, typically HTTP/HTTPS. It provides load balancing, SSL termination, and name-based virtual hosting.</p>
    
    <h3>Key Features</h3>
    <ul>
        <li>Exposes HTTP and HTTPS routes from outside to services within the cluster</li>
        <li>Can provide load balancing and SSL/TLS termination</li>
        <li>Name-based virtual hosting support</li>
        <li>Requires an Ingress Controller (NGINX, Traefik, HAProxy, etc.)</li>
    </ul>
    
    <h3>Example Ingress Resource</h3>
    <pre><code>
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: flask-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
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
    <h3 style="color: #667eea; margin-bottom: 1.5rem;">Ingress Architecture</h3>
    <div style="margin: 2rem 0; text-align: center;">
        <div style="background: #fff3e0; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
            <strong style="color: #e65100;">🌐 External Traffic</strong>
        </div>
        <div style="font-size: 2rem;">⬇️</div>
        <div style="background: #e3f2fd; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            <strong style="color: #1976d2;">Ingress Controller (NGINX/Traefik)</strong>
        </div>
        <div style="font-size: 2rem;">⬇️</div>
        <div style="background: #e8f5e9; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            <strong style="color: #2e7d32;">Service (ClusterIP)</strong>
        </div>
        <div style="font-size: 2rem;">⬇️</div>
        <div style="background: #f3e5f5; padding: 1rem; border-radius: 8px; margin-top: 1rem;">
            <strong style="color: #7b1fa2;">Pods</strong>
        </div>
    </div>
</div>

<div class="concept-card">
    <h2>🚀 Gateway API - The Future of Kubernetes Networking</h2>
    <p>Gateway API is the next-generation API for managing ingress and service mesh traffic in Kubernetes. It provides a more expressive, extensible, and role-oriented API compared to Ingress.</p>
    
    <h3>Key Advantages Over Ingress</h3>
    <ul>
        <li><strong>Role-oriented</strong>: Separates concerns between infrastructure admins and app developers</li>
        <li><strong>Protocol support</strong>: HTTP, HTTPS, TCP, UDP, gRPC (not just L7)</li>
        <li><strong>Extensible</strong>: CRD-based, cleanly extensible without annotations</li>
        <li><strong>Portable</strong>: Standardized across implementations</li>
        <li><strong>Traffic management</strong>: Built-in support for A/B testing, canary deployments, traffic splitting</li>
    </ul>
</div>

<div class="concept-card">
    <h2>🏗️ Gateway API Resource Model</h2>
    <p>Gateway API introduces three core resources:</p>
    
    <table>
        <tr>
            <th>Resource</th>
            <th>Role</th>
            <th>Description</th>
        </tr>
        <tr>
            <td><code>GatewayClass</code></td>
            <td>Infrastructure</td>
            <td>Defines controller capabilities (e.g., NGINX, Cilium, Istio)</td>
        </tr>
        <tr>
            <td><code>Gateway</code></td>
            <td>Cluster Operator</td>
            <td>Instantiates a load balancer with specific configuration</td>
        </tr>
        <tr>
            <td><code>HTTPRoute</code></td>
            <td>App Developer</td>
            <td>Defines HTTP routing rules (replaces Ingress)</td>
        </tr>
    </table>
</div>

<div class="concept-card">
    <h2>📝 HTTPRoute Example</h2>
    <p><code>HTTPRoute</code> is the Gateway API equivalent of Ingress for HTTP traffic.</p>
    <pre><code>apiVersion: gateway.networking.k8s.io/v1
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
      port: 5000
    filters:
    - type: RequestHeaderModifier
      requestHeaderModifier:
        add:
        - name: X-Custom-Header
          value: "my-value"</code></pre>
</div>

<div class="concept-card">
    <h2>⚖️ Ingress vs Gateway API Comparison</h2>
    <table class="comparison-table">
        <tr>
            <th>Feature</th>
            <th>Ingress</th>
            <th>Gateway API</th>
        </tr>
        <tr>
            <td>Architecture</td>
            <td>Flat (single resource)</td>
            <td>Layered (GatewayClass → Gateway → Route)</td>
        </tr>
        <tr>
            <td>Extensibility</td>
            <td>Annotations (vendor-specific)</td>
            <td>CRD-based, standardized</td>
        </tr>
        <tr>
            <td>Protocol Support</td>
            <td>HTTP/HTTPS only</td>
            <td>HTTP, HTTPS, TCP, TLS, UDP, gRPC</td>
        </tr>
        <tr>
            <td>Role Separation</td>
            <td>Limited</td>
            <td>Built-in (Infra/Cluster/App roles)</td>
        </tr>
        <tr>
            <td>Traffic Management</td>
            <td>Basic routing</td>
            <td>Advanced (splitting, mirroring, retries)</td>
        </tr>
        <tr>
            <td>Portability</td>
            <td>Vendor-specific annotations</td>
            <td>Standardized across implementations</td>
        </tr>
    </table>
</div>

<div class="concept-card">
    <h2>🔗 Official Resources</h2>
    <div style="margin-top: 1rem;">
        <a href="https://kubernetes.io/docs/concepts/services-networking/ingress/" target="_blank" class="link-button">Ingress Documentation</a>
        <a href="https://gateway-api.sigs.k8s.io/" target="_blank" class="link-button">Gateway API Documentation</a>
        <a href="https://gateway-api.sigs.k8s.io/guides/http-routing/" target="_blank" class="link-button">HTTPRoute Guide</a>
    </div>
</div>
"""

ALIBABA_ACK_PAGE = """
<h1 style="color: #667eea; margin-bottom: 2rem; text-align: center;">☁️ Alibaba Cloud Container Service for Kubernetes (ACK)</h1>

<div class="concept-card">
    <h2>📖 What is Alibaba ACK?</h2>
    <p>Alibaba Cloud Container Service for Kubernetes (ACK) is a fully managed Kubernetes service that integrates with Alibaba Cloud's virtualization, storage, networking, and security capabilities to provide high-performance and scalable container applications.</p>
    
    <h3>Key Benefits</h3>
    <ul>
        <li>Fully managed Kubernetes control plane</li>
        <li>High availability across multiple zones</li>
        <li>Deep integration with Alibaba Cloud services (VPC, SLB, OSS, NAS, etc.)</li>
        <li>Built-in security and compliance features</li>
        <li>Auto-scaling and disaster recovery</li>
        <li>Managed cluster upgrades and patches</li>
    </ul>
</div>

<div class="concept-card">
    <h2>🏗️ ACK Architecture</h2>
    <p>ACK manages the entire control plane while you manage worker nodes. The architecture includes:</p>
    
    <h3>Managed Control Plane</h3>
    <ul>
        <li>At least 2 <code>kube-apiserver</code> instances</li>
        <li>3 <code>etcd</code> instances deployed across zones</li>
        <li><code>kube-controller-manager</code> and <code>kube-scheduler</code></li>
        <li>Alibaba Cloud Controller Manager for cloud integration</li>
    </ul>
    
    <h3>Worker Nodes</h3>
    <ul>
        <li>ECS instances or Elastic Container Instance (ECI) for serverless</li>
        <li>Support for GPU, FPGA, and ARM instances</li>
        <li>Auto-scaling based on metrics or schedule</li>
    </ul>
</div>

<div class="architecture-diagram">
    <h3 style="color: #667eea; margin-bottom: 1.5rem;">ACK Service Architecture</h3>
    <div style="margin: 2rem 0; text-align: left;">
        <div style="background: #fff3e0; padding: 1.5rem; border-radius: 8px; margin-bottom: 1rem;">
            <strong style="color: #e65100;">🎯 Alibaba Cloud Services Integration</strong><br><br>
            <div class="component-box" style="border-color: #e65100; font-size: 0.9rem;">VPC</div>
            <div class="component-box" style="border-color: #e65100; font-size: 0.9rem;">SLB</div>
            <div class="component-box" style="border-color: #e65100; font-size: 0.9rem;">OSS</div>
            <div class="component-box" style="border-color: #e65100; font-size: 0.9rem;">NAS</div>
            <div class="component-box" style="border-color: #e65100; font-size: 0.9rem;">ACR</div>
        </div>
        <div style="font-size: 2rem; text-align: center;">⬇️</div>
        <div style="background: #e3f2fd; padding: 1.5rem; border-radius: 8px; margin: 1rem 0;">
            <strong style="color: #1976d2;">ACK Managed Control Plane</strong><br><br>
            <div class="component-box" style="border-color: #1976d2; font-size: 0.9rem;">API Server (HA)</div>
            <div class="component-box" style="border-color: #1976d2; font-size: 0.9rem;">etcd (3 nodes)</div>
            <div class="component-box" style="border-color: #1976d2; font-size: 0.9rem;">Scheduler</div>
            <div class="component-box" style="border-color: #1976d2; font-size: 0.9rem;">Controllers</div>
        </div>
        <div style="font-size: 2rem; text-align: center;">⬇️</div>
        <div style="background: #f3e5f5; padding: 1.5rem; border-radius: 8px; margin-top: 1rem;">
            <strong style="color: #7b1fa2;">Worker Nodes (Your ECS Instances)</strong><br><br>
            <div class="component-box" style="border-color: #7b1fa2; font-size: 0.9rem;">kubelet</div>
            <div class="component-box" style="border-color: #7b1fa2; font-size: 0.9rem;">Container Runtime</div>
            <div class="component-box" style="border-color: #7b1fa2; font-size: 0.9rem;">Your Applications</div>
        </div>
    </div>
</div>

<div class="concept-card">
    <h2>🚀 ACK Cluster Types</h2>
    <table>
        <tr>
            <th>Type</th>
            <th>Description</th>
            <th>Use Case</th>
        </tr>
        <tr>
            <td><strong>Managed Kubernetes</strong></td>
            <td>Alibaba manages control plane, you manage worker nodes</td>
            <td>Production workloads with full control</td>
        </tr>
        <tr>
            <td><strong>Serverless Kubernetes (ASK)</strong></td>
            <td>No need to manage nodes, pay per pod</td>
            <td>Burst workloads, cost optimization</td>
        </tr>
        <tr>
            <td><strong>Dedicated Kubernetes</strong></td>
            <td>Full control over control plane and worker nodes</td>
            <td>Regulated industries, custom requirements</td>
        </tr>
        <tr>
            <td><strong>Edge Kubernetes</strong></td>
            <td>Extends K8s to edge locations</td>
            <td>IoT, CDN, edge computing</td>
        </tr>
    </table>
</div>

<div class="concept-card">
    <h2>🔧 ACK Key Features</h2>
    
    <h3>Networking</h3>
    <ul>
        <li><strong>Terway</strong>: High-performance CNI plugin for VPC networking</li>
        <li><strong>Flannel</strong>: Standard overlay networking</li>
        <li>Network Policy support for pod-to-pod security</li>
        <li>Integration with SLB for load balancing</li>
    </ul>
    
    <h3>Storage</h3>
    <ul>
        <li><strong>Cloud Disk</strong>: Block storage (SSD, ESSD, Ultra)</li>
        <li><strong>NAS</strong>: Network Attached Storage for shared volumes</li>
        <li><strong>OSS</strong>: Object storage integration</li>
        <li>Dynamic volume provisioning with CSI drivers</li>
    </ul>
    
    <h3>Auto Scaling</h3>
    <ul>
        <li><strong>HPA</strong>: Horizontal Pod Autoscaler based on metrics</li>
        <li><strong>VPA</strong>: Vertical Pod Autoscaler for resource optimization</li>
        <li><strong>Cluster Autoscaler</strong>: Auto scale nodes based on demand</li>
        <li>Scheduled scaling for predictable workloads</li>
    </ul>
    
    <h3>Observability</h3>
    <ul>
        <li>Integration with Alibaba Cloud Monitor</li>
        <li>Built-in logging with Log Service (SLS)</li>
        <li>Application Real-Time Monitoring Service (ARMS)</li>
        <li>Prometheus and Grafana support</li>
    </ul>
</div>

<div class="concept-card">
    <h2>🔐 ACK Security Features</h2>
    <ul>
        <li><strong>RAM</strong>: Role-based access control integration</li>
        <li><strong>Security Center</strong>: Runtime security scanning</li>
        <li><strong>KMS</strong>: Encryption for secrets at rest</li>
        <li><strong>Security Groups</strong>: Network-level firewall rules</li>
        <li><strong>Pod Security Policies</strong>: Control pod privileges</li>
        <li>Regular security patches and CVE fixes</li>
    </ul>
</div>

<div class="concept-card">
    <h2>💡 ACK Best Practices</h2>
    <ul>
        <li>Use managed clusters for easier operations</li>
        <li>Deploy across multiple zones for high availability</li>
        <li>Use Terway CNI for better network performance</li>
        <li>Enable cluster autoscaling for cost optimization</li>
        <li>Implement pod security policies</li>
        <li>Use ACR (Alibaba Container Registry) for faster image pulls</li>
        <li>Monitor with ARMS and Log Service</li>
        <li>Use Node pools for different workload types</li>
    </ul>
</div>

<div class="concept-card">
    <h2>🔗 Official Resources</h2>
    <div style="margin-top: 1rem;">
        <a href="https://www.alibabacloud.com/product/kubernetes" target="_blank" class="link-button">ACK Product Page</a>
        <a href="https://www.alibabacloud.com/help/container-service-for-kubernetes" target="_blank" class="link-button">ACK Documentation</a>
        <a href="https://www.alibabacloud.com/help/doc-detail/86745.htm" target="_blank" class="link-button">ACK Architecture</a>
    </div>
</div>
"""

DEVOPS_CONCEPTS = """
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
    return render_template_string(HOME_PAGE, version=VERSION, environment=ENVIRONMENT)

@app.route('/kubernetes')
def kubernetes():
    k8s_html = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', KUBERNETES_PAGE)
    return render_template_string(k8s_html, version=VERSION, environment=ENVIRONMENT)

@app.route('/ingress-gateway')
def ingress_gateway():
    ig_html = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', INGRESS_GATEWAY_PAGE)
    return render_template_string(ig_html, version=VERSION, environment=ENVIRONMENT)

@app.route('/alibaba-ack')
def alibaba_ack():
    ack_html = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', ALIBABA_ACK_PAGE)
    return render_template_string(ack_html, version=VERSION, environment=ENVIRONMENT)

@app.route('/devops-concepts')
def devops_concepts():
    concepts_html = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', DEVOPS_CONCEPTS)
    return render_template_string(concepts_html, version=VERSION, environment=ENVIRONMENT)

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
    
    info_html = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', f"""
    <h1 style="color: #667eea; margin-bottom: 2rem; text-align: center;">ℹ️ Deployment Information</h1>
    <div style="background: #f8f9fa; padding: 2rem; border-radius: 10px;">
        <table>
            {''.join([f'<tr><td style="font-weight: 600; color: #667eea;">{key.replace("_", " ").title()}</td><td>{value}</td></tr>' for key, value in deployment_info.items()])}
        </table>
    </div>
    <div style="margin-top: 2rem; padding: 1.5rem; background: #e8f5e9; border-left: 5px solid #4caf50; border-radius: 5px;">
        <strong style="color: #2e7d32;">✅ Status:</strong> Application is running successfully!
    </div>
    """)
    
    return render_template_string(info_html, version=VERSION, environment=ENVIRONMENT)

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
            gap: 1.5rem;
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
            max-width: 1400px;
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
        }
        .architecture-diagram {
            background: #f8f9fa;
            padding: 2rem;
            border-radius: 10px;
            margin: 2rem 0;
            text-align: center;
        }
        .component-box {
            display: inline-block;
            padding: 1rem 1.5rem;
            margin: 0.5rem;
            background: white;
            border: 2px solid #667eea;
            border-radius: 8px;
            font-weight: 600;
        }
        .link-button {
            display: inline-block;
            padding: 0.6rem 1.2rem;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin: 0.5rem;
            transition: background 0.3s;
        }
        .link-button:hover { background: #764ba2; }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
        }
        th, td {
            padding: 1rem;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background: #667eea;
            color: white;
            font-weight: 600;
        }
        .comparison-table td:first-child {
            font-weight: 600;
            color: #667eea;
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
        code {
            background: #f4f4f4;
            padding: 0.2rem 0.5rem;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            color: #e83e8c;
        }
        pre {
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 1.5rem;
            border-radius: 8px;
            overflow-x: auto;
            margin: 1rem 0;
        }
        pre code {
            background: transparent;
            color: #f8f8f2;
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
    <h1>🚀 Welcome to DevOps Learning Platform</h1>
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
            <div class="icon">☁️</div>
            <h3>Alibaba ACK</h3>
            <p>Managed Kubernetes</p>
        </div>
        
        <div class="card">
            <div class="icon">⚡</div>
            <h3>CI/CD Pipeline</h3>
            <p>GitHub Actions + ArgoCD</p>
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

KUBERNETES_PAGE = """
<h1 style="color: #667eea; margin-bottom: 2rem; text-align: center;">☸️ Kubernetes Architecture & Concepts</h1>

<div class="concept-card">
    <h2>📖 Official Documentation</h2>
    <p>Kubernetes is an open-source container orchestration platform for automating deployment, scaling, and management of containerized applications.</p>
    <div style="margin-top: 1rem;">
        <a href="https://kubernetes.io/docs/concepts/architecture/" target="_blank" class="link-button">Official Architecture Docs</a>
        <a href="https://kubernetes.io/docs/concepts/" target="_blank" class="link-button">Kubernetes Concepts</a>
        <a href="https://kubernetes.io/docs/tutorials/" target="_blank" class="link-button">Tutorials</a>
    </div>
</div>

<div class="concept-card">
    <h2>🏗️ Kubernetes Architecture</h2>
    <p>A Kubernetes cluster consists of <strong>Control Plane</strong> nodes and <strong>Worker</strong> nodes.</p>
    
    <h3>Control Plane Components</h3>
    <ul>
        <li><code>kube-apiserver</code> - Core component that exposes the Kubernetes HTTP API</li>
        <li><code>etcd</code> - Consistent and highly-available key-value store for all cluster data</li>
        <li><code>kube-scheduler</code> - Assigns Pods to nodes based on resource requirements</li>
        <li><code>kube-controller-manager</code> - Runs controllers to implement Kubernetes API behavior</li>
        <li><code>cloud-controller-manager</code> - Integrates with cloud provider APIs (optional)</li>
    </ul>
    
    <h3>Worker Node Components</h3>
    <ul>
        <li><code>kubelet</code> - Agent that ensures containers are running in a Pod</li>
        <li><code>kube-proxy</code> - Network proxy maintaining network rules for Service communication</li>
        <li><code>Container Runtime</code> - Software for running containers (containerd, CRI-O, Docker)</li>
    </ul>
</div>

<div class="architecture-diagram">
    <h3 style="color: #667eea; margin-bottom: 1.5rem;">Kubernetes Cluster Architecture</h3>
    <div style="margin: 2rem 0;">
        <div style="background: #e3f2fd; padding: 1.5rem; border-radius: 8px; margin-bottom: 1rem;">
            <strong style="color: #1976d2;">Control Plane</strong><br><br>
            <div class="component-box" style="border-color: #1976d2;">API Server</div>
            <div class="component-box" style="border-color: #1976d2;">etcd</div>
            <div class="component-box" style="border-color: #1976d2;">Scheduler</div>
            <div class="component-box" style="border-color: #1976d2;">Controller Manager</div>
        </div>
        <div style="font-size: 2rem; color: #667eea;">⬇️</div>
        <div style="background: #f3e5f5; padding: 1.5rem; border-radius: 8px; margin-top: 1rem;">
            <strong style="color: #7b1fa2;">Worker Nodes</strong><br><br>
            <div class="component-box" style="border-color: #7b1fa2;">kubelet</div>
            <div class="component-box" style="border-color: #7b1fa2;">kube-proxy</div>
            <div class="component-box" style="border-color: #7b1fa2;">Container Runtime</div>
            <div class="component-box" style="border-color: #7b1fa2;">Pods</div>
        </div>
    </div>
</div>

<div class="concept-card">
    <h2>📦 Core Kubernetes Objects</h2>
    <table>
        <tr>
            <th>Object</th>
            <th>Purpose</th>
        </tr>
        <tr>
            <td><code>Pod</code></td>
            <td>Smallest deployable unit, contains one or more containers</td>
        </tr>
        <tr>
            <td><code>Deployment</code></td>
            <td>Manages ReplicaSets and provides declarative updates</td>
        </tr>
        <tr>
            <td><code>Service</code></td>
            <td>Exposes applications running on Pods as network services</td>
        </tr>
        <tr>
            <td><code>ConfigMap</code></td>
            <td>Stores configuration data in key-value pairs</td>
        </tr>
        <tr>
            <td><code>Secret</code></td>
            <td>Stores sensitive data like passwords and tokens</td>
        </tr>
        <tr>
            <td><code>Namespace</code></td>
            <td>Provides virtual clusters for resource isolation</td>
        </tr>
        <tr>
            <td><code>StatefulSet</code></td>
            <td>Manages stateful applications with persistent identity</td>
        </tr>
        <tr>
            <td><code>DaemonSet</code></td>
            <td>Ensures all nodes run a copy of a Pod</td>
        </tr>
    </table>
</div>

<div class="concept-card">
    <h2>🔧 Kubectl Common Commands</h2>
    <pre><code># Get cluster info
kubectl cluster-info
kubectl get nodes

# Pod operations
kubectl get pods -A
kubectl describe pod &lt;pod-name&gt;
kubectl logs &lt;pod-name&gt;

# Deployment operations
kubectl get deployments
kubectl apply -f deployment.yaml
kubectl rollout status deployment/&lt;name&gt;

# Service operations
kubectl get services
kubectl expose deployment &lt;name&gt; --port=80

# Debug
kubectl exec -it &lt;pod-name&gt; -- /bin/bash
kubectl port-forward &lt;pod-name&gt; 8080:80</code></pre>
</div>
"""

INGRESS_GATEWAY_PAGE = """
<h1 style="color: #667eea; margin-bottom: 2rem; text-align: center;">🚪 Kubernetes Ingress & Gateway API</h1>

<div class="concept-card">
    <h2>📖 What is Ingress?</h2>
    <p>Ingress is a Kubernetes API object that manages external access to services in a cluster, typically HTTP/HTTPS. It provides load balancing, SSL termination, and name-based virtual hosting.</p>
    
    <h3>Key Features</h3>
    <ul>
        <li>Exposes HTTP and HTTPS routes from outside to services within the cluster</li>
        <li>Can provide load balancing and SSL/TLS termination</li>
        <li>Name-based virtual hosting support</li>
        <li>Requires an Ingress Controller (NGINX, Traefik, HAProxy, etc.)</li>
    </ul>
    
    <h3>Example Ingress Resource</h3>
    <pre><code>apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: flask-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
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
    <h3 style="color: #667eea; margin-bottom: 1.5rem;">Ingress Architecture</h3>
    <div style="margin: 2rem 0; text-align: center;">
        <div style="background: #fff3e0; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
            <strong style="color: #e65100;">🌐 External Traffic</strong>
        </div>
        <div style="font-size: 2rem;">⬇️</div>
        <div style="background: #e3f2fd; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            <strong style="color: #1976d2;">Ingress Controller (NGINX/Traefik)</strong>
        </div>
        <div style="font-size: 2rem;">⬇️</div>
        <div style="background: #e8f5e9; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            <strong style="color: #2e7d32;">Service (ClusterIP)</strong>
        </div>
        <div style="font-size: 2rem;">⬇️</div>
        <div style="background: #f3e5f5; padding: 1rem; border-radius: 8px; margin-top: 1rem;">
            <strong style="color: #7b1fa2;">Pods</strong>
        </div>
    </div>
</div>

<div class="concept-card">
    <h2>🚀 Gateway API - The Future of Kubernetes Networking</h2>
    <p>Gateway API is the next-generation API for managing ingress and service mesh traffic in Kubernetes. It provides a more expressive, extensible, and role-oriented API compared to Ingress.</p>
    
    <h3>Key Advantages Over Ingress</h3>
    <ul>
        <li><strong>Role-oriented</strong>: Separates concerns between infrastructure admins and app developers</li>
        <li><strong>Protocol support</strong>: HTTP, HTTPS, TCP, UDP, gRPC (not just L7)</li>
        <li><strong>Extensible</strong>: CRD-based, cleanly extensible without annotations</li>
        <li><strong>Portable</strong>: Standardized across implementations</li>
        <li><strong>Traffic management</strong>: Built-in support for A/B testing, canary deployments, traffic splitting</li>
    </ul>
</div>

<div class="concept-card">
    <h2>🏗️ Gateway API Resource Model</h2>
    <p>Gateway API introduces three core resources:</p>
    
    <table>
        <tr>
            <th>Resource</th>
            <th>Role</th>
            <th>Description</th>
        </tr>
        <tr>
            <td><code>GatewayClass</code></td>
            <td>Infrastructure</td>
            <td>Defines controller capabilities (e.g., NGINX, Cilium, Istio)</td>
        </tr>
        <tr>
            <td><code>Gateway</code></td>
            <td>Cluster Operator</td>
            <td>Instantiates a load balancer with specific configuration</td>
        </tr>
        <tr>
            <td><code>HTTPRoute</code></td>
            <td>App Developer</td>
            <td>Defines HTTP routing rules (replaces Ingress)</td>
        </tr>
    </table>
</div>

<div class="concept-card">
    <h2>📝 HTTPRoute Example</h2>
    <p><code>HTTPRoute</code> is the Gateway API equivalent of Ingress for HTTP traffic.</p>
    <pre><code>apiVersion: gateway.networking.k8s.io/v1
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
      port: 5000
    filters:
    - type: RequestHeaderModifier
      requestHeaderModifier:
        add:
        - name: X-Custom-Header
          value: "my-value"</code></pre>
</div>

<div class="concept-card">
    <h2>⚖️ Ingress vs Gateway API Comparison</h2>
    <table class="comparison-table">
        <tr>
            <th>Feature</th>
            <th>Ingress</th>
            <th>Gateway API</th>
        </tr>
        <tr>
            <td>Architecture</td>
            <td>Flat (single resource)</td>
            <td>Layered (GatewayClass → Gateway → Route)</td>
        </tr>
        <tr>
            <td>Extensibility</td>
            <td>Annotations (vendor-specific)</td>
            <td>CRD-based, standardized</td>
        </tr>
        <tr>
            <td>Protocol Support</td>
            <td>HTTP/HTTPS only</td>
            <td>HTTP, HTTPS, TCP, TLS, UDP, gRPC</td>
        </tr>
        <tr>
            <td>Role Separation</td>
            <td>Limited</td>
            <td>Built-in (Infra/Cluster/App roles)</td>
        </tr>
        <tr>
            <td>Traffic Management</td>
            <td>Basic routing</td>
            <td>Advanced (splitting, mirroring, retries)</td>
        </tr>
        <tr>
            <td>Portability</td>
            <td>Vendor-specific annotations</td>
            <td>Standardized across implementations</td>
        </tr>
    </table>
</div>

<div class="concept-card">
    <h2>🔗 Official Resources</h2>
    <div style="margin-top: 1rem;">
        <a href="https://kubernetes.io/docs/concepts/services-networking/ingress/" target="_blank" class="link-button">Ingress Documentation</a>
        <a href="https://gateway-api.sigs.k8s.io/" target="_blank" class="link-button">Gateway API Documentation</a>
        <a href="https://gateway-api.sigs.k8s.io/guides/http-routing/" target="_blank" class="link-button">HTTPRoute Guide</a>
    </div>
</div>
"""

ALIBABA_ACK_PAGE = """
<h1 style="color: #667eea; margin-bottom: 2rem; text-align: center;">☁️ Alibaba Cloud Container Service for Kubernetes (ACK)</h1>

<div class="concept-card">
    <h2>📖 What is Alibaba ACK?</h2>
    <p>Alibaba Cloud Container Service for Kubernetes (ACK) is a fully managed Kubernetes service that integrates with Alibaba Cloud's virtualization, storage, networking, and security capabilities to provide high-performance and scalable container applications.</p>
    
    <h3>Key Benefits</h3>
    <ul>
        <li>Fully managed Kubernetes control plane</li>
        <li>High availability across multiple zones</li>
        <li>Deep integration with Alibaba Cloud services (VPC, SLB, OSS, NAS, etc.)</li>
        <li>Built-in security and compliance features</li>
        <li>Auto-scaling and disaster recovery</li>
        <li>Managed cluster upgrades and patches</li>
    </ul>
</div>

<div class="concept-card">
    <h2>🏗️ ACK Architecture</h2>
    <p>ACK manages the entire control plane while you manage worker nodes. The architecture includes:</p>
    
    <h3>Managed Control Plane</h3>
    <ul>
        <li>At least 2 <code>kube-apiserver</code> instances</li>
        <li>3 <code>etcd</code> instances deployed across zones</li>
        <li><code>kube-controller-manager</code> and <code>kube-scheduler</code></li>
        <li>Alibaba Cloud Controller Manager for cloud integration</li>
    </ul>
    
    <h3>Worker Nodes</h3>
    <ul>
        <li>ECS instances or Elastic Container Instance (ECI) for serverless</li>
        <li>Support for GPU, FPGA, and ARM instances</li>
        <li>Auto-scaling based on metrics or schedule</li>
    </ul>
</div>

<div class="architecture-diagram">
    <h3 style="color: #667eea; margin-bottom: 1.5rem;">ACK Service Architecture</h3>
    <div style="margin: 2rem 0; text-align: left;">
        <div style="background: #fff3e0; padding: 1.5rem; border-radius: 8px; margin-bottom: 1rem;">
            <strong style="color: #e65100;">🎯 Alibaba Cloud Services Integration</strong><br><br>
            <div class="component-box" style="border-color: #e65100; font-size: 0.9rem;">VPC</div>
            <div class="component-box" style="border-color: #e65100; font-size: 0.9rem;">SLB</div>
            <div class="component-box" style="border-color: #e65100; font-size: 0.9rem;">OSS</div>
            <div class="component-box" style="border-color: #e65100; font-size: 0.9rem;">NAS</div>
            <div class="component-box" style="border-color: #e65100; font-size: 0.9rem;">ACR</div>
        </div>
        <div style="font-size: 2rem; text-align: center;">⬇️</div>
        <div style="background: #e3f2fd; padding: 1.5rem; border-radius: 8px; margin: 1rem 0;">
            <strong style="color: #1976d2;">ACK Managed Control Plane</strong><br><br>
            <div class="component-box" style="border-color: #1976d2; font-size: 0.9rem;">API Server (HA)</div>
            <div class="component-box" style="border-color: #1976d2; font-size: 0.9rem;">etcd (3 nodes)</div>
            <div class="component-box" style="border-color: #1976d2; font-size: 0.9rem;">Scheduler</div>
            <div class="component-box" style="border-color: #1976d2; font-size: 0.9rem;">Controllers</div>
        </div>
        <div style="font-size: 2rem; text-align: center;">⬇️</div>
        <div style="background: #f3e5f5; padding: 1.5rem; border-radius: 8px; margin-top: 1rem;">
            <strong style="color: #7b1fa2;">Worker Nodes (Your ECS Instances)</strong><br><br>
            <div class="component-box" style="border-color: #7b1fa2; font-size: 0.9rem;">kubelet</div>
            <div class="component-box" style="border-color: #7b1fa2; font-size: 0.9rem;">Container Runtime</div>
            <div class="component-box" style="border-color: #7b1fa2; font-size: 0.9rem;">Your Applications</div>
        </div>
    </div>
</div>

<div class="concept-card">
    <h2>🚀 ACK Cluster Types</h2>
    <table>
        <tr>
            <th>Type</th>
            <th>Description</th>
            <th>Use Case</th>
        </tr>
        <tr>
            <td><strong>Managed Kubernetes</strong></td>
            <td>Alibaba manages control plane, you manage worker nodes</td>
            <td>Production workloads with full control</td>
        </tr>
        <tr>
            <td><strong>Serverless Kubernetes (ASK)</strong></td>
            <td>No need to manage nodes, pay per pod</td>
            <td>Burst workloads, cost optimization</td>
        </tr>
        <tr>
            <td><strong>Dedicated Kubernetes</strong></td>
            <td>Full control over control plane and worker nodes</td>
            <td>Regulated industries, custom requirements</td>
        </tr>
        <tr>
            <td><strong>Edge Kubernetes</strong></td>
            <td>Extends K8s to edge locations</td>
            <td>IoT, CDN, edge computing</td>
        </tr>
    </table>
</div>

<div class="concept-card">
    <h2>🔧 ACK Key Features</h2>
    
    <h3>Networking</h3>
    <ul>
        <li><strong>Terway</strong>: High-performance CNI plugin for VPC networking</li>
        <li><strong>Flannel</strong>: Standard overlay networking</li>
        <li>Network Policy support for pod-to-pod security</li>
        <li>Integration with SLB for load balancing</li>
    </ul>
    
    <h3>Storage</h3>
    <ul>
        <li><strong>Cloud Disk</strong>: Block storage (SSD, ESSD, Ultra)</li>
        <li><strong>NAS</strong>: Network Attached Storage for shared volumes</li>
        <li><strong>OSS</strong>: Object storage integration</li>
        <li>Dynamic volume provisioning with CSI drivers</li>
    </ul>
    
    <h3>Auto Scaling</h3>
    <ul>
        <li><strong>HPA</strong>: Horizontal Pod Autoscaler based on metrics</li>
        <li><strong>VPA</strong>: Vertical Pod Autoscaler for resource optimization</li>
        <li><strong>Cluster Autoscaler</strong>: Auto scale nodes based on demand</li>
        <li>Scheduled scaling for predictable workloads</li>
    </ul>
    
    <h3>Observability</h3>
    <ul>
        <li>Integration with Alibaba Cloud Monitor</li>
        <li>Built-in logging with Log Service (SLS)</li>
        <li>Application Real-Time Monitoring Service (ARMS)</li>
        <li>Prometheus and Grafana support</li>
    </ul>
</div>

<div class="concept-card">
    <h2>🔐 ACK Security Features</h2>
    <ul>
        <li><strong>RAM</strong>: Role-based access control integration</li>
        <li><strong>Security Center</strong>: Runtime security scanning</li>
        <li><strong>KMS</strong>: Encryption for secrets at rest</li>
        <li><strong>Security Groups</strong>: Network-level firewall rules</li>
        <li><strong>Pod Security Policies</strong>: Control pod privileges</li>
        <li>Regular security patches and CVE fixes</li>
    </ul>
</div>

<div class="concept-card">
    <h2>💡 ACK Best Practices</h2>
    <ul>
        <li>Use managed clusters for easier operations</li>
        <li>Deploy across multiple zones for high availability</li>
        <li>Use Terway CNI for better network performance</li>
        <li>Enable cluster autoscaling for cost optimization</li>
        <li>Implement pod security policies</li>
        <li>Use ACR (Alibaba Container Registry) for faster image pulls</li>
        <li>Monitor with ARMS and Log Service</li>
        <li>Use Node pools for different workload types</li>
    </ul>
</div>

<div class="concept-card">
    <h2>🔗 Official Resources</h2>
    <div style="margin-top: 1rem;">
        <a href="https://www.alibabacloud.com/product/kubernetes" target="_blank" class="link-button">ACK Product Page</a>
        <a href="https://www.alibabacloud.com/help/container-service-for-kubernetes" target="_blank" class="link-button">ACK Documentation</a>
        <a href="https://www.alibabacloud.com/help/doc-detail/86745.htm" target="_blank" class="link-button">ACK Architecture</a>
    </div>
</div>
"""

DEVOPS_CONCEPTS = """
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
    return render_template_string(HOME_PAGE, version=VERSION, environment=ENVIRONMENT)

@app.route('/kubernetes')
def kubernetes():
    k8s_html = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', KUBERNETES_PAGE)
    return render_template_string(k8s_html, version=VERSION, environment=ENVIRONMENT)

@app.route('/ingress-gateway')
def ingress_gateway():
    ig_html = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', INGRESS_GATEWAY_PAGE)
    return render_template_string(ig_html, version=VERSION, environment=ENVIRONMENT)

@app.route('/alibaba-ack')
def alibaba_ack():
    ack_html = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', ALIBABA_ACK_PAGE)
    return render_template_string(ack_html, version=VERSION, environment=ENVIRONMENT)

@app.route('/devops-concepts')
def devops_concepts():
    concepts_html = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', DEVOPS_CONCEPTS)
    return render_template_string(concepts_html, version=VERSION, environment=ENVIRONMENT)

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
    
    info_html = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', f"""
    <h1 style="color: #667eea; margin-bottom: 2rem; text-align: center;">ℹ️ Deployment Information</h1>
    <div style="background: #f8f9fa; padding: 2rem; border-radius: 10px;">
        <table>
            {''.join([f'<tr><td style="font-weight: 600; color: #667eea;">{key.replace("_", " ").title()}</td><td>{value}</td></tr>' for key, value in deployment_info.items()])}
        </table>
    </div>
    <div style="margin-top: 2rem; padding: 1.5rem; background: #e8f5e9; border-left: 5px solid #4caf50; border-radius: 5px;">
        <strong style="color: #2e7d32;">✅ Status:</strong> Application is running successfully!
    </div>
    """)
    
    return render_template_string(info_html, version=VERSION, environment=ENVIRONMENT)

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
