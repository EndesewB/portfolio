import json
import os
from datetime import datetime

class BaseModel:
    _id_counter = 0  # Class variable to track the next available ID

    def __init__(self):
        self.instance_id = BaseModel._id_counter
        BaseModel._id_counter += 1
        self.created_at = datetime.now()
        self.updated_at = self.created_at

    def save_data(self):
        data = {
            'instance_id': self.instance_id,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

        filename = f"{self.__class__.__name__.lower()}_{self.instance_id}.json"
        with open(filename, 'w') as file:
            json.dump(data, file)

    def reload_data(self):
        filename = f"{self.__class__.__name__.lower()}_{self.instance_id}.json"
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                data = json.load(file)
                self.created_at = datetime.strptime(data.get('created_at'), '%Y-%m-%d %H:%M:%S')
                self.updated_at = datetime.strptime(data.get('updated_at'), '%Y-%m-%d %H:%M:%S')

    @classmethod
    def call_all(cls):
        instances = []
        for filename in os.listdir():
            if filename.startswith(cls.__name__.lower() + '_') and filename.endswith('.json'):
                instance_id = int(filename.split('_')[-1].split('.')[0])
                instance = cls()
                instance.instance_id = instance_id
                instance.reload_data()
                instances.append(instance)
        return instances

class User(BaseModel):
    def __init__(self, username, email, password):
        super().__init__()
        self.username = username
        self.email = email
        self.password = password

    def save_data(self):
        data = {
            'instance_id': self.instance_id,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'username': self.username,
            'email': self.email,
            'password': self.password
        }

        filename = f"{self.__class__.__name__.lower()}_{self.instance_id}.json"
        with open(filename, 'w') as file:
            json.dump(data, file)

    @classmethod
    def create_user(cls, username, email, password):
        user = cls(username, email, password)
        user.save_data()
        return user

    @classmethod
    def get_user_by_username(cls, username):
        for user in cls.call_all():
            if user.username == username:
                return user
        return None

    @classmethod
    def get_user_by_email(cls, email):
        for user in cls.call_all():
            if user.email == email:
                return user
        return None
