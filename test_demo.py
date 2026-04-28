"""
Test and Demo Script for Blockchain Academic Record System
This script demonstrates how to interact with the blockchain system programmatically
"""

import requests
import json
import time

# API Configuration
API_URL = "http://localhost:5000/api"

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")

def print_json(data, indent=2):
    """Pretty print JSON data"""
    print(json.dumps(data, indent=indent, default=str))

# ==================== DEMO FUNCTIONS ====================

def demo_health_check():
    """Check if the system is healthy"""
    print_section("1. HEALTH CHECK")
    try:
        response = requests.get(f"{API_URL}/health")
        print_json(response.json())
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_register_students():
    """Register sample students"""
    print_section("2. REGISTER STUDENTS")
    
    students_data = [
        {
            "name": "Alice Johnson",
            "email": "alice@university.edu",
            "roll_number": "2024001",
            "department": "Computer Science"
        },
        {
            "name": "Bob Smith",
            "email": "bob@university.edu",
            "roll_number": "2024002",
            "department": "Computer Science"
        },
        {
            "name": "Charlie Brown",
            "email": "charlie@university.edu",
            "roll_number": "2024003",
            "department": "Information Technology"
        }
    ]
    
    student_ids = []
    
    for student in students_data:
        try:
            response = requests.post(f"{API_URL}/students/register", json=student)
            data = response.json()
            
            if response.status_code == 201:
                print(f"✓ Registered: {student['name']}")
                student_ids.append(data['student']['student_id'])
            else:
                print(f"❌ Failed: {student['name']}")
                print_json(data)
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return student_ids

def demo_list_students():
    """List all registered students"""
    print_section("3. LIST ALL STUDENTS")
    try:
        response = requests.get(f"{API_URL}/students")
        students = response.json()
        print(f"Total Students: {len(students)}\n")
        
        for student in students:
            print(f"  ID: {student['student_id'][:8]}...")
            print(f"  Name: {student['name']}")
            print(f"  Roll: {student['roll_number']}")
            print(f"  Dept: {student['department']}\n")
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_add_records(student_ids):
    """Add academic records for students"""
    print_section("4. ADD ACADEMIC RECORDS")
    
    if not student_ids:
        print("❌ No students found. Register students first.")
        return
    
    records_data = [
        {
            "student_id": student_ids[0],
            "course_name": "Data Structures",
            "grade": "A+",
            "credits": 4,
            "semester": "Fall 2024"
        },
        {
            "student_id": student_ids[0],
            "course_name": "Database Management",
            "grade": "A",
            "credits": 4,
            "semester": "Fall 2024"
        },
        {
            "student_id": student_ids[1],
            "course_name": "Web Development",
            "grade": "A-",
            "credits": 3,
            "semester": "Fall 2024"
        },
        {
            "student_id": student_ids[1],
            "course_name": "Mobile Apps",
            "grade": "B+",
            "credits": 3,
            "semester": "Fall 2024"
        },
        {
            "student_id": student_ids[2],
            "course_name": "Machine Learning",
            "grade": "A",
            "credits": 4,
            "semester": "Fall 2024"
        }
    ]
    
    record_ids = []
    
    for record in records_data:
        try:
            response = requests.post(f"{API_URL}/records/add", json=record)
            data = response.json()
            
            if response.status_code == 201:
                print(f"✓ Added: {record['course_name']} for {record['student_id'][:8]}...")
                record_ids.append(data['record']['record_id'])
            else:
                print(f"❌ Failed: {record['course_name']}")
                print_json(data)
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return record_ids

def demo_view_pending():
    """View pending records"""
    print_section("5. VIEW PENDING RECORDS")
    try:
        response = requests.get(f"{API_URL}/blockchain/pending")
        data = response.json()
        
        print(f"Pending Records: {data['count']}\n")
        
        for i, record in enumerate(data['pending_records'], 1):
            print(f"Record {i}:")
            print(f"  Student: {record['student_id'][:8]}...")
            print(f"  Course: {record['course_name']}")
            print(f"  Grade: {record['grade']}")
            print(f"  Credits: {record['credits']}\n")
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_mine_records():
    """Mine pending records into blockchain"""
    print_section("6. MINE RECORDS")
    try:
        print("Mining pending records...")
        print("(This may take a few seconds due to Proof of Work)\n")
        
        response = requests.post(
            f"{API_URL}/records/mine",
            json={"miner_id": "demo_system"}
        )
        
        data = response.json()
        
        if response.status_code == 200:
            print("✓ Mining completed successfully!\n")
            print(f"Block Details:")
            print(f"  Index: {data['block']['index']}")
            print(f"  Hash: {data['block']['hash']}")
            print(f"  Previous Hash: {data['block']['previous_hash']}")
            print(f"  Nonce: {data['block']['nonce']}")
            print(f"  Records: {len(data['block']['data']['records'])}")
        else:
            print("❌ Failed to mine records")
            print_json(data)
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_view_blockchain():
    """View the entire blockchain"""
    print_section("7. VIEW BLOCKCHAIN")
    try:
        response = requests.get(f"{API_URL}/blockchain/chain")
        data = response.json()
        
        print(f"Total Blocks: {data['length']}\n")
        
        for block in data['chain']:
            print(f"Block #{block['index']}:")
            print(f"  Hash: {block['hash']}")
            print(f"  Previous: {block['previous_hash']}")
            print(f"  Nonce: {block['nonce']}")
            
            if block['data'].get('type') == 'genesis':
                print(f"  Type: Genesis Block")
            else:
                print(f"  Records: {len(block['data']['records'])}")
            print()
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_get_student_records(student_ids):
    """Get all records for a specific student"""
    print_section("8. GET STUDENT RECORDS")
    
    if not student_ids:
        print("❌ No students found.")
        return
    
    student_id = student_ids[0]
    
    try:
        response = requests.get(f"{API_URL}/records/student/{student_id}")
        data = response.json()
        
        print(f"Student: {student_id[:8]}...")
        print(f"Total Records: {data['total_records']}\n")
        
        for record in data['records']:
            print(f"Block #{record['block_index']}:")
            print(f"  Course: {record['record']['course_name']}")
            print(f"  Grade: {record['record']['grade']}")
            print(f"  Credits: {record['record']['credits']}")
            print(f"  Timestamp: {record['timestamp']}\n")
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_validate_blockchain():
    """Validate blockchain integrity"""
    print_section("9. VALIDATE BLOCKCHAIN")
    try:
        response = requests.get(f"{API_URL}/blockchain/validate")
        data = response.json()
        
        if data['valid']:
            print("✓ Blockchain is VALID")
            print("  All blocks are intact and no tampering detected")
        else:
            print("❌ Blockchain is INVALID")
            print("  Some blocks may have been tampered with")
        
        print(f"\nMessage: {data['message']}")
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_verify_record(record_ids):
    """Verify a specific record"""
    print_section("10. VERIFY RECORD")
    
    if not record_ids:
        print("❌ No records found.")
        return
    
    record_id = record_ids[0]
    
    try:
        response = requests.get(f"{API_URL}/records/verify/{record_id}")
        data = response.json()
        
        if data['verified']:
            print("✓ Record is VERIFIED")
            print(f"  Message: {data['message']}")
            print(f"  Record ID: {data['record']['record']['record_id']}")
            print(f"  Block: #{data['record']['block_index']}")
        else:
            print("❌ Record verification FAILED")
            print(f"  Message: {data['message']}")
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_get_statistics():
    """Get blockchain statistics"""
    print_section("11. BLOCKCHAIN STATISTICS")
    try:
        response = requests.get(f"{API_URL}/blockchain/stats")
        data = response.json()
        
        print(f"Total Blocks: {data['total_blocks']}")
        print(f"Total Records: {data['total_records']}")
        print(f"Pending Records: {data['pending_records']}")
        print(f"Chain Valid: {'Yes' if data['chain_valid'] else 'No'}")
    except Exception as e:
        print(f"❌ Error: {e}")

# ==================== MAIN DEMO ====================

def run_demo():
    """Run complete demo"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  Blockchain Academic Record System - Demo Script  ".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    print("\nMake sure the Flask server is running on http://localhost:5000")
    print("Start it with: python app.py\n")
    
    try:
        # Run demo steps
        demo_health_check()
        
        time.sleep(1)
        student_ids = demo_register_students()
        
        time.sleep(1)
        demo_list_students()
        
        time.sleep(1)
        record_ids = demo_add_records(student_ids)
        
        time.sleep(1)
        demo_view_pending()
        
        time.sleep(1)
        demo_mine_records()
        
        time.sleep(1)
        demo_view_blockchain()
        
        time.sleep(1)
        demo_get_student_records(student_ids)
        
        time.sleep(1)
        demo_validate_blockchain()
        
        time.sleep(1)
        demo_verify_record(record_ids)
        
        time.sleep(1)
        demo_get_statistics()
        
        print_section("✅ DEMO COMPLETED SUCCESSFULLY")
        print("The blockchain system is working correctly!")
        print("Now open http://localhost:5000 in your browser to use the web interface.")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to the server!")
        print("Make sure Flask is running: python app.py")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    run_demo()
