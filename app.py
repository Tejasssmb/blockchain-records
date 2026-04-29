"""
Flask backend for Blockchain Academic Record System
Provides REST API endpoints for managing academic records
With Metamask Web3 Integration
"""
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import uuid
from datetime import datetime
from blockchain import AcademicRecordBlockchain
import os
from functools import wraps

app = Flask(__name__)
CORS(app)

# Initialize blockchain
blockchain = AcademicRecordBlockchain(difficulty=2)

# In-memory database for student and institution info
students_db = {}
institutions_db = {}
# Metamask wallet tracking
metamask_wallets = {}  # Maps wallet address to student_id


@app.route('/')
def home():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Academic Record Blockchain System is running'})


# ==================== METAMASK ENDPOINTS ====================

@app.route('/api/metamask/connect', methods=['POST'])
def metamask_connect():
    """Connect Metamask wallet"""
    try:
        data = request.json
        wallet_address = data.get('walletAddress')
        # Handle both camelCase (from frontend) and snake_case
        student_id = data.get('studentId') or data.get('student_id')
        
        if not wallet_address or not student_id:
            return jsonify({'error': 'Missing wallet address or student ID'}), 400
        
        if student_id not in students_db:
            return jsonify({'error': 'Student not found'}), 404
        
        # Link wallet to student
        metamask_wallets[wallet_address] = student_id
        
        return jsonify({
            'success': True,
            'message': 'Metamask wallet connected successfully',
            'wallet_address': wallet_address,
            'student_id': student_id,
            'student_name': students_db[student_id]['name']
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/metamask/verify', methods=['POST'])
def metamask_verify():
    """Verify Metamask connection"""
    try:
        data = request.json
        wallet_address = data.get('walletAddress')
        
        if not wallet_address:
            return jsonify({'error': 'Missing wallet address'}), 400
        
        if wallet_address not in metamask_wallets:
            return jsonify({
                'connected': False,
                'message': 'Wallet not connected'
            }), 200
        
        student_id = metamask_wallets[wallet_address]
        student = students_db.get(student_id, {})
        
        return jsonify({
            'connected': True,
            'wallet_address': wallet_address,
            'student_id': student_id,
            'student_name': student.get('name', 'Unknown'),
            'message': 'Wallet verified'
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/metamask/wallet/<wallet_address>', methods=['GET'])
def get_wallet_info(wallet_address):
    """Get wallet information"""
    try:
        if wallet_address not in metamask_wallets:
            return jsonify({'error': 'Wallet not connected'}), 404
        
        student_id = metamask_wallets[wallet_address]
        student = students_db.get(student_id, {})
        records = blockchain.get_record_by_student_id(student_id)
        
        return jsonify({
            'wallet_address': wallet_address,
            'student_id': student_id,
            'student': student,
            'records_count': len(records),
            'records': records
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== STUDENT ENDPOINTS ====================

@app.route('/api/students/register', methods=['POST'])
def register_student():
    """Register a new student"""
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['name', 'email', 'roll_number', 'department']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        student_id = str(uuid.uuid4())
        
        student = {
            'student_id': student_id,
            'name': data['name'],
            'email': data['email'],
            'roll_number': data['roll_number'],
            'department': data['department'],
            'registered_at': datetime.now().isoformat()
        }
        
        students_db[student_id] = student
        
        return jsonify({
            'success': True,
            'message': 'Student registered successfully',
            'student': student
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/students/<student_id>', methods=['GET'])
def get_student(student_id):
    """Get student information"""
    if student_id not in students_db:
        return jsonify({'error': 'Student not found'}), 404
    
    return jsonify(students_db[student_id]), 200


@app.route('/api/students', methods=['GET'])
def list_students():
    """List all registered students"""
    return jsonify(list(students_db.values())), 200


# ==================== INSTITUTION ENDPOINTS ====================

@app.route('/api/institutions/register', methods=['POST'])
def register_institution():
    """Register a new institution"""
    try:
        data = request.json
        
        required_fields = ['name', 'code', 'email']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        institution_id = str(uuid.uuid4())
        
        institution = {
            'institution_id': institution_id,
            'name': data['name'],
            'code': data['code'],
            'email': data['email'],
            'registered_at': datetime.now().isoformat()
        }
        
        institutions_db[institution_id] = institution
        
        return jsonify({
            'success': True,
            'message': 'Institution registered successfully',
            'institution': institution
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/institutions', methods=['GET'])
def list_institutions():
    """List all registered institutions"""
    return jsonify(list(institutions_db.values())), 200


# ==================== ACADEMIC RECORD ENDPOINTS ====================

@app.route('/api/records/add', methods=['POST'])
def add_record():
    """Add a new academic record"""
    try:
        data = request.json
        
        required_fields = ['student_id', 'course_name', 'grade', 'credits', 'semester']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Verify student exists
        if data['student_id'] not in students_db:
            return jsonify({'error': 'Student not found'}), 404
        
        record = {
            'record_id': str(uuid.uuid4()),
            'student_id': data['student_id'],
            'course_name': data['course_name'],
            'grade': data['grade'],
            'credits': data['credits'],
            'semester': data['semester'],
            'issued_by': data.get('issued_by', 'default_institution'),
            'created_at': datetime.now().isoformat()
        }
        
        blockchain.add_record(record)
        
        return jsonify({
            'success': True,
            'message': 'Record added to pending pool',
            'record': record
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/records/mine', methods=['POST'])
def mine_records():
    """Mine pending records into the blockchain"""
    try:
        data = request.json
        miner_id = data.get('miner_id', 'system')
        
        if not blockchain.pending_records:
            return jsonify({'error': 'No pending records to mine'}), 400
        
        block = blockchain.mine_pending_records(miner_id)
        
        return jsonify({
            'success': True,
            'message': 'Records mined successfully',
            'block': block.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/records/student/<student_id>', methods=['GET'])
def get_student_records(student_id):
    """Get all academic records for a student"""
    try:
        records = blockchain.get_record_by_student_id(student_id)
        
        return jsonify({
            'student_id': student_id,
            'records': records,
            'total_records': len(records)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/records/<record_id>', methods=['GET'])
def get_record(record_id):
    """Get a specific record by ID"""
    try:
        record = blockchain.get_record_by_id(record_id)
        
        if not record:
            return jsonify({'error': 'Record not found'}), 404
        
        return jsonify(record), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/records/verify/<record_id>', methods=['GET'])
def verify_record(record_id):
    """Verify the authenticity of a record"""
    try:
        result = blockchain.verify_record(record_id)
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== BLOCKCHAIN ENDPOINTS ====================

@app.route('/api/blockchain/chain', methods=['GET'])
def get_chain():
    """Get the entire blockchain"""
    try:
        chain_data = blockchain.get_chain_data()
        return jsonify({
            'chain': chain_data,
            'length': len(chain_data)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/blockchain/validate', methods=['GET'])
def validate_blockchain():
    """Validate the blockchain integrity"""
    try:
        is_valid = blockchain.is_chain_valid()
        return jsonify({
            'valid': is_valid,
            'message': 'Blockchain is intact' if is_valid else 'Blockchain has been tampered with'
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/blockchain/stats', methods=['GET'])
def get_stats():
    """Get blockchain statistics"""
    try:
        stats = blockchain.get_statistics()
        return jsonify(stats), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/blockchain/pending', methods=['GET'])
def get_pending():
    """Get pending records"""
    return jsonify({
        'pending_records': blockchain.pending_records,
        'count': len(blockchain.pending_records)
    }), 200


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    import os
    print("Starting Academic Record Blockchain System...")
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False') == 'True'
    print(f"Server running on port {port}")
    app.run(debug=debug, host='0.0.0.0', port=port)
