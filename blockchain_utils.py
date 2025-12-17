import random
import string

def random_tx():
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(6))

def simulate_blockchain(num_blocks=10, tx_per_block=5):
    chain = []
    pending_counts = []
    pending = [random_tx() for _ in range(20)]

    for i in range(num_blocks):
        block_txs = pending[:tx_per_block]
        pending = pending[tx_per_block:]
        block = {
            "index": i,
            "transactions": block_txs,
            "prev_hash": chain[-1]["hash"] if chain else "GENESIS",
            "hash": f"BLOCK{i}{random.randint(1000,9999)}"
        }
        chain.append(block)
        pending_counts.append(len(pending))

    return chain, pending_counts