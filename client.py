import socket

import TxBlock
import Transaction
import Signatures
import pickle
import socket

TCP_PORT = 5005


def sendBlock(ip_addr, blk):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip_addr, TCP_PORT))
    data = pickle.dumps(blk)
    s.send(data)
    return False


if __name__ == "__main__":
    pr1, pu1 = Signatures.generate_keys()
    pr2, pu2 = Signatures.generate_keys()
    pr3, pu3 = Signatures.generate_keys()

    Tx1 = Transaction.Tx()
    Tx1.add_input(pu1, 2.3)
    Tx1.add_output(pu2, 1.0)
    Tx1.add_output(pu3, 1.1)
    Tx1.sign(pr1)

    Tx2 = Transaction.Tx()
    Tx2.add_input(pu3, 2.3)
    Tx2.add_input(pu2, 1.0)
    Tx2.add_output(pu2, 1.0)
    Tx2.add_output(pu1, 3.1)
    Tx2.sign(pr2)
    Tx2.sign(pr3)

    B1 = TxBlock.TxBlock(None)
    B1.addTx(Tx1)
    B1.addTx(Tx2)

    sendBlock('192.168.0.108', B1)

    sendBlock('192.168.0.108', Tx2)