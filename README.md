
---

# Simple Blockchain Network

A minimal blockchain network implementation in Python. This project demonstrates the core concepts of blockchain, including blocks, mining, proof of work, and node-to-node communication using a simple REST API.

## Table of Contents
- [About the Project](#about-the-project)
- [Features](#features)
- [Technologies](#technologies)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Endpoints](#endpoints)
- [Future Improvements](#future-improvements)

---

## About the Project
This project is a Python-based blockchain network where nodes communicate over a REST API. The blockchain supports basic functionalities like transaction handling, mining with proof-of-work, and peer-to-peer communication, making it an excellent way to understand blockchain infrastructure.

## Features
- **Blockchain Structure**: Manages a chain of blocks, each containing transactions.
- **Proof of Work (PoW)**: Implements a mining mechanism that adds computational difficulty to secure the network.
- **REST API Node Communication**: Exposes endpoints to interact with nodes (e.g., mining, adding transactions).
- **Peer-to-Peer Networking**: Allows nodes to connect and share information with other nodes in the network.

## Technologies
- **Python 3.9+**
- **Flask**: For creating RESTful API endpoints.
- **Hashlib**: Used to secure block hashes.
- **Requests**: Optional, for peer communication (future improvements).

---

## Getting Started

### Prerequisites
- **Python 3.9+**: Ensure you have Python installed on your system.
- **Flask**: Flask is used for building the REST API. You can install it via `pip`.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/federico2102/SimpleBlockchainNetwork.git
   ```
2. Navigate to the project directory:
   ```bash
   cd SimpleBlockchainNetwork
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Starting a Node
To start a blockchain node, run the following command:
```bash
python run_node.py
```
This will start a server on `http://127.0.0.1:5000`.

### Interacting with the API

#### Endpoints

- **Mine a Block**
  - URL: `http://127.0.0.1:5000/mine`
  - Method: `GET`
  - Description: Mines a new block with pending transactions and adds it to the blockchain.
  - Example:
    ```powershell
    Invoke-WebRequest -Uri http://127.0.0.1:5000/mine -Method GET
    ```

- **View the Full Blockchain**
  - URL: `http://127.0.0.1:5000/chain`
  - Method: `GET`
  - Description: Returns the entire blockchain in JSON format.
  - Example:
    ```powershell
    Invoke-WebRequest -Uri http://127.0.0.1:5000/chain -Method GET
    ```

- **Add a New Transaction**
  - URL: `http://127.0.0.1:5000/transactions/new`
  - Method: `POST`
  - Description: Adds a new transaction to the list of pending transactions.
  - Data Format:
    ```json
    {
      "sender": "A",
      "receiver": "B",
      "amount": 50
    }
    ```
  - Example:
    ```powershell
    Invoke-WebRequest -Uri http://127.0.0.1:5000/transactions/new -Method POST -Body '{"sender": "A", "receiver": "B", "amount": 50}' -ContentType "application/json"
    ```

- **Register a Node**
  - URL: `http://127.0.0.1:5000/nodes/register`
  - Method: `POST`
  - Description: Register a list of peer nodes to enable decentralized communication.
  - Data Format:
    ```json
    {
      "nodes": ["http://127.0.0.1:5001", "http://127.0.0.1:5002"]
    }
    ```

---

## Future Improvements
Some possible expansions to this project include:
- **Consensus Algorithm**: Implement a consensus protocol to synchronize the longest chain across nodes.
- **Web Interface**: Add a user-friendly front-end for easier interaction with the blockchain.
- **Enhanced Peer Discovery**: Develop automated peer discovery and dynamic connection handling.
- **Dockerization**: Containerize nodes with Docker to simulate a multi-node blockchain network.

---
