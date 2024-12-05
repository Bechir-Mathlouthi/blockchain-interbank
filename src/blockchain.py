import hashlib
import json
from time import time
from typing import List, Dict, Any

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        
        # Create genesis block
        self.generate_block(previous_hash="0", proof=100)
    
    def add_transaction(self, sender: str, receiver: str, amount: float) -> int:
        """
        Add a new transaction to the list of current transactions
        
        Args:
            sender: Address of the sender
            receiver: Address of the receiver
            amount: Amount of money to transfer
            
        Returns:
            The index of the block that will hold this transaction
        """
        self.current_transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount,
            'timestamp': time()
        })
        
        return self.get_last_block()['index'] + 1
    
    def generate_block(self, proof: int, previous_hash: str = None) -> Dict[str, Any]:
        """
        Create a new block in the blockchain
        
        Args:
            proof: The proof of work
            previous_hash: Hash of the previous block
            
        Returns:
            The new block
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]) if self.chain else None
        }
        
        # Reset the current list of transactions
        self.current_transactions = []
        
        self.chain.append(block)
        return block
    
    def validate_chain(self) -> bool:
        """
        Determine if the blockchain is valid
        
        Returns:
            True if valid, False if not
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            # Check that the hash of the block is correct
            if current_block['previous_hash'] != self.hash(previous_block):
                return False
            
            # Check that the Proof of Work is correct
            if not self.valid_proof(previous_block['proof'], current_block['proof']):
                return False
        
        return True
    
    def get_chain(self) -> List[Dict[str, Any]]:
        """
        Return the full chain
        
        Returns:
            The blockchain
        """
        return self.chain
    
    def get_last_block(self) -> Dict[str, Any]:
        """
        Returns the last block in the chain
        
        Returns:
            The last block
        """
        return self.chain[-1] if self.chain else None
    
    @staticmethod
    def hash(block: Dict[str, Any]) -> str:
        """
        Creates a SHA-256 hash of a block
        
        Args:
            block: Block to hash
            
        Returns:
            Hash of the block
        """
        # We must make sure that the Dictionary is ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    @staticmethod
    def valid_proof(last_proof: int, proof: int) -> bool:
        """
        Validates the proof
        
        Args:
            last_proof: Previous proof
            proof: Current proof
            
        Returns:
            True if correct, False if not
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000" 