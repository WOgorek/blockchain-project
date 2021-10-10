import threading


def printa():
    print("A ... . ...")


def printb():
    print("B*******")


def printany(inarg):
    print(str(inarg))


t1 = threading.Thread(target=printa)

t2 = threading.Thread(target=printany, args=(789,))

t1.start()
t2.start()

printb()

t1.join()
t2.join()

print("End here")


