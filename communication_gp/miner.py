# Paste your version of miner.py from the clinet_mining_p
# folder here
import hashlib
import requests

import sys


# TODO: Implement functionality to search for a proof 

# Run the proof_of_work function until a valid proof is found, validating or rejecting each attempt

def proof_of_work(last_block_string):
    """
    Simple Proof of Work Algorithm
    Find a number p such that hash(last_block_string, p) contains 6 leading
    zeroes
    """
    print("Starting work on a new proof...")
    proof = 0
    while valid_proof(last_block_string , proof) is False:
        proof +=1
    print("Attempting to mine...")
    return proof

# Request the latest proof from the last_proof endpoint on the server
def valid_proof(last_block_string, proof):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 6
    leading zeroes?
    """
    # TODO
    #build string to hash
    guess = f'{last_block_string}{proof}'.encode()
    # use hash function
    guess_hash = hashlib.sha256(guess).hexdigest()
    #Check if 6 leading 0's
    beg = guess_hash[0:6] #[:6]
    if beg == "0000":
        return True
    else:
        return False
    pass

if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    # Run forever until interrupted
    while True:
        # TODO: Get the last proof from the server and look for a new one
        r = requests.get(url = node + "/last_block_string")
        data = r.json()
        last_block_string = data['last_block_string']['previous_hash']

        print(last_block_string)

        # TODO: When found, POST it to the server {"proof": new_proof}
        new_proof = proof_of_work(last_block_string)
    
        # TODO: We're going to have to research how to do a POST in Python
        # HINT: Research `requests` and remember we're sending our data as JSON
        proof_data = {'proof': new_proof}
        # TODO: If the server responds with 'New Block Forged'
        r = requests.post(url = node+'/mine', json = proof_data)
        data = r.json()
        # add 1 to the number of coins mined and print it.  Otherwise,
        if data.get('message') == "New Block Forged":
            coins_mined += 1
            print("You have: " + str(coins_mined) + "coins")

        # print the message from the server.
        print(data.get('message'))
        
