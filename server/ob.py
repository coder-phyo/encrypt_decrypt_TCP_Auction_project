class Observer:
    def __init__(self):
        print("Starting ob program!")

    def receive_data(self, data):
        print("Received: ", data)
        return data

    def send_data(self, data):
        print("Send: ", data)
        return data


if __name__ == '__main__':
    ob = Observer()
