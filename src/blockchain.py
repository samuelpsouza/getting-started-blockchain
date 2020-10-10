import hashlib
import json
from time import time

from uuid import uuid4
from flask import Flask, jsonify, request

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.transactions = []

    def new_block(self, proof, prev_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.transactions,
            'proof': proof,
            'prev_hash': prev_hash
        }

        self.transactions = []
        self.chain.append(block)

        return block

    def new_transaction(self, sender, recipient, amount):
        self.transactions.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        })

        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        self.chain[-1]

    def proof_of_word(self, last_proof):
        proof = 0

        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f"{last_proof}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        
        return guess_hash[:4] == "0000"

app = Flask(__name__)
node_identifier = str(uuid4()).replace("-", "")

blockchain = Blockchain()

@app.route("/mine", methods=["GET"])
def mine():
    pass

@app.route("/transactions/new", methods=["POST"])
def new_transaction():
    SENDER = "sender"
    RECIPIENT = "recipient"
    AMOUNT = "amount"
    values = request.get_json()

    required = [SENDER, RECIPIENT, AMOUNT]

    if not all(k in values for k in required):
        return "Required values are missing", 400

    index = blockchain.new_transaction(values[SENDER], values[RECIPIENT], values[AMOUNT])
    res = {"message": f"Transaction will be added to Block {index}"}

    return jsonify(res), 200

@app.route("/chain", methods=["GET"])
def complete_chain():
    chain = blockchain.chain
    res = {
        "chain": chain,
        "length": len(chain)
    }

    return jsonify(res), 200

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 8080)