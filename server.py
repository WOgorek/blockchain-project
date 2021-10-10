import socket
import pickle
import TxBlock
import socket

TCP_PORT = 5005
BUFFER_SIZE = 1024

def recvObj(ip_addr):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip_addr,TCP_PORT))
    s.listen()
    new_sock, addr = s.accept()
    all_data = b''
    while True:
        data = new_sock.recv(BUFFER_SIZE)
        if not data: break
        all_data = all_data + data
    return pickle.loads(all_data)


if __name__ == "__main__":
    newB = recvObj('192.168.0.108')
    print(newB.data[0])
    print(newB.data[1])
    if (newB.is_valid()):
        print("Success. Tx is valid")
    else:
        print("ERROR! Tx invalid")

    if newB.data[0].inputs[0][1] == 2.3:
        print("Success. Input value matches")
    else:
        print("Error! Wrong input value for block 1")

    if newB.data[1].inputs[0][1] == 2.3:
        print("Success. Input value matches")
    else:
        print("Error! Wrong input value for block 1")

    if newB.data[1].inputs[1][1] == 1.0:
        print("Success. Input value matches")
    else:
        print("Error! Wrong input value for block 1")

    if newB.data[0].outputs[1][1] == 1.1:
        print("Success. Output value matches")
    else:
        print("Error! Wrong output value for block 1")

    if newB.data[1].outputs[0][1] == 3.1:
        print("Success. Output value matches")
    else:
        print("Error! Wrong output value for block 1")

    newTx = recvObj('192.168.0.108')
    print(newTx)
