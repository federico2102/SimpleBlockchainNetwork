from flask import Flask, jsonify, request
from blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    blockchain.mine_pending_transactions()
    return jsonify({"message": "New block mined!"}), 200

@app.route('/chain', methods=['GET'])
def full_chain():
    chain_data = [{"index": block.index, "hash": block.hash} for block in blockchain.chain]
    return jsonify({"length": len(chain_data), "chain": chain_data}), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    tx_data = request.get_json()
    blockchain.pending_transactions.append(tx_data)
    return jsonify({"message": "Transaction added to pending list"}), 201

if __name__ == '__main__':
    app.run(port=5000)

peers = set()

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    nodes = request.get_json().get("nodes")
    for node in nodes:
        peers.add(node)
    return jsonify({"message": "Nodes registered successfully", "nodes": list(peers)}), 201

@app.route('/nodes', methods=['GET'])
def get_nodes():
    return jsonify({"nodes": list(peers)}), 200
