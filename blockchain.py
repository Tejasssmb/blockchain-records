"""
Custom Blockchain Implementation for Academic Records
Implements a simple but functional blockchain system
"""
import hashlib
import json
from datetime import datetime
from typing import List, Dict, Any, Optional


class Block:
    """Represents a single block in the blockchain"""
    
    def __init__(self, index: int, timestamp: str, data: Dict[str, Any], 
                 previous_hash: str, nonce: int = 0):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Calculate SHA-256 hash of the block"""
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int):
        """Proof of Work - find hash with 'difficulty' leading zeros"""
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block mined: {self.hash}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert block to dictionary"""
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce,
            'hash': self.hash
        }


class AcademicRecordBlockchain:
    """Main blockchain class for managing academic records"""
    
    def __init__(self, difficulty: int = 2):
        """
        Initialize blockchain
        
        Args:
            difficulty: Number of leading zeros for proof of work
        """
        self.chain: List[Block] = []
        self.difficulty = difficulty
        self.pending_records: List[Dict[str, Any]] = []
        
        # Create genesis block
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the first block in the blockchain"""
        genesis_block = Block(
            index=0,
            timestamp=datetime.now().isoformat(),
            data={'type': 'genesis', 'message': 'Genesis Block'},
            previous_hash='0'
        )
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
    
    def get_latest_block(self) -> Block:
        """Get the most recent block in the chain"""
        return self.chain[-1]
    
    def add_record(self, record: Dict[str, Any]):
        """Add a new academic record (pending)"""
        self.pending_records.append(record)
    
    def mine_pending_records(self, miner_id: str) -> Block:
        """
        Mine pending records into a new block
        
        Args:
            miner_id: ID of the entity mining this block
            
        Returns:
            The newly created and mined block
        """
        if not self.pending_records:
            return None
        
        latest_block = self.get_latest_block()
        
        new_block = Block(
            index=len(self.chain),
            timestamp=datetime.now().isoformat(),
            data={
                'miner': miner_id,
                'records': self.pending_records
            },
            previous_hash=latest_block.hash
        )
        
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.pending_records = []
        
        return new_block
    
    def is_chain_valid(self) -> bool:
        """Verify the integrity of the entire blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Verify current block's hash
            if current_block.hash != current_block.calculate_hash():
                print(f"Block {i}: Hash mismatch")
                return False
            
            # Verify chain link
            if current_block.previous_hash != previous_block.hash:
                print(f"Block {i}: Previous hash mismatch")
                return False
        
        return True
    
    def get_record_by_student_id(self, student_id: str) -> List[Dict[str, Any]]:
        """Search for all records belonging to a student"""
        records = []
        for block in self.chain:
            if block.data.get('type') != 'genesis':
                for record in block.data.get('records', []):
                    if record.get('student_id') == student_id:
                        records.append({
                            'block_index': block.index,
                            'timestamp': block.timestamp,
                            'record': record
                        })
        return records
    
    def get_record_by_id(self, record_id: str) -> Optional[Dict[str, Any]]:
        """Search for a specific record by ID"""
        for block in self.chain:
            if block.data.get('type') != 'genesis':
                for record in block.data.get('records', []):
                    if record.get('record_id') == record_id:
                        return {
                            'block_index': block.index,
                            'timestamp': block.timestamp,
                            'record': record
                        }
        return None
    
    def get_chain_data(self) -> List[Dict[str, Any]]:
        """Get all blocks in the chain"""
        return [block.to_dict() for block in self.chain]
    
    def verify_record(self, record_id: str) -> Dict[str, Any]:
        """Verify a record's authenticity"""
        record_data = self.get_record_by_id(record_id)
        
        if not record_data:
            return {'verified': False, 'message': 'Record not found'}
        
        if not self.is_chain_valid():
            return {'verified': False, 'message': 'Blockchain integrity compromised'}
        
        return {
            'verified': True,
            'message': 'Record is authentic and has not been tampered with',
            'record': record_data
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get blockchain statistics"""
        total_records = 0
        for block in self.chain:
            if block.data.get('type') != 'genesis':
                total_records += len(block.data.get('records', []))
        
        return {
            'total_blocks': len(self.chain),
            'total_records': total_records,
            'pending_records': len(self.pending_records),
            'chain_valid': self.is_chain_valid()
        }
