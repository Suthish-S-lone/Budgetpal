import os
from functools import wraps
import firebase_admin
from firebase_admin import credentials, firestore, auth
from flask import Flask, jsonify, request, g
from dotenv import load_dotenv
from datetime import datetime
from flask_cors import CORS 

# Load environment variables from .env file
load_dotenv()

# Initialize Flask App
app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:5000",
            "http://127.0.0.1:5000",
            "https://suthish-s-lone.github.io"  # Replace with your actual GitHub Pages URL
        ],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# --- Firestore Initialization ---
try:
    if os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON'):
        import json
        service_account_info = json.loads(os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON'))
        cred = credentials.Certificate(service_account_info)
        firebase_admin.initialize_app(cred)
    else:
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred)
    print("✅ Successfully connected to Firestore")
except Exception as e:
    print(f"🔥 Failed to connect to Firestore: {e}")

db = firestore.client()

# --- Authentication Decorator ---
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'message': 'Authorization header is missing or invalid'}), 401
        
        id_token = auth_header.split('Bearer ')[1]
        try:
            decoded_token = auth.verify_id_token(id_token, check_revoked=True)
            g.user = decoded_token
        except auth.RevokedIdTokenError:
            return jsonify({'message': 'Token has been revoked'}), 401
        except auth.InvalidIdTokenError:
            return jsonify({'message': 'Token is invalid'}), 401
        except Exception as e:
            return jsonify({'message': 'An unknown error occurred', 'error': str(e)}), 500
        
        return f(*args, **kwargs)
    return decorated_function

# --- Helper Functions ---
def verify_resource_ownership(collection_name, document_id, user_id):
    """Verify that a resource belongs to the authenticated user"""
    doc_ref = db.collection(collection_name).document(document_id)
    doc = doc_ref.get()
    
    if not doc.exists:
        return None, jsonify({'message': f'{collection_name.capitalize()[:-1]} not found'}), 404
    
    if doc.to_dict().get('userId') != user_id:
        return None, jsonify({'message': 'Forbidden: You do not own this resource'}), 403
    
    return doc_ref, doc, 200

def verify_group_ownership(group_id, user_id):
    """Verify that a group belongs to the authenticated user"""
    doc_ref = db.collection('groups').document(group_id)
    doc = doc_ref.get()
    
    if not doc.exists:
        return None, jsonify({'message': 'Group not found'}), 404
    
    if doc.to_dict().get('ownerId') != user_id:
        return None, jsonify({'message': 'Forbidden: You are not the owner of this group'}), 403
    
    return doc_ref, doc, 200

# --- Routes ---
@app.route("/")
def index():
    return jsonify({"status": "ok", "message": "BudgetPal API is running!"})

# --- Expense Routes ---
@app.route("/expenses", methods=['POST'])
@token_required
def add_expense():
    try:
        data = request.get_json()
        user_id = g.user['uid']
        
        expense_data = {
            'userId': user_id,
            'description': data['description'],
            'amount': float(data['amount']),
            'category': data['category'],
            'date': datetime.now().isoformat(),
            'groupId': data.get('groupId'),
            'paidBy': data.get('paidBy') 
        }

        update_time, doc_ref = db.collection('expenses').add(expense_data)
        return jsonify({'id': doc_ref.id, **expense_data}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route("/expenses", methods=['GET'])
@token_required
def get_expenses():
    user_id = g.user['uid']
    expenses_ref = db.collection('expenses').where('userId', '==', user_id).order_by('date', direction=firestore.Query.DESCENDING)
    results = expenses_ref.stream()
    
    expenses_list = []
    for doc in results:
        expense_data = doc.to_dict()
        expense_data['id'] = doc.id
        expenses_list.append(expense_data)
        
    return jsonify(expenses_list), 200

@app.route("/expenses/<expense_id>", methods=['PUT'])
@token_required
def update_expense(expense_id):
    try:
        doc_ref, doc, status_code = verify_resource_ownership('expenses', expense_id, g.user['uid'])
        if status_code != 200:
            return doc, status_code

        data = request.get_json()
        doc_ref.update(data)
        
        updated_expense = doc_ref.get().to_dict()
        updated_expense['id'] = doc_ref.id
        
        return jsonify(updated_expense), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route("/expenses/<expense_id>", methods=['DELETE'])
@token_required
def delete_expense(expense_id):
    try:
        doc_ref, doc, status_code = verify_resource_ownership('expenses', expense_id, g.user['uid'])
        if status_code != 200:
            return doc, status_code

        doc_ref.delete()
        return jsonify({'message': 'Expense deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- Budget Routes ---
@app.route("/budgets", methods=['POST'])
@token_required
def add_budget():
    try:
        data = request.get_json()
        user_id = g.user['uid']
        
        budget_data = {
            'userId': user_id,
            'category': data['category'],
            'amount': float(data['amount']),
            'createdAt': datetime.now().isoformat()
        }

        update_time, doc_ref = db.collection('budgets').add(budget_data)
        return jsonify({'id': doc_ref.id, **budget_data}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route("/budgets", methods=['GET'])
@token_required
def get_budgets():
    user_id = g.user['uid']
    budgets_ref = db.collection('budgets').where('userId', '==', user_id)
    results = budgets_ref.stream()
    
    budgets_list = []
    for doc in results:
        budget_data = doc.to_dict()
        budget_data['id'] = doc.id
        budgets_list.append(budget_data)
        
    return jsonify(budgets_list), 200

@app.route("/budgets/<budget_id>", methods=['PUT'])
@token_required
def update_budget(budget_id):
    try:
        doc_ref, doc, status_code = verify_resource_ownership('budgets', budget_id, g.user['uid'])
        if status_code != 200:
            return doc, status_code

        data = request.get_json()
        doc_ref.update({'amount': float(data['amount'])})
        
        updated_budget = doc_ref.get().to_dict()
        updated_budget['id'] = doc_ref.id
        
        return jsonify(updated_budget), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route("/budgets/<budget_id>", methods=['DELETE'])
@token_required
def delete_budget(budget_id):
    try:
        doc_ref, doc, status_code = verify_resource_ownership('budgets', budget_id, g.user['uid'])
        if status_code != 200:
            return doc, status_code

        doc_ref.delete()
        return jsonify({'message': 'Budget deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- Group Routes ---
@app.route("/groups", methods=['POST'])
@token_required
def create_group():
    try:
        data = request.get_json()
        creator_id = g.user['uid']
        group_name = data['name']
        member_emails = data.get('members', [])

        member_ids = {creator_id}
        for email in member_emails:
            try:
                user = auth.get_user_by_email(email)
                member_ids.add(user.uid)
            except auth.UserNotFoundError:
                print(f"Warning: User with email {email} not found.")
                continue
        
        group_data = {
            'name': group_name,
            'members': list(member_ids),
            'ownerId': creator_id,
            'createdAt': datetime.now().isoformat()
        }

        update_time, doc_ref = db.collection('groups').add(group_data)
        return jsonify({'id': doc_ref.id, **group_data}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route("/groups", methods=['GET'])
@token_required
def get_groups():
    user_id = g.user['uid']
    groups_ref = db.collection('groups').where('members', 'array_contains', user_id)
    results = groups_ref.stream()
    
    groups_list = []
    for doc in results:
        group_data = doc.to_dict()
        group_data['id'] = doc.id
        
        # Fetch member details
        member_details = []
        if 'members' in group_data:
            for member_uid in group_data['members']:
                try:
                    user_record = auth.get_user(member_uid)
                    member_details.append({
                        'uid': user_record.uid,
                        'displayName': user_record.display_name,
                        'email': user_record.email
                    })
                except auth.UserNotFoundError:
                    member_details.append({'uid': member_uid, 'displayName': 'Unknown User'})
        
        group_data['members'] = member_details
        groups_list.append(group_data)
        
    return jsonify(groups_list), 200

@app.route("/groups/<group_id>", methods=['DELETE'])
@token_required
def delete_group(group_id):
    try:
        doc_ref, doc, status_code = verify_group_ownership(group_id, g.user['uid'])
        if status_code != 200:
            return doc, status_code

        doc_ref.delete()
        return jsonify({'message': 'Group deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- Income Routes ---
@app.route("/incomes", methods=['POST'])
@token_required
def add_income():
    try:
        data = request.get_json()
        user_id = g.user['uid']
        
        income_data = {
            'userId': user_id,
            'source': data['source'],
            'amount': float(data['amount']),
            'recurrence': data['recurrence'],
            'createdAt': datetime.now().isoformat()
        }

        update_time, doc_ref = db.collection('incomes').add(income_data)
        return jsonify({'id': doc_ref.id, **income_data}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route("/incomes", methods=['GET'])
@token_required
def get_incomes():
    user_id = g.user['uid']
    incomes_ref = db.collection('incomes').where('userId', '==', user_id)
    results = incomes_ref.stream()
    
    incomes_list = []
    for doc in results:
        income_data = doc.to_dict()
        income_data['id'] = doc.id
        incomes_list.append(income_data)
        
    return jsonify(incomes_list), 200

@app.route("/incomes/<income_id>", methods=['DELETE'])
@token_required
def delete_income(income_id):
    try:
        doc_ref, doc, status_code = verify_resource_ownership('incomes', income_id, g.user['uid'])
        if status_code != 200:
            return doc, status_code

        doc_ref.delete()
        return jsonify({'message': 'Income source deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port)