import os, re, datetime, urllib.parse
from flask import Flask, render_template_string

app = Flask(__name__)

def get_session_data():
    sessions_path = os.path.expanduser('~/Desktop/Sessions')
    results = []
    
    if not os.path.exists(sessions_path):
        return results

    for filename in sorted(os.listdir(sessions_path), reverse=True):
        if filename.startswith(('Session_', 'Tabs_')):
            file_path = os.path.join(sessions_path, filename)
            try:
                mtime = os.path.getmtime(file_path)
                timestamp = datetime.datetime.fromtimestamp(mtime).strftime('%I:%M %p - %b %d')
                
                with open(file_path, 'rb') as f:
                    data = f.read()
                    # Robust URL extraction from binary data
                    urls = re.findall(b'https?://[^\s\x00-\x1f\x7f-\xff]+', data)
                    
                    tab_list = []
                    seen = set()
                    for u in urls:
                        try:
                            # Clean up the URL string
                            url_str = u.decode('utf-8', 'ignore').rstrip(')"\'')
                            # Basic validation and deduplication
                            if url_str not in seen and "://google.com" not in url_str:
                                parsed = urllib.parse.urlparse(url_str)
                                if parsed.netloc:
                                    domain = parsed.netloc.replace('www.', '')
                                    tab_list.append({'url': url_str, 'domain': domain})
                                    seen.add(url_str)
                        except Exception:
                            continue
                    
                    if tab_list:
                        results.append({
                            'file': filename,
                            'time': timestamp,
                            'count': len(tab_list),
                            'tabs': tab_list
                        })
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                continue
    return results

@app.route('/')
def index():
    data = get_session_data()
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Chrome Recovery Pro</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>
            :root {
                --primary-color: #0d6efd;
                --bg-color: #f8f9fa;
                --card-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
            }
            body { 
                background: var(--bg-color); 
                font-family: 'Inter', sans-serif;
                color: #333;
                padding-bottom: 50px;
            }
            .header-section {
                background: white;
                padding: 40px 0;
                margin-bottom: 40px;
                border-bottom: 1px solid #eee;
                box-shadow: 0 2px 10px rgba(0,0,0,0.02);
            }
            .session-card { 
                border: none; 
                border-radius: 16px; 
                box-shadow: var(--card-shadow); 
                overflow: hidden;
                margin-bottom: 30px;
                background: white;
            }
            .card-header {
                background: #fff !important;
                border-bottom: 1px solid #f0f0f0 !important;
                padding: 20px 25px !important;
            }
            .tab-link { 
                text-decoration: none; 
                color: #2c3e50; 
                display: flex; 
                align-items: center; 
                gap: 12px; 
                padding: 10px 15px; 
                border-radius: 10px;
                transition: all 0.2s ease;
                border: 1px solid transparent;
            }
            .tab-link:hover { 
                background: #f0f7ff; 
                color: var(--primary-color);
                border-color: #d0e7ff;
            }
            .favicon { 
                width: 20px; 
                height: 20px; 
                border-radius: 4px; 
                flex-shrink: 0;
            }
            .badge-custom { 
                background: #e7f1ff; 
                color: #0d6efd; 
                font-weight: 600; 
                padding: 6px 14px;
                border-radius: 20px;
            }
            .domain-text {
                font-weight: 500;
                font-size: 0.95rem;
            }
            .url-text {
                font-size: 0.8rem;
                opacity: 0.6;
            }
            .refresh-btn {
                border-radius: 10px;
                padding: 8px 18px;
                font-weight: 500;
            }
        </style>
    </head>
    <body class="bg-light">
        <div class="header-section">
            <div class="container d-flex justify-content-between align-items-center">
                <div>
                    <h1 class="h2 fw-bold mb-1">Chrome Recovery Pro</h1>
                    <p class="text-muted mb-0">Recover your lost tabs from local session files</p>
                </div>
                <button onclick="window.location.reload()" class="btn btn-primary refresh-btn">
                    Refresh Files
                </button>
            </div>
        </div>

        <div class="container">
            {% for session in sessions %}
            <div class="card session-card">
                <div class="card-header d-flex justify-content-between align-items-center">
                    <div>
                        <h5 class="mb-1 fw-bold text-dark">📦 {{ session.file }}</h5>
                        <div class="d-flex align-items-center gap-2">
                            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" class="bi bi-clock text-muted" viewBox="0 0 16 16">
                                <path d="M8 3.5a.5.5 0 0 0-1 0V9a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 8.71V3.5z"/>
                                <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm7-8A7 7 0 1 1 1 8a7 7 0 0 1 14 0z"/>
                            </svg>
                            <small class="text-muted">{{ session.time }}</small>
                        </div>
                    </div>
                    <span class="badge-custom">{{ session.count }} Tabs Found</span>
                </div>
                <div class="card-body p-4">
                    <div class="row g-3">
                        {% for tab in session.tabs %}
                        <div class="col-lg-4 col-md-6">
                            <a href="{{ tab.url }}" target="_blank" class="tab-link h-100">
                                <img src="https://www.google.com/s2/favicons?domain={{ tab.domain }}&sz=32" class="favicon" alt="">
                                <div class="text-truncate">
                                    <div class="domain-text text-truncate">{{ tab.domain }}</div>
                                    <div class="url-text text-truncate">{{ tab.url }}</div>
                                </div>
                            </a>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>
            {% else %}
            <div class="text-center py-5">
                <div class="display-1 text-muted mb-4">📂</div>
                <h3>No session files found</h3>
                <p class="text-muted">Make sure your Chrome session files are in the Desktop/Sessions folder.</p>
            </div>
            {% endfor %}
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template, sessions=data)

if __name__ == '__main__':
    print("🚀 Recovery App starting at http://127.0.0.1:5001")
    # Setting use_reloader=False to avoid issues in some environments
    app.run(port=5001, debug=True, use_reloader=False)
