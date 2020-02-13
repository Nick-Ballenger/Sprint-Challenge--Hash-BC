
import hashlib
import requests

import sys

from uuid import uuid4

from timeit import default_timer as timer

import random


def proof_of_work(last_proof):
 

    start = timer()

    print("Searching for next proof")
    proof = 0

    encode_proof = f'{last_proof}'.encode()

    proof_hash = hashlib.sha256(encode_proof).hexdigest()


    while valid_proof(proof_hash, proof) is False:
        proof += 100

    print("Proof found: " + str(proof) + " in " + str(timer() - start))

    return proof


def valid_proof(last_hash, proof):
    hash_proof = last_hash[-6:]
    guess = f'{proof}'.encode()
    
    guess_hash = hashlib.sha256(guess).hexdigest()

    if guess_hash[:6] == hash_proof:
        print(guess_hash)
        return True
    return False


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-coin.herokuapp.com/api"

    coins_mined = 0

    # Load or create ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    if id == 'NONAME\n':
        print("ERROR: You must change your name in `my_id.txt`!")
        exit()
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof")
        data = r.json()
        new_proof = proof_of_work(data.get('proof'))

        post_data = {"proof": new_proof,
                     "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))