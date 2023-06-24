import socket
import auction_server
import encry_decrypt


class AucClient:

    def __init__(self):
        self.target_ip = 'localhost'
        self.target_port = 8888
        self.encryption()

    def client_runner(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.target_ip, self.target_port))
        return client

    def client_menu(self):
        print("This is client menu:")
        user_data = input("Press 1 to sent data: ")
        if user_data == '1':
            client = self.client_runner()
            client.send(bytes("A3", "utf-8"))
            from_server = client.recv(1024).decode("utf-8")
            print(from_server)
            client.close()
        else:
            print("Invalid option!")

    def encryption(self):
        userKey: str = input("Enter encryption for the whole process: ")
        encry = encry_decrypt.A3Encryption()
        encrypted_data = encry.start_encryption("NationalCyberCity", userKey)
        print(encrypted_data)


if __name__ == '__main__':
    auc_client: AucClient = AucClient()
    while True:
        auc_client.client_menu()
