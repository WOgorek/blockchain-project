from Blockchain import CBlock
import Signatures
from Transaction import Tx
import pickle
import random
import time
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

reward = 25.0
leading_zeros = 2
next_char_limit = 20

class TxBlock(CBlock):
    nonce = "AAAAAAAA"

    def __init__(self, previousBlock):
        super(TxBlock, self).__init__([], previousBlock)

    def addTx(self, Tx_in):
        self.data.append(Tx_in)

    def __count_totals(self):
        total_in = 0
        total_out = 0
        for tx in self.data:
            for addr, amt in tx.inputs:
                total_in += amt
            for addr, amt in tx.outputs:
                total_out += amt
        return total_in, total_out

    def is_valid(self):
        if not super(TxBlock, self).is_valid():
            return False
        for tx in self.data:
            if not tx.is_valid():
                return False
        total_in, total_out = self.__count_totals()
        if total_out - total_in - reward > 0.00000000000000001:
            return False
        return True

    def good_nonce(self):
        digest = hashes.Hash(hashes.SHA256())
        digest.update(bytes(str(self.data), 'utf-8'))
        digest.update(bytes(str(self.previousHash), 'utf-8'))
        digest.update(bytes(str(self.nonce), 'utf-8'))
        this_hash = digest.finalize()
        # print(str(this_hash[:leading_zeros]))

        if this_hash[:leading_zeros] != bytes(''.join([ '\x4f' for i in range(leading_zeros)]), 'utf-8'):
            return False
        return int(this_hash[leading_zeros]) < next_char_limit
    def find_nonce(self):
        for i in range(1000000):
            self.nonce = ''.join([chr(random.randint(0,255)) for i in range(10*leading_zeros)])
            if self.good_nonce():
                return self.nonce
        return None


if __name__ == "__main__":
    pr1, pu1 = Signatures.generate_keys()
    pr2, pu2 = Signatures.generate_keys()
    pr3, pu3 = Signatures.generate_keys()

    Tx1 = Tx()
    Tx1.add_input(pu1, 1)
    Tx1.add_output(pu2, 1)
    Tx1.sign(pr1)

    #Test czy Tx1 jest walid
    Tx1.is_valid()

    #Test czy możemy zrobić dumpa i odczytać Tx1
    savefile = open("save.dat", 'wb')
    pickle.dump(Tx1, savefile)
    savefile.close()
    loadfile = open("save.dat", 'rb')
    newTx = pickle.load(loadfile)
    newTx.is_valid()

    root = TxBlock(None)
    root.addTx(Tx1)

    Tx2 = Tx()
    Tx2.add_input(pu2, 1.1)
    Tx2.add_output(pu3, 1)
    Tx2.sign(pr2)
    root.addTx(Tx2)

    B1 = TxBlock(root)
    Tx3 = Tx()
    Tx3.add_input(pu3, 1.1)
    Tx3.add_output(pu1, 1)
    Tx3.sign(pr3)
    B1.addTx(Tx3)

    Tx4 = Tx()
    Tx4.add_input(pu1, 1)
    Tx4.add_output(pu2, 1)
    Tx4.add_reqd(pu3)
    Tx4.sign(pr1)
    Tx4.sign(pr3)
    B1.addTx(Tx4)

    start = time.time()
    print(B1.find_nonce())
    elapsed = time.time() - start
    if B1.good_nonce():
        print("Success! Nonce is good!")
    else:
        print("Error - nounce is bad")
    print("elapsed time: " + str(elapsed) + " s.")
    if elapsed < 60:
        print("ERROR - mining too fast")

    B1.is_valid()
    root.is_valid()

    savefile = open("block.dat", "wb")
    pickle.dump(B1, savefile)
    savefile.close()

    loadfile = open("block.dat", "rb")
    load_B1 = pickle.load(loadfile)
    loadfile.close()
    load_B1.is_valid()

    #print(bytes(str(load_B1.data), 'utf8'))

    for b in [root, B1, load_B1, load_B1.previousBlock]:
        if b.is_valid():
            print("Succes! Valid block")
        else:
            print("ERROR! Bad block")

    if load_B1.good_nonce():
        print("Success! Nonce is good after save and load!")
    else:
        print("ERROR - Nonce is bad after save and load")

    B2 = TxBlock(B1)
    Tx5 = Tx()
    Tx5.add_input(pu3, 1)
    Tx5.add_output(pu1, 100)
    Tx5.sign(pr3)
    B2.addTx(Tx5)

    load_B1.previousBlock.addTx(Tx4)

    for b in [load_B1, B2]:
        if b.is_valid():
            print("ERROR! Bad block verified")
        else:
            print("Success! Bad block detected!")

    # Test mining reward and tx fees

    # Mining reward
    pr4, pu4 = Signatures.generate_keys()
    B3 = TxBlock(B2)
    B3.addTx(Tx2)
    B3.addTx(Tx3)
    B3.addTx(Tx4)
    Tx6 = Tx()
    Tx6.add_output(pu4, 25)
    B3.addTx(Tx6)
    if B3.is_valid():
        print("Success! Block reward succeeds")
    else:
        print("ERROR! Block reward fail!")

    # Mining + fee reward
    B4 = TxBlock(B3)
    B4.addTx(Tx2)
    B4.addTx(Tx3)
    B4.addTx(Tx4)
    Tx7 = Tx()
    Tx7.add_output(pu4, 25.2)
    B4.addTx(Tx6)
    if B4.is_valid():
        print("Success! Tx fees succeeds")
    else:
        print("ERROR! Tx fees fail!")

    # Greedy miner
    B5 = TxBlock(B4)
    B5.addTx(Tx2)
    B5.addTx(Tx3)
    B5.addTx(Tx4)
    Tx8 = Tx()
    Tx8.add_output(pu4, 26.2)
    B5.addTx(Tx8)
    if B5.is_valid():
        print("ERROR! Greedy miner not detected!")
    else:
        print("Success - greedy miner detected")
