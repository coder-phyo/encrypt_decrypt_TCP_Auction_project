import socket
import encry_decrypt
import email_checking
import json


class AucClient:

    def __init__(self):
        self.target_ip = 'localhost'
        self.target_port = 8888
        self.encrypt = encry_decrypt.A3Encryption()
        self.decrypt = encry_decrypt.A3Decryption()
        self.userKey = self.getting_key()

    def client_runner(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.target_ip, self.target_port))
        return client

    def getting_key(self):
        userKey: str = input("Enter encryption key for the whole process: ")
        return userKey

    def client_menu(self):
        print("This is client menu:")
        user_data = input("get:Get_all_information \nlogin:to login \nreg:to register"
                          " \nPress 1 to get auction info: \nPress 2 to Exit: ")
        if user_data == 'get':
            pass
        elif user_data == 'login':
            self.login(user_data)
        elif user_data == 'reg':
            self.registration(user_data)
        elif user_data == '1':
            raw_data: str = "info"
            self.sending_encrypted(raw_data)
        elif user_data == '2':
            exit(1)
        else:
            print("Invalid option!")

    def sending_encrypted(self, raw_data: str):
        encrypted_data = self.encrypt.start_encryption(raw_data, self.userKey)
        client = self.client_runner()
        client.send(bytes(encrypted_data, "utf-8"))
        received_data = client.recv(4096).decode("utf-8")
        decrypted_data = self.decrypt.start_decryption(received_data)
        print("$: ", decrypted_data)
        data = json.loads(decrypted_data)
        for i in range(len(data)):
            print("name - ", data[str(i)]["name"], '***' + " reserve_price - $", data[str(i)]["reserve_price"])
        client.close()

    # def info(self, data):

    def registration(self, data):
        print("This is registration section")
        try:
            user_name = input("Enter name to register:")
            while True:
                user_email = input("Enter email to register:")
                check_email = email_checking.EmailChecking()
                flag = check_email.start_checking(user_email)
                if flag == 1:
                    print("valid email!")
                    break
                else:
                    print("invalid email!Try again.")

            self.final_registration(data, user_name, user_email)

        except Exception as err:
            print(str(err))

    def final_registration(self, data, user_name, user_email):
        if self.email_check_db(user_email):
            while True:
                user_pass = input("Enter password to register:")
                confirm_pass = input("Enter confirm password: ")
                if user_pass == confirm_pass:
                    break
                else:
                    print("incorrect password.Try again!")
            data_list = data + ' ' + user_name + ' ' + user_email + ' ' + user_pass
            encrypted_data = self.encrypt.start_encryption(data_list, self.userKey)
            client = self.client_runner()
            client.send(bytes(encrypted_data, "utf-8"))
            recv_data = client.recv(4096).decode("utf-8")
            decrypted_data = self.decrypt.start_decryption(recv_data)
            print("$: ", decrypted_data)
            client.close()
        else:
            print("Your email was already registered!")
            self.registration(data)

    def login(self, data):
        print("This is login section")
        try:
            l_email = input("Enter your email to login: ")
            l_pass = input("Enter your password to login: ")
            data_form = data + ' ' + l_email + ' ' + l_pass
            encrypted_data = self.encrypt.start_encryption(data_form, self.userKey)
            client = self.client_runner()
            client.send(bytes(encrypted_data, "utf-8"))
            recv_data = client.recv(4096).decode("utf-8")
            decrypted_data = self.decrypt.start_decryption(recv_data)
            if decrypted_data != "user not found":
                user_info: dict = json.loads(decrypted_data)
                self.boss_sector(user_info)
            else:
                print("$: ", decrypted_data)
                self.login(data)
        except Exception as err:
            print(err)

    def boss_sector(self, user_info):
        print("Hollo Boss...")
        print("[+]Name - ", user_info["name"])
        print("Email - ", user_info["email"])
        print("Your point - ", user_info["point"])

        try:
            option = int(input("[+]1::\n[+]2::\n[+]3:Make Auction::\n"))

            if option == 1:
                pass
            elif option == 2:
                pass
            elif option == 3:
                raw_data = "auction " + user_info["email"]
                # data = self.sending_encrypted(raw_data)
            else:
                self.boss_sector(user_info)
        except Exception as err:
            print(err)

    def email_check_db(self, email):
        client = self.client_runner()
        data_form = "emailCheck" + ' ' + email
        encrypted_data = self.encrypt.start_encryption(data_form, self.userKey)
        client.send(bytes(encrypted_data, "utf-8"))
        recv_data = client.recv(4096).decode("utf-8")
        decrypted_data = self.decrypt.start_decryption(recv_data)
        if decrypted_data == "notExist":
            client.close()
            return True
        else:
            client.close()
            return False


if __name__ == '__main__':
    auc_client: AucClient = AucClient()
    while True:
        auc_client.client_menu()
