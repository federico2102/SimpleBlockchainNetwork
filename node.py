import requests
from flask import Flask, jsonify, request
from blockchain import Blockchain, Block

# Global set to store all peer nodes
peers = set()

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    # Mine a new block with pending transactions
    blockchain.mine_pending_transactions()

    # After mining, ask all peers to check for the latest chain
    for peer in peers:
        try:
            # Trigger each peer to replace their chain if needed
            requests.get(f"{peer}/chain/replace")
        except requests.exceptions.RequestException:
            print(f"Could not connect to peer {peer}")

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
        hash=block_data['hash']  # Explicitly set hash to match
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
            response.raise_for_status()

            # Ensure the response contains the "chain" key
            peer_chain_data = response.json().get("chain", [])
            if not peer_chain_data:
                print(f"No chain data from {peer}")
                continue

            # Construct peer chain with validation on keys
            peer_chain = []
            for block_data in peer_chain_data:
                # Ensure all required keys are present
                if all(key in block_data for key in ["index", "previous_hash", "timestamp", "transactions", "nonce", "hash"]):
                    peer_chain.append(Block(
                        block_data["index"],
                        block_data["previous_hash"],
                        block_data["timestamp"],
                        block_data["transactions"],
                        block_data["nonce"],
                        block_data["hash"]
                    ))
                else:
                    print(f"Skipping invalid block from {peer}: {block_data}")
                    continue

            # Update if peer's chain is longer and valid
            if len(peer_chain) > len(longest_chain) and blockchain.is_chain_valid(peer_chain):
                longest_chain = peer_chain

        except (requests.exceptions.RequestException, KeyError, TypeError) as e:
            print(f"Error syncing with peer {peer}: {e}")
            continue

    # Replace chain if we found a longer valid chain
    if longest_chain != blockchain.chain:
        blockchain.chain = longest_chain
        return jsonify({"message": "Chain was replaced with a longer chain."}), 200
    else:
        return jsonify({"message": "No replacement needed; chain is up to date."}), 200
