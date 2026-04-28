# 🔗 Blockchain Based Academic Record System

A secure, transparent, and immutable academic record management system built with blockchain technology. This system allows institutions to create, store, verify, and share student academic records on a blockchain, ensuring data integrity and preventing tampering.

## 📋 Project Overview

This is a **miniproject** implementing a blockchain-based solution for academic records management. It demonstrates core blockchain concepts including:

- **Immutability**: Records cannot be altered once recorded
- **Transparency**: All transactions are visible and verifiable
- **Decentralization**: Records are distributed across blocks
- **Proof of Work**: Simple mining mechanism for block validation
- **Data Integrity**: Cryptographic hashing ensures authenticity

## ✨ Features

### 1. **Student Management**
- Register students with personal details
- Maintain student database
- View registered students

### 2. **Academic Records**
- Add course grades and credits
- Store records in blockchain
- Search records by student
- View complete academic history

### 3. **Blockchain Core**
- Custom Python blockchain implementation
- Mining (Proof of Work)
- Chain validation
- Block structure with hashing
- Immutable record storage

### 4. **Record Verification**
- Verify record authenticity
- Check blockchain integrity
- Confirm no tampering has occurred

### 5. **Web Dashboard**
- Intuitive user interface
- Real-time statistics
- Interactive blockchain viewer
- Record management tools

## 🛠️ Technology Stack

- **Backend**: Python, Flask, Flask-CORS
- **Blockchain**: Custom Python implementation
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Hashing**: SHA-256
- **Consensus**: Proof of Work (PoW)

## 📦 Project Structure

```
Blockchain Academic Record System/
│
├── blockchain.py              # Core blockchain implementation
├── app.py                     # Flask backend server
├── requirements.txt           # Python dependencies
├── README.md                  # This file
│
└── templates/
    └── index.html             # Frontend web interface
```

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Any modern web browser

### Installation

1. **Navigate to project directory**:
```bash
cd "Academic record Sysetem"
```

2. **Create a virtual environment** (recommended):
```bash
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

### Running the Application

1. **Start the Flask server**:
```bash
python app.py
```

The server will start at `http://localhost:5000`

2. **Open in browser**:
```
http://localhost:5000
```

## 📖 Usage Guide

### Dashboard
- View overall system statistics
- See total blocks, records, and pending transactions
- Mine pending records into the blockchain

### Student Management
- **Register Student**: Add a new student with name, email, roll number, and department
- **View Students**: See all registered students in the system

### Academic Records
- **Add Record**: Record a student's course grade
  - Need: Student ID, Course name, Grade, Credits, Semester
- **Search Records**: Find all records for a specific student
- **View History**: Complete academic transcript

### Blockchain Explorer
- **View Chain**: See all blocks in the blockchain
- **Validate Chain**: Verify blockchain integrity
- **View Pending**: See records waiting to be mined

### Record Verification
- **Verify Authenticity**: Paste a record ID to verify it's authentic
- **Check Tampering**: System will detect any changes to records

## 🔐 How It Works

### Blockchain Structure

Each block contains:
- **Index**: Block number in chain
- **Timestamp**: When block was created
- **Data**: Academic records in the block
- **Previous Hash**: Link to previous block (chain integrity)
- **Hash**: Current block's hash (SHA-256)
- **Nonce**: Proof of work counter

### Mining Process

1. Pending academic records are collected
2. A new block is created with these records
3. Proof of Work algorithm finds a valid hash (with leading zeros)
4. Block is added to the chain
5. Records become immutable

### Verification

To verify a record:
1. Find the record in the blockchain
2. Recalculate its hash
3. Check if it matches the stored hash
4. Verify chain integrity by checking all previous hashes
5. If all match, the record is authentic

## 📊 API Endpoints

### Health Check
- `GET /api/health` - Check server status

### Students
- `POST /api/students/register` - Register a new student
- `GET /api/students` - List all students
- `GET /api/students/<student_id>` - Get student details

### Academic Records
- `POST /api/records/add` - Add a new record
- `POST /api/records/mine` - Mine pending records
- `GET /api/records/student/<student_id>` - Get student's records
- `GET /api/records/<record_id>` - Get specific record
- `GET /api/records/verify/<record_id>` - Verify record

### Blockchain
- `GET /api/blockchain/chain` - Get entire blockchain
- `GET /api/blockchain/validate` - Validate blockchain
- `GET /api/blockchain/stats` - Get statistics
- `GET /api/blockchain/pending` - Get pending records

## 🔑 Key Concepts

### Immutability
Once a record is mined into a block, it cannot be changed. Any attempt to modify it will break the chain's integrity.

### Hash Function (SHA-256)
Each block has a unique hash that depends on its content. Changing any data will result in a different hash, breaking the chain.

### Proof of Work
Before a block is added, it must be "mined" - the system must find a hash with a specific number of leading zeros. This requires computation effort.

### Chain Validation
The system can verify the entire blockchain by checking:
1. Each block's hash is correct
2. Each block's previous_hash matches the previous block's hash
3. If any tampering occurred, validation will fail

## 📝 Example Workflow

1. **Register Students**
   - Go to Students tab
   - Fill in student details
   - Click "Register Student"

2. **Add Academic Records**
   - Go to Records tab
   - Enter student ID (from registration)
   - Add course grades
   - Click "Add Record"

3. **Mine Records**
   - Go to Dashboard
   - Click "Mine Pending Records"
   - Wait for mining to complete

4. **View Blockchain**
   - Go to Blockchain tab
   - Click "Load Blockchain"
   - See all blocks and records

5. **Verify Records**
   - Go to Verify tab
   - Enter a record ID
   - Click "Verify Record"
   - Confirm authenticity

## 🎓 Learning Outcomes

This project helps you understand:
- ✅ Blockchain fundamentals and architecture
- ✅ Cryptographic hashing and digital signatures
- ✅ Consensus mechanisms (Proof of Work)
- ✅ Smart contract concepts (record validation)
- ✅ Distributed systems and immutability
- ✅ Real-world applications of blockchain

## 🔍 Troubleshooting

### Port Already in Use
If port 5000 is already in use:
```bash
# Change port in app.py
# Change: app.run(debug=True, host='0.0.0.0', port=5000)
# To: app.run(debug=True, host='0.0.0.0', port=5001)
```

### Module Not Found
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

### CORS Errors
The application has CORS enabled, but if you face issues:
- Ensure Flask-CORS is installed
- Check that requests are from `http://localhost:5000`

## 📚 Additional Resources

- [Blockchain Basics](https://en.wikipedia.org/wiki/Blockchain)
- [SHA-256 Hashing](https://en.wikipedia.org/wiki/SHA-2)
- [Proof of Work](https://en.wikipedia.org/wiki/Proof_of_work)
- [Flask Documentation](https://flask.palletsprojects.com/)

## 📄 License

This project is created for educational purposes as a miniproject for the Blockchain subject.

## 👨‍💻 Author

Created as an Academic Record System using Blockchain Technology - Miniproject

## 🤝 Contributing

Feel free to extend this project with:
- Smart contracts (if using Ethereum)
- Multi-signature verification
- Revocation mechanism
- Performance optimization
- Enhanced UI/UX
- Mobile application
- Database integration
- Role-based access control

## ✅ Checklist for Miniproject Submission

- [x] Blockchain implementation with hashing
- [x] Mining/Proof of Work mechanism
- [x] Record storage and retrieval
- [x] Chain validation
- [x] Record verification
- [x] Web interface
- [x] REST API
- [x] Documentation
- [x] Working demo

---

**Happy Coding! 🚀**

For questions or issues, refer to the troubleshooting section or review the code comments.
