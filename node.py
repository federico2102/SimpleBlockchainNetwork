import os
import requests
from flask import Flask, jsonify, request
from blockchain import Blockchain, Block

# Initialize Flask app and blockchain
app = Flask(__name__)
blockchain = Blockchain()

# Global set to store all peer nodes
peers = set()

# Load peers from the PEERS environment variable (set in docker-compose.yml)
peer_env = os.getenv("PEERS", "")
for peer in peer_env.split(","):
    peers.add(peer.strip())

@app.route('/mine', methods=['GET'])
def mine():
    blockchain.mine_pending_transactions()
    new_block = blockchain.get_latest_block()

    # Prepare block data to send to peers
    new_block_data = {
        "index": new_block.index,
        "previous_hash": new_block.previous_hash,
        "timestamp": new_block.timestamp,
        "transactions": new_block.transactions,
        "nonce": new_block.nonce,
        "hash": new_block.hash,
    }

    # Broadcast new block to all peers
    for peer in peers:
        try:
            response = requests.post(f"{peer}/chain/add_block", json=new_block_data)
            print(f"Block broadcasted to {peer}, response: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to broadcast to {peer}: {e}")

    return jsonify({"message": "New block mined and broadcasted!"}), 200

@app.route('/chain/add_block', methods=['POST'])
def add_block():
    block_data = request.get_json()
    new_block = Block(
        index=block_data['index'],
        previous_hash=block_data['previous_hash'],
        timestamp=block_data['timestamp'],
        transactions=block_data['transactions'],
        nonce=block_data['nonce'],
        hash=block_data['hash']
    )

    # Append block if valid
    if blockchain.get_latest_block().hash == new_block.previous_hash and new_block.hash == new_block.calculate_hash():
        blockchain.chain.append(new_block)
        return jsonify({"message": "Block added successfully!"}), 200
    else:
        return jsonify({"message": "Block rejected due to invalid hash or previous hash mismatch"}), 400

@app.route('/chain', methods=['GET'])
def full_chain():
    chain_data = [{"index": block.index, "hash": block.hash} for block in blockchain.chain]
    return jsonify({"length": len(chain_data), "chain": chain_data}), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    tx_data = request.get_json()
    blockchain.pending_transactions.append(tx_data)
    return jsonify({"message": "Transaction added to pending list"}), 201

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    nodes = request.get_json().get("nodes")
    for node in nodes:
        peers.add(node)
    return jsonify({"message": "Nodes registered successfully", "nodes": list(peers)}), 201

@app.route('/nodes', methods=['GET'])
def get_nodes():
    return jsonify({"nodes": list(peers)}), 200

@app.route('/chain/replace', methods=['GET'])
def replace_chain():
    global blockchain
    longest_chain = blockchain.chain
    for peer in peers:
        try:
            response = requests.get(f"{peer}/chain")
            peer_chain_data = response.json().get("chain", [])
            peer_chain = [Block(
                data["index"],
                data["previous_hash"],
                data["timestamp"],
                data["transactions"],
                data["nonce"],
                data["hash"]
            ) for data in peer_chain_data]

            if len(peer_chain) > len(longest_chain) and blockchain.is_chain_valid(peer_chain):
                longest_chain = peer_chain
                print(f"Replacing chain with longer chain from {peer}")
        except Exception as e:
            print(f"Error syncing with peer {peer}: {e}")

    if longest_chain != blockchain.chain:
        blockchain.chain = longest_chain
        return jsonify({"message": "Chain was replaced with a longer chain."}), 200
    else:
        return jsonify({"message": "No replacement needed; chain is up to date."}), 200
