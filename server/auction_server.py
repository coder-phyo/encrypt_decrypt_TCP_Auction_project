import socket
import encry_decrypt


class AucServer:

    def __init__(self):
        self.server_ip = 'localhost'
        self.server_port = 8888
        self.a3Decryption = encry_decrypt.A3Decryption()

    def main(self):
        auction_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        auction_server.bind((self.server_ip, self.server_port))
        auction_server.listen()
        print("Server is listen on - {}:{}".format(self.server_ip, self.server_port))

        while True:
            client, address = auction_server.accept()
            self.client_control(client)
            print("Accepted connection from - {}:{}".format(address[0], address[1]))

    def client_control(self, client):
        with client as sock:
            from_client = sock.recv(1024)
            data_list = from_client.decode("utf-8")
            dec_data = self.decryption(data_list)
            sock.send(bytes(dec_data, "utf-8"))

    def decryption(self, data_list):
        decrypted_data = self.a3Decryption.start_decryption(data_list)
        return decrypted_data


if __name__ == '__main__':
    auc_server: AucServer = AucServer()
    auc_server.main()