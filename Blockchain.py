from cryptography.hazmat.primitives import hashes

# digest = hashes.Hash(hashes.SHA256())
# digest.update(b"abc")
# digest.update(b"123")
# hash_example = digest.finalize()
# print(hash_example)


class SomeClass:
    example_string = None

    def __init__(self, mystring):
        self.example_string = mystring

    def __repr__(self):
        return self.example_string


class CBlock:
    data = None
    previousHash = None
    previousBlock = None

    def __init__(self, data, previousblock):
        self.data = data
        self.previousBlock = previousblock
        if previousblock:
            self.previousHash = self.previousBlock.computehash()

    def computehash(self):
        digest = hashes.Hash(hashes.SHA256())
        digest.update(bytes(str(self.data), 'utf-8'))
        digest.update(bytes(str(self.previousHash), 'utf-8'))
        return digest.finalize()

    def is_valid(self):
        if self.previousBlock is None:
            return True
        return self.previousBlock.computehash() == self.previousHash


if __name__ == "__main__":
    root = CBlock("I am root", None)
    B1 = CBlock("I am a child", root)
    B2 = CBlock("I am a B1s brother", root)
    B3 = CBlock(12345, B1)
    B4 = CBlock(SomeClass("Hi there!"), B3)
    B5 = CBlock("Top block", B4)

    i = 1
    for block in [B1, B2, B3, B4, B5]:
        if block.previousBlock.computehash() == block.previousHash:

            print(f"{i}: Success! Hash is good")
        else:
            print(f"{i}: ERROR! Hash is not good")
        i += 1
    i = 1
    print("*"*40)
    B3.data = "a psik"

    for block in [B1, B2, B3, B4, B5]:
        if block.previousBlock.computehash() == block.previousHash:
            print(f"{i}: Success! Hash is good")
        else:
            print(f"{i}: ERROR! Hash is not good")
        i += 1
