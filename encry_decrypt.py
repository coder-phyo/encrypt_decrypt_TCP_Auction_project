import random


class A3Encryption:

    def __init__(self):
        self.encrypted_data = ''
        self.randomKey = random.randint(1, 65536)

    def start_encryption(self, text, key):

        totalKey = 0
        for i in key:
            totalKey += ord(i)

        key = bin(totalKey)[2:]

        for i in text:
            encrypted_ord = ord(i) ^ totalKey
            doubleEncrypted_ord = encrypted_ord ^ self.randomKey
            print(doubleEncrypted_ord)

            self.encrypted_data += str(hex(doubleEncrypted_ord)) + 'X'

        print(self.encrypted_data)
        self.encrypted_data += str(hex(totalKey)) + 'X' + str(hex(self.randomKey))
        return self.encrypted_data


class A3Decryption:

    def __init__(self):
        self.dataList: list = []
        self.decrypted_data: str = ''

    def start_decryption(self, encrypted_data: str):
        self.dataList = encrypted_data.split('X')
        keyList = self.dataList[-2:]
        print(self.dataList, "key ", keyList)
        key = int(keyList[0], 16)
        rkey = int(keyList[1], 16)

        for i in range(len(self.dataList)-2):
            dDecrypt = int(self.dataList[i], 16) ^ rkey
            decrypted_int = dDecrypt ^ key
            self.decrypted_data += chr(decrypted_int)

        return self.decrypted_data


if __name__ == '__main__':
    a3 = A3Encryption()
    da3 = A3Decryption()
    encrypted = a3.start_encryption("NationalCyberCity", "vinnie")
    decrypted = da3.start_decryption(encrypted)
    print("Decrypted data: ", decrypted)
