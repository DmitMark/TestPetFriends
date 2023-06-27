import requests

class PetFriends:
    def __init__(self):
        self.base_url = "petfriends.skillfactory.ru/"

    def get_api_key(self, email, password):

        headers = {
            'email': email,
            'password': password
        }