import socket
import s_encry_decrypt
import ob
import pymongo
import json
from dbModal import NccAuctionModal

connection = pymongo.MongoClient("localhost", 27017)
database = connection["ncc_dip2"]
user_info = database["user_info"]


class AucServer:

    def __init__(self):
        self.server_ip = 'localhost'
        self.server_port = 8888
        self.decrypt = s_encry_decrypt.A3Decryption()
        self.encrypt = s_encry_decrypt.A3Encryption()
        self.ob = ob.Observer()
        self.rc = RequestControl()

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
            from_client = sock.recv(4096)
            data_list = from_client.decode("utf-8")
            decrypted = self.decrypt.start_decryption(data_list)
            print("#: ", decrypted)
            decrypted_list = decrypted.split(' ')
            # ob_recv = self.ob.receive_data(decrypted_list[0])
            # print("OB receive:", ob_recv)

            if decrypted_list[0] == "info":
                data = self.rc.info(decrypted_list)
            elif decrypted_list[0] == "emailCheck":
                data = self.rc.email_checking(decrypted_list)
            elif decrypted_list[0] == "reg":
                data = self.rc.register(decrypted_list)
            elif decrypted_list[0] == "login":
                data = self.rc.login(decrypted_list)

            encrypted = self.encrypt.start_encryption(data, 'servertcp')

            sock.send(bytes(encrypted, "utf-8"))

            ob_send = self.ob.send_data(data)
            print("Ob send:", ob_send)

    # def get_auction_info(self, sock, decrypted_list):
    #     ob_recv = self.ob.receive_data(decrypted_list[0])
    #     print("OB receive:", ob_recv)
    #
    #     data = ''
    #     if decrypted_list[0] == "info":
    #         data = self.rc.info(decrypted_list)


class RequestControl:
    def __init__(self):
        self.database = NccAuctionModal()

    def info(self, decrypted_list):
        data = {}
        collection = self.database.item()
        for i in collection.find({}, {'_id': 0}):
            id_ = int(len(data))
            data.update({id_: {"name": i["name"], "reserve_price": i["reserve_price"]}})

        data = json.dumps(data)
        return data

    def register(self, decrypted_list):
        data_form: dict = {"name": decrypted_list[1], "email": decrypted_list[2], "password": decrypted_list[3]}
        ids = user_info.insert_one(data_form)
        message = "Registration success for id:" + str(ids.inserted_id)
        return message

    def login(self, decrypted_list):
        flag = -1
        data = {}
        for i in user_info.find():
            if i["email"] == decrypted_list[1] and i["password"] == decrypted_list[2]:
                flag = i["_id"]
                data = {"name": i["name"], "email": i["email"]}
                break

        if flag != -1:
            info = "Welcome " + data["name"] + ": " + str(flag)
            data.update({"info": info})
            data = json.dumps(data)
            return data
        else:
            data = "user not found"
            return data

    def email_checking(self, decrypted_list):
        email_exist = 0
        for i in user_info.find({}, {"_id": 0, "email": 1}):
            if i["email"] == decrypted_list[1]:
                email_exist = -1
                break

        if email_exist == 0:
            data = "notExist"
            return data
        else:
            data = "exist"
            return data


if __name__ == '__main__':
    auc_server: AucServer = AucServer()
    auc_server.main()
