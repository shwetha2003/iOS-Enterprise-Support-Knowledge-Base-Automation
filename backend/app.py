#!/usr/bin/env python3
"""
iOS Enterprise Support Portal - Backend API
Flask application serving knowledge base and automation tools
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import json
from datetime import datetime

# Import custom modules
from scripts.network_validator import NetworkValidator
from scripts.mdm_checker import MDMComplianceChecker
from scripts.storage_cleaner import StorageAnalyzer

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Rate limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

# Configuration
app.config['JSON_SORT_KEYS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

# Load knowledge base data
def load_knowledge_base():
    try:
        with open('data/knowledge_base.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Return sample data if file doesn't exist
        return {
            "articles": [
                {
                    "id": 1,
                    "title": "Cannot connect to corporate email",
                    "category": "Email",
                    "difficulty": "Easy",
                    "time": "5 minutes",
                    "views": 1245,
                    "last_updated": "2024-01-15",
                    "content": {
                        "problem": "Email app shows 'Cannot connect to server' error",
                        "solution_steps": [
                            "Check internet connection (Wi-Fi or cellular)",
                            "Force quit the Mail app and restart",
                            "Remove and re-add email account in Settings",
                            "Verify server settings with IT department"
                        ],
                        "related_scripts": ["network_validator"],
                        "tags": ["email", "connection", "exchange"]
                    }
                },
                {
                    "id": 2,
                    "title": "MDM profile installation failed",
                    "category": "Security",
                    "difficulty": "Medium",
                    "time": "10 minutes",
                    "views": 892,
                    "last_updated": "2024-01-10",
                    "content": {
                        "problem": "Error message: 'Profile installation failed. Could not verify'",
                        "solution_steps": [
                            "Ensure device is connected to corporate network",
                            "Update iOS to latest version",
                            "Clear Safari cache and cookies",
                            "Contact IT for new enrollment link"
                        ],
                        "related_scripts": ["mdm_checker"],
                        "tags": ["mdm", "profile", "enrollment"]
                    }
                }
            ],
            "categories": ["Email", "Wi-Fi", "VPN", "MDM", "Apps", "Security", "General"]
        }

# Load analytics data
def load_analytics():
    return {
        "tickets_reduced": 342,
        "deflection_rate": "68%",
        "top_issues": [
            {"issue": "Email setup", "count": 245},
            {"issue": "VPN connection", "count": 189},
            {"issue": "App crashes", "count": 156},
            {"issue": "Storage full", "count": 123},
            {"issue": "MDM issues", "count": 98}
        ],
        "monthly_trend": [
            {"month": "Oct", "tickets": 189, "deflected": 120},
            {"month": "Nov", "tickets": 156, "deflected": 102},
            {"month": "Dec", "tickets": 134, "deflected": 92},
            {"month": "Jan", "tickets": 121, "deflected": 82}
        ]
    }

# Routes
@app.route('/')
def index():
    """API root endpoint"""
    return jsonify({
        "name": "iOS Enterprise Support Portal API",
        "version": "1.0.0",
        "endpoints": {
            "/api/knowledge-base": "Search knowledge base articles",
            "/api/run-script/<script_name>": "Run automation scripts",
            "/api/dashboard": "Get analytics dashboard data",
            "/api/submit-feedback": "Submit user feedback"
        }
    })

@app.route('/api/knowledge-base', methods=['GET'])
def get_knowledge_base():
    """Get knowledge base articles with optional search"""
    kb_data = load_knowledge_base()
    
    # Search functionality
    search_query = request.args.get('q', '').lower()
    category_filter = request.args.get('category', '')
    
    if search_query or category_filter:
        filtered_articles = []
        for article in kb_data['articles']:
            matches_search = (
                not search_query or
                search_query in article['title'].lower() or
                search_query in ' '.join(article['content']['tags']).lower()
            )
            matches_category = (
                not category_filter or
                category_filter == article['category']
            )
            
            if matches_search and matches_category:
                filtered_articles.append(article)
        
        response = {
            "articles": filtered_articles,
            "total": len(filtered_articles),
            "categories": kb_data['categories']
        }
    else:
        response = {
            "articles": kb_data['articles'],
            "total": len(kb_data['articles']),
            "categories": kb_data['categories']
        }
    
    return jsonify(response)

@app.route('/api/knowledge-base/<int:article_id>', methods=['GET'])
def get_article(article_id):
    """Get specific article by ID"""
    kb_data = load_knowledge_base()
    
    for article in kb_data['articles']:
        if article['id'] == article_id:
            # Increment view count (in memory)
            article['views'] = article.get('views', 0) + 1
            return jsonify(article)
    
    return jsonify({"error": "Article not found"}), 404

@app.route('/api/run-script/<script_name>', methods=['POST'])
@limiter.limit("10 per minute")
def run_script(script_name):
    """Run automation scripts"""
    try:
        data = request.get_json() or {}
        device_id = data.get('device_id', f"user-{datetime.now().timestamp()}")
        
        if script_name == 'network_validator':
            validator = NetworkValidator(device_id)
            result = validator.generate_health_report()
            
        elif script_name == 'mdm_checker':
            checker = MDMComplianceChecker(device_id)
            result = checker.run_compliance_check()
            
        elif script_name == 'storage_cleaner':
            analyzer = StorageAnalyzer(device_id)
            result = analyzer.identify_storage_issues()
            
        else:
            return jsonify({
                "error": "Script not found",
                "available_scripts": ["network_validator", "mdm_checker", "storage_cleaner"]
            }), 404
        
        # Log script execution
        log_execution(script_name, device_id, "success")
        
        return jsonify({
            "success": True,
            "script": script_name,
            "device_id": device_id,
            "timestamp": datetime.now().isoformat(),
            "result": result
        })
        
    except Exception as e:
        log_execution(script_name, device_id, f"error: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    """Get dashboard analytics"""
    analytics = load_analytics()
    
    # Add script usage statistics
    script_stats = [
        {"name": "Network Validator", "runs": 245, "success_rate": 92},
        {"name": "MDM Checker", "runs": 189, "success_rate": 88},
        {"name": "Storage Cleaner", "runs": 312, "success_rate": 95}
    ]
    
    return jsonify({
        "analytics": analytics,
        "script_usage": script_stats,
        "system_status": {
            "knowledge_base_articles": 25,
            "active_users_today": 42,
            "average_resolution_time": "12 minutes",
            "user_satisfaction": 4.7
        }
    })

@app.route('/api/submit-feedback', methods=['POST'])
def submit_feedback():
    """Submit user feedback"""
    data = request.get_json()
    
    if not data or 'rating' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    feedback = {
        "id": datetime.now().timestamp(),
        "rating": data['rating'],
        "comment": data.get('comment', ''),
        "article_id": data.get('article_id'),
        "timestamp": datetime.now().isoformat(),
        "user_agent": request.headers.get('User-Agent', '')
    }
    
    # In production, save to database
    print(f"Feedback received: {feedback}")
    
    return jsonify({
        "success": True,
        "message": "Thank you for your feedback!",
        "feedback_id": feedback['id']
    })

@app.route('/api/search-suggestions', methods=['GET'])
def search_suggestions():
    """Get search suggestions"""
    query = request.args.get('q', '').lower()
    
    if not query:
        return jsonify({"suggestions": []})
    
    kb_data = load_knowledge_base()
    suggestions = []
    
    for article in kb_data['articles']:
        if query in article['title'].lower():
            suggestions.append({
                "text": article['title'],
                "category": article['category'],
                "id": article['id']
            })
    
    # Add common searches
    common_searches = [
        "email setup", "vpn connect", "app crash", "storage full",
        "wifi password", "mdm profile", "ios update", "backup"
    ]
    
    for search in common_searches:
        if query in search:
            suggestions.append({
                "text": search,
                "category": "Common Search",
                "type": "search_term"
            })
    
    return jsonify({"suggestions": suggestions[:5]})

def log_execution(script_name, device_id, status):
    """Log script execution for analytics"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "script": script_name,
        "device_id": device_id,
        "status": status,
        "ip_address": request.remote_addr
    }
    
    # In production, save to database or log file
    print(f"Script execution: {log_entry}")

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(429)
def ratelimit_handler(error):
    return jsonify({
        "error": "Rate limit exceeded",
        "message": "Please try again in a few minutes"
    }), 429

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
