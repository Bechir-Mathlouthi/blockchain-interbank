import sqlite3
import os
from typing import List, Dict, Any
from datetime import datetime

DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'transactions.db')

def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Create transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT NOT NULL,
            receiver TEXT NOT NULL,
            amount REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create blocks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            block_hash TEXT NOT NULL,
            previous_hash TEXT,
            proof INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def store_transaction(sender: str, receiver: str, amount: float) -> int:
    """
    Store a transaction in the database
    
    Args:
        sender: Address of the sender
        receiver: Address of the receiver
        amount: Amount of money transferred
        
    Returns:
        ID of the inserted transaction
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO transactions (sender, receiver, amount)
        VALUES (?, ?, ?)
    ''', (sender, receiver, amount))
    
    transaction_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return transaction_id

def store_block(block_hash: str, previous_hash: str, proof: int) -> int:
    """
    Store a block in the database
    
    Args:
        block_hash: Hash of the current block
        previous_hash: Hash of the previous block
        proof: Proof of work
        
    Returns:
        ID of the inserted block
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO blocks (block_hash, previous_hash, proof)
        VALUES (?, ?, ?)
    ''', (block_hash, previous_hash, proof))
    
    block_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return block_id

def get_all_transactions() -> List[Dict[str, Any]]:
    """
    Retrieve all transactions from the database
    
    Returns:
        List of transactions
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM transactions')
    transactions = cursor.fetchall()
    
    conn.close()
    
    return [
        {
            'id': t[0],
            'sender': t[1],
            'receiver': t[2],
            'amount': t[3],
            'timestamp': t[4]
        }
        for t in transactions
    ]

def get_all_blocks() -> List[Dict[str, Any]]:
    """
    Retrieve all blocks from the database
    
    Returns:
        List of blocks
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM blocks')
    blocks = cursor.fetchall()
    
    conn.close()
    
    return [
        {
            'id': b[0],
            'block_hash': b[1],
            'previous_hash': b[2],
            'proof': b[3],
            'timestamp': b[4]
        }
        for b in blocks
    ] 