import Signatures

class Tx:
    inputs = None
    outputs = None
    sigs = None
    reqd = None

    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.sigs = []
        self.reqd = []
        self.debug = 0

    def add_input(self, from_addr, amount):
        self.inputs.append((from_addr, amount))

    def add_output(self, to_addr, amount):
        self.outputs.append((to_addr, amount))

    def add_reqd(self, addr):
        self.reqd.append(addr)

    def sign(self, private):
        inputs_string = bytes(str(self.inputs), 'utf-8')
        self.sigs.append(Signatures.sign(inputs_string, private))

    def is_valid(self):
        # sprawdzamy czy kazdy input podpisany i dobrym kluczem
        ilosc_wejsc = len(self.inputs)
        ilosc_wejsc_zwalidowanych = 0
        for input in self.inputs:
            for signature in self.sigs:
                if Signatures.verify(bytes(str(self.inputs), 'utf-8'), signature, input[0]):
                    ilosc_wejsc_zwalidowanych +=1
                    if self.debug == 1:
                        print(f"Zwalidowano podpisy {ilosc_wejsc_zwalidowanych} z {ilosc_wejsc} wejść")
                    break
        if ilosc_wejsc_zwalidowanych == ilosc_wejsc:
            if self.debug == 1:
                print("Walidacja podpisow wszyskich wejsc pomyslna")
        else:
            if self.debug == 1:
                print("Nie ma podpisow walidacji wejsc - ODRZUCAMY TRANSAKCJE")
            return False

        # sprawdzamy czy escrow podpisal

        ilosc_escrow = len(self.reqd)
        ilosc_escrow_zwalidowanych = 0

        for escrow in self.reqd:
            for signature in self.sigs:
                if Signatures.verify(bytes(str(self.inputs), 'utf-8'), signature, escrow):
                    ilosc_escrow_zwalidowanych +=1
                    if self.debug == 1:
                        print(f"Zwalidowano podpisy {ilosc_escrow_zwalidowanych} z {ilosc_escrow} escrow")
                    break
        if ilosc_escrow_zwalidowanych == ilosc_escrow:
            if self.debug == 1:
                print("Walidacja escrow pomyslna")
        else:
            if self.debug == 1:
                print("Podpisy escrow niezwalidowane- ODRZUCAMY TRANSAKCE")
            return False

        #sprawdzamy czy wyjscia nie przekraczaja wejsc

        suma_wejsc = 0
        suma_wyjsc = 0

        for input in self.inputs:
            if input[1] < 0:
                if self.debug == 1:
                    print("Wejscie mniejsze niz zero - ODRZUCAMY TRANSAKCJE")
                return False
            suma_wejsc += input[1]

        for output in self.outputs:
            if output[1] < 0:
                if self.debug == 1:
                    print("Wyjscie mniejsze niz zero - ODRZUCAMY TRANSAKCJE")
                return False
            suma_wyjsc += output[1]

        # if suma_wejsc < suma_wyjsc:
        #     if self.debug == 1:
        #         print("Mniej na wejsciu, niz na wyjsciu - ODRZUCAMY TRANSAKCJE")
        #     return False

        if self.debug == 1:
            print("TRANSAKCJA POPRAWNA")
        return True

    def __repr__(self):
        reprstr = "INPUTS:\n"
        for addr, amt in self.inputs:
            reprstr = reprstr + str(amt) + " from " + str(addr) + "\n"
        reprstr = reprstr + "OUTPUTS:\n"
        for addr, amt in self.outputs:
            reprstr = reprstr + str(amt) + " to " + str(addr) + "\n"
        reprstr = reprstr + "REQD:\n"
        for r in self.reqd:
            reprstr = reprstr + str(r) + "\n"
        reprstr = reprstr + "SIGS:\n"
        for s in self.sigs:
            reprstr = reprstr + str(s) + "\n"
        reprstr = reprstr + "END\n"
        return reprstr


if __name__ == "__main__":
    pr1, pu1 = Signatures.generate_keys()
    pr2, pu2 = Signatures.generate_keys()
    pr3, pu3 = Signatures.generate_keys()
    pr4, pu4 = Signatures.generate_keys()

    Tx1 = Tx()
    Tx1.add_input(pu1, 1)
    Tx1.add_output(pu2, 1)
    Tx1.sign(pr1)
    # if Tx1.is_valid():
    #     print("Success! Tx is valid")
    # else:
    #     print("ERROR! Tx is invalid")

    Tx2 = Tx()
    Tx2.add_input(pu1, 2)
    Tx2.add_output(pu2, 1)
    Tx2.add_output(pu3, 1)
    Tx2.sign(pr1)

    Tx3 = Tx()
    Tx3.add_input(pu3, 1.2)
    Tx3.add_output(pu1, 1.1)
    Tx3.add_reqd(pu4)
    Tx3.sign(pr3)
    Tx3.sign(pr4)

    i = 1
    for T in [Tx1, Tx2, Tx3]:
        print()
        print("="*40)
        print(f"Transakcja: {i}")
        T.is_valid()
        # if T.is_valid():
        #     print("Success! Tx is valid")
        # else:
        #     print("ERROR! Tx is invalid")
        # print("="*40)
        i += 1

    #Wrong key used to signed
    Tx4 = Tx()
    Tx4.add_input(pu1, 1)
    Tx4.add_output(pu2,1)
    Tx4.sign(pr2)

    #Arbiter (escrow) did not signed
    Tx5 = Tx()
    Tx5.add_input(pu3, 1.2)
    Tx5.add_output(pu1, 1.1)
    Tx5.add_reqd(pu4)
    Tx5.sign(pr3)

    #Two inputs only one signed
    Tx6 = Tx()
    Tx6.add_input(pu3, 1.2)
    Tx6.add_input(pu4, 0.1)
    Tx6.add_output(pu1, 1.1)
    Tx6.sign(pr3)

    #Outputs exeed inputs
    Tx7 = Tx()
    Tx7.add_input(pu4, 1.2)
    Tx7.add_output(pu1, 1)
    Tx7.add_output(pu2, 2)
    Tx7.sign(pr4)

    #Negative value
    Tx8 = Tx()
    Tx8.add_input(pu2, -1)
    Tx8.add_output(pu1, -1)
    Tx8.sign(pr2)

    for T in [Tx4, Tx5, Tx6, Tx7, Tx8]:
        print()
        print("="*40)
        print(f"TRANSAKCJA: {i}")
        T.is_valid()
        # if T.is_valid():
        #     print("Error! Bad Tx is valid")
        # else:
        #     print("Succes! Tx is invalid")
        print("="* 40)
        i += 1
