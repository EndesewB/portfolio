import json

class Storage:
    def __init__(self, file_path='data.json'):
        self.file_path = file_path
        self.load_data()  # Load existing data from the JSON file

    def add_user(self, username, email, password):
        if username in self.users:
            return False
        self.users[username] = {'email': email, 'password': password}
        self.save_data()  # Save updated data to the JSON file
        return True

    def save_data(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.users, file, indent=4)

    def load_data(self):
        try:
            with open(self.file_path, 'r') as file:
                data = file.read()
                if not data:
                    self.users = {}  # File is empty, initialize an empty dictionary
                else:
                    self.users = json.loads(data)
        except FileNotFoundError:
            self.users = {}  # File doesn't exist, initialize an empty dictionary

    def get_user_by_username(self, username):
        return self.users.get(username)
