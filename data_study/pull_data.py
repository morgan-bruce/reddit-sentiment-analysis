import os

import pandas as pd
import requests
from dotenv import load_dotenv

SUBREDDIT_LIST = [
    'politics',
]


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


def create_endpoint(subreddit):
    return f'https://oauth.reddit.com/r/{subreddit}/top'


def pull_posts():
    access_token = get_access_token()

    headers = {
        'User-Agent': 'MyBot/0.0.1',
        'Authorization': f"bearer {access_token}",
    }

    titles = []
    post_times = []
    links = []
    num_comments = []
    scores = []

    for subreddit in SUBREDDIT_LIST:
        endpoint = create_endpoint(subreddit)
        result = requests.get(
            endpoint,
            headers=headers
        )

        if result.ok:
            json_result = result.json()
            json_result = json_result['data']['children']
            for post in json_result:
                post_data = post['data']
                titles.append(post_data['title'])
                post_times.append(post_data['created'])
                links.append(post_data['permalink'])
                num_comments.append(post_data['num_comments'])
                scores.append(post_data['score'])

    output_df = pd.DataFrame(
        data={
            'title': titles,
            'post_time': post_times,
            'link': links,
            'num_comments': num_comments,
            'score': scores,
        })

    output_df['subreddit'] = output_df['link'].apply(lambda x: x.split('/')[2])
    output_df['post_time'] = pd.to_datetime(output_df['post_time'], unit='s')

    output_columns = ['title', 'subreddit',
                      'post_time', 'num_comments', 'score']
    print(output_df[output_columns])


if __name__ == '__main__':
    load_dotenv()
    pull_posts()
