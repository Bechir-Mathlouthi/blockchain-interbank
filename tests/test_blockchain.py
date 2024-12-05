import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from blockchain import Blockchain

class TestBlockchain(unittest.TestCase):
    def setUp(self):
        self.blockchain = Blockchain()
    
    def test_genesis_block(self):
        """Test that the blockchain is initialized with a genesis block"""
        self.assertEqual(len(self.blockchain.chain), 1)
        genesis_block = self.blockchain.chain[0]
        self.assertEqual(genesis_block['previous_hash'], "0")
        self.assertEqual(genesis_block['proof'], 100)
    
    def test_add_transaction(self):
        """Test adding a new transaction"""
        next_block = self.blockchain.add_transaction("BankA", "BankB", 100.0)
        self.assertEqual(len(self.blockchain.current_transactions), 1)
        transaction = self.blockchain.current_transactions[0]
        self.assertEqual(transaction['sender'], "BankA")
        self.assertEqual(transaction['receiver'], "BankB")
        self.assertEqual(transaction['amount'], 100.0)
    
    def test_generate_block(self):
        """Test block generation"""
        self.blockchain.add_transaction("BankA", "BankB", 100.0)
        initial_chain_length = len(self.blockchain.chain)
        
        block = self.blockchain.generate_block(proof=123)
        
        self.assertEqual(len(self.blockchain.chain), initial_chain_length + 1)
        self.assertEqual(len(self.blockchain.current_transactions), 0)
        self.assertEqual(block['proof'], 123)
    
    def test_chain_validation(self):
        """Test blockchain validation"""
        self.blockchain.add_transaction("BankA", "BankB", 100.0)
        self.blockchain.generate_block(proof=123)
        
        # Chain should be valid
        self.assertTrue(self.blockchain.validate_chain())
        
        # Tamper with the chain
        self.blockchain.chain[1]['transactions'][0]['amount'] = 200.0
        
        # Chain should be invalid
        self.assertFalse(self.blockchain.validate_chain())

if __name__ == '__main__':
    unittest.main() 