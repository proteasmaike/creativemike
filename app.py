from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///tasks.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

db = SQLAlchemy(app)

# Database Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default='pending')  # pending, in_progress, completed
    priority = db.Column(db.String(50), default='medium')  # low, medium, high
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# Create tables
with app.app_context():
    db.create_all()

# Routes

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}), 200

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks with optional filtering"""
    status = request.args.get('status')
    priority = request.args.get('priority')
    
    query = Task.query
    
    if status:
        query = query.filter_by(status=status)
    if priority:
        query = query.filter_by(priority=priority)
    
    tasks = query.order_by(Task.created_at.desc()).all()
    return jsonify({
        'success': True,
        'count': len(tasks),
        'tasks': [task.to_dict() for task in tasks]
    }), 200

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get a single task by ID"""
    task = Task.query.get(task_id)
    
    if not task:
        return jsonify({'success': False, 'error': 'Task not found'}), 404
    
    return jsonify({
        'success': True,
        'task': task.to_dict()
    }), 200

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create a new task"""
    data = request.get_json()
    
    if not data or not data.get('title'):
        return jsonify({'success': False, 'error': 'Title is required'}), 400
    
    task = Task(
        title=data.get('title'),
        description=data.get('description'),
        status=data.get('status', 'pending'),
        priority=data.get('priority', 'medium')
    )
    
    db.session.add(task)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Task created successfully',
        'task': task.to_dict()
    }), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a task"""
    task = Task.query.get(task_id)
    
    if not task:
        return jsonify({'success': False, 'error': 'Task not found'}), 404
    
    data = request.get_json()
    
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'status' in data:
        task.status = data['status']
    if 'priority' in data:
        task.priority = data['priority']
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Task updated successfully',
        'task': task.to_dict()
    }), 200

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    task = Task.query.get(task_id)
    
    if not task:
        return jsonify({'success': False, 'error': 'Task not found'}), 404
    
    db.session.delete(task)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Task deleted successfully'
    }), 200

@app.route('/api/tasks/stats/summary', methods=['GET'])
def get_stats():
    """Get task statistics"""
    total_tasks = Task.query.count()
    completed = Task.query.filter_by(status='completed').count()
    pending = Task.query.filter_by(status='pending').count()
    in_progress = Task.query.filter_by(status='in_progress').count()
    
    return jsonify({
        'success': True,
        'stats': {
            'total': total_tasks,
            'completed': completed,
            'pending': pending,
            'in_progress': in_progress
        }
    }), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'success': False, 'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
