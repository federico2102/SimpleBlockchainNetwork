
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
  - [Dockerization](#dockerization)
- [Usage](#usage)
  - [Starting and Registering Nodes](#starting-and-registering-nodes)
  - [Endpoints](#endpoints)
  - [Testing and Verification](#testing-and-verification)
- [Future Improvements](#future-improvements)
---

## About the Project
This project is a Python-based blockchain network where nodes communicate over a REST API. The blockchain supports basic functionalities like transaction handling, mining with proof-of-work, and peer-to-peer communication, making it an excellent way to understand blockchain infrastructure.

## Features
- **Blockchain Structure**: Manages a chain of blocks, each containing transactions.
- **Proof of Work (PoW)**: Implements a mining mechanism that adds computational difficulty to secure the network.
- **REST API Node Communication**: Exposes endpoints to interact with nodes (e.g., mining, adding transactions).
- **Peer-to-Peer Networking**: Allows nodes to connect and share information with other nodes in the network.
- **Dockerized Node Setup**: Easily simulate a multi-node blockchain network using Docker.

## Technologies
- **Python 3.9+**
- **Flask**: For creating RESTful API endpoints.
- **Hashlib**: Used to secure block hashes.
- **Docker**: For containerizing nodes and simulating a networked environment.

---

## Getting Started

### Prerequisites
- **Python 3.9+**: Ensure you have Python installed on your system.
- **Docker**: Install Docker to containerize and manage multiple nodes.

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

### Dockerization

To simulate a multi-node network, Dockerize each node and connect them within a Docker network.

1. **Create a Docker Network**:
   ```bash
   docker network create blockchain-network
   ```
2. **Build the Docker Image**:
   ```bash
   docker build -t blockchain-node .
   ```
3. **Run Containers for Each Node**:
   ```bash
   docker run -d --name node1 --network blockchain-network -p 5000:5000 blockchain-node
   docker run -d --name node2 --network blockchain-network -p 5001:5000 blockchain-node
   docker run -d --name node3 --network blockchain-network -p 5002:5000 blockchain-node
   ```

---

## Usage

### Starting and Registering Nodes

After starting nodes as Docker containers, register each node with others to enable peer-to-peer communication.

1. **Register `node2` with `node1`**:
   ```powershell
   Invoke-WebRequest -Uri http://localhost:5000/nodes/register -Method POST -Body '{"nodes": ["http://node2:5000"]}' -ContentType "application/json"
   ```

2. **Register `node3` with `node1`**:
   ```powershell
   Invoke-WebRequest -Uri http://localhost:5000/nodes/register -Method POST -Body '{"nodes": ["http://node3:5000"]}' -ContentType "application/json"
   ```

### Endpoints

- **Mine a Block**
  - URL: `http://localhost:5000/mine`
  - Method: `GET`
  - Description: Mines a new block with pending transactions and adds it to the blockchain.
  - Example:
    ```powershell
    Invoke-WebRequest -Uri http://localhost:5000/mine -Method GET
    ```

- **View the Full Blockchain**
  - URL: `http://localhost:5000/chain`
  - Method: `GET`
  - Description: Returns the entire blockchain in JSON format.
  - Example:
    ```powershell
    Invoke-WebRequest -Uri http://localhost:5000/chain -Method GET
    ```

- **Add a New Transaction**
  - URL: `http://localhost:5000/transactions/new`
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
    Invoke-WebRequest -Uri http://localhost:5000/transactions/new -Method POST -Body '{"sender": "A", "receiver": "B", "amount": 50}' -ContentType "application/json"
    ```

- **Register a Node**
  - URL: `http://localhost:5000/nodes/register`
  - Method: `POST`
  - Description: Register a list of peer nodes to enable decentralized communication.
  - Data Format:
    ```json
    {
      "nodes": ["http://localhost:5001", "http://localhost:5002"]
    }
    ```

### Testing and Verification

1. **Confirm Node Registration**:
   - Retrieve the list of registered peers from `node1`:
     ```powershell
     Invoke-WebRequest -Uri http://localhost:5000/nodes -Method GET
     ```

2. **Add and Mine Transactions**:
   - Add a transaction to `node1`:
     ```powershell
     Invoke-WebRequest -Uri http://localhost:5000/transactions/new -Method POST -Body '{"sender": "Alice", "receiver": "Bob", "amount": 25}' -ContentType "application/json"
     ```
   - Mine a block on `node1` to add the transaction to the blockchain:
     ```powershell
     Invoke-WebRequest -Uri http://localhost:5000/mine -Method GET
     ```

3. **Verify Blockchain Synchronization**:
   - Retrieve the blockchain from each node to verify they are synchronized:
     ```powershell
     Invoke-WebRequest -Uri http://localhost:5000/chain -Method GET
     Invoke-WebRequest -Uri http://localhost:5001/chain -Method GET
     Invoke-WebRequest -Uri http://localhost:5002/chain -Method GET
     ```

---

## Future Improvements
Some possible expansions to this project include:
- **Consensus Algorithm**: Implement a consensus protocol to synchronize the longest chain across nodes.
- **Web Interface**: Add a user-friendly front-end for easier interaction with the blockchain.
- **Enhanced Peer Discovery**: Develop automated peer discovery and dynamic connection handling.
- **Improved Security**: Use SSL/TLS for secure communication between nodes.

---

