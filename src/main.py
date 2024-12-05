import sys
import logging
from typing import Optional
from blockchain import Blockchain
import utils

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BlockchainCLI:
    def __init__(self):
        self.blockchain = Blockchain()
        utils.init_db()
    
    def add_transaction(self, sender: str, receiver: str, amount: float) -> None:
        """Add a new transaction to the blockchain"""
        try:
            # Validate input
            if not all([sender, receiver, amount]):
                raise ValueError("All fields (sender, receiver, amount) are required")
            if amount <= 0:
                raise ValueError("Amount must be positive")
            
            # Add to blockchain and database
            next_block_index = self.blockchain.add_transaction(sender, receiver, amount)
            utils.store_transaction(sender, receiver, amount)
            
            logger.info(f"Transaction added successfully. Will be included in block {next_block_index}")
        except Exception as e:
            logger.error(f"Error adding transaction: {str(e)}")
    
    def generate_block(self) -> None:
        """Generate a new block"""
        try:
            # Simple proof of work - in production this would be more sophisticated
            proof = 100
            previous_block = self.blockchain.get_last_block()
            previous_hash = self.blockchain.hash(previous_block) if previous_block else "0"
            
            block = self.blockchain.generate_block(proof, previous_hash)
            utils.store_block(
                self.blockchain.hash(block),
                block['previous_hash'],
                block['proof']
            )
            
            logger.info(f"New block generated: {block['index']}")
        except Exception as e:
            logger.error(f"Error generating block: {str(e)}")
    
    def view_chain(self) -> None:
        """View the entire blockchain"""
        try:
            chain = self.blockchain.get_chain()
            logger.info("\n=== Current Blockchain ===")
            for block in chain:
                logger.info(f"\nBlock #{block['index']}")
                logger.info(f"Timestamp: {block['timestamp']}")
                logger.info(f"Previous Hash: {block['previous_hash']}")
                logger.info(f"Proof: {block['proof']}")
                logger.info("Transactions:")
                for tx in block['transactions']:
                    logger.info(f"  {tx['sender']} -> {tx['receiver']}: {tx['amount']}")
                logger.info("=" * 30)
        except Exception as e:
            logger.error(f"Error viewing chain: {str(e)}")
    
    def validate_chain(self) -> None:
        """Validate the blockchain"""
        try:
            is_valid = self.blockchain.validate_chain()
            if is_valid:
                logger.info("Blockchain is valid!")
            else:
                logger.warning("Blockchain validation failed!")
        except Exception as e:
            logger.error(f"Error validating chain: {str(e)}")

def print_menu():
    """Print the main menu"""
    print("\nInterbank Blockchain System")
    print("1. Add Transaction")
    print("2. Generate Block")
    print("3. View Blockchain")
    print("4. Validate Chain")
    print("5. Exit")
    print("\nEnter your choice (1-5): ")

def main():
    cli = BlockchainCLI()
    
    while True:
        print_menu()
        choice = input().strip()
        
        if choice == "1":
            sender = input("Enter sender bank: ").strip()
            receiver = input("Enter receiver bank: ").strip()
            try:
                amount = float(input("Enter amount: ").strip())
                cli.add_transaction(sender, receiver, amount)
            except ValueError:
                logger.error("Invalid amount entered")
        
        elif choice == "2":
            cli.generate_block()
        
        elif choice == "3":
            cli.view_chain()
        
        elif choice == "4":
            cli.validate_chain()
        
        elif choice == "5":
            print("Goodbye!")
            sys.exit(0)
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting gracefully...")
        sys.exit(0) 