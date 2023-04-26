import pandas
import requests
import dotenv
import os


def get_access_token():
    auth = requests.auth.HTTPBasicAuth(
        os.getenv('client_id'),
        os.getenv('secret_token')
    )

    headers = {
        'User-Agent': 'MyBot/0.0.1',
    }

    data = {
        'grant_type': 'password',
        'username': os.getenv('username'),
        'password': os.getenv('password'),
    }

    result = requests.post(
        'https://www.reddit.com/api/v1/access_token',
        auth=auth,
        data=data,
        headers=headers,
    )

    result_json = result.json()
    access_token = result_json['access_token']

    return access_token

def sample_request():
    access_token = get_access_token()

    headers = {
        **headers,
        'Authorization': f"bearer {access_token}",
    }
    result = requests.get(
        'https://oauth.reddit.com/api/v1/me',
        headers=headers
    )

    print(result.json())


def pull_posts():
    pass


if __name__ == '__main__':
    dotenv.load_dotenv()
    sample_request()
