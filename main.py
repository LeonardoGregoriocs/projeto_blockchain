from flask import Flask, jsonify, request
from uuid import uuid4

from blockchain import Blockchain

app = Flask(__name__)

node_identifier = str(uuid4()).replace('-','')
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1
    )

    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_transaction(proof, previous_hash)

    response = {
        'message' : "Novo bloco forjado",
        'index' : block['index'],
        'transaction' : block['transaction'],
        'proof' : block['proof'],
        'previous_hash' : block['previous_hash']
    }

    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Valores ausentes'

    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amout'])

    response = {'message': f"A transação será adicionada ao Bloco {index}"}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain' : blockchain.chain,
        'length' : len(blockchain.chain)
    }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
