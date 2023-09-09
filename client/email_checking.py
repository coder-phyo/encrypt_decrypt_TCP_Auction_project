class EmailChecking:
    def __init__(self):
        print("checking your email now")

    def start_checking(self, email):
        count = 0
        for i in email:
            if i == "@":
                break
            count += 1

        name_form = email[0:count]
        email_form = email[count:]
        print(name_form, email_form)

        # checking name_form
        name_flag = 0
        for aChar in name_form:
            if (31 < ord(aChar) < 48) or (57 < ord(aChar) < 65) or (90 < ord(aChar) < 97) or (122 < ord(aChar) < 128):
                name_flag = -1
                break

        # checking email_form
        email_flag = 0
        domain_list = ["@facebook.com", "@gmail.com", "@ncc.com", "@mail.ru", "@yahoo.com", "@outlook.com",
                       "@apple.com", "@zoho.com"]

        for i in domain_list:
            if i == email_form:
                email_flag = 1
                break

        if name_flag == -1 or email_flag == 0:
            return -1
        else:
            return 1


if __name__ == '__main__':
    while True:
        email = input("Enter testing email: ")
        email_checking = EmailChecking()
        recv = email_checking.start_checking(email)
        if recv == 1:
            print("valid email")
        else:
            print("invalid email")
