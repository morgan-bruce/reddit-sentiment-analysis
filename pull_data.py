import os
import itertools

import pandas as pd
import requests
from dotenv import load_dotenv

SUBREDDIT_LIST = [
    "politics",
    "news",
]

ORDERING_LIST = [
    "top",
]

POST_DATA_COLS = [
    "title",
    "created",
    "permalink",
    "num_comments",
    "score",
]

SAVE_DATA_COLS = [
    "title",
    "subreddit",
    "created",
    "num_comments",
    "score",
]

CSV_PATH = "data.csv"


def get_default_headers(access_token=None):
    headers = {"User-Agent": "MyBot/0.0.1"}
    if access_token:
        headers["Authorization"] = f"bearer {access_token}"
    return headers


def get_access_token():
    load_dotenv()

    auth = requests.auth.HTTPBasicAuth(
        os.getenv("client_id"), os.getenv("secret_token")
    )

    headers = get_default_headers()

    data = {
        "grant_type": "password",
        "username": os.getenv("username"),
        "password": os.getenv("password"),
    }

    result = requests.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=auth,
        data=data,
        headers=headers,
    )

    result_json = result.json()
    access_token = result_json["access_token"]

    return access_token


def create_endpoint(subreddit, ordering):
    return f"https://oauth.reddit.com/r/{subreddit}/{ordering}"


def save_df(df, path):
    if os.path.exists(path):
        os.remove(path)
    df.to_csv(CSV_PATH)


def create_cols_dict(cols):
    output_dict = dict()
    for col in cols:
        output_dict[col] = []
    return output_dict


def add_data_from_json(json, output_dict):
    json_result = json.json()
    json_result = json_result["data"]["children"]
    for post in json_result:
        post_data = post["data"]
        for col in POST_DATA_COLS:
            output_dict[col].append(post_data[col])
    return output_dict


def pull_posts_from_subreddit(subreddit, ordering, headers, output_dict):
    endpoint = create_endpoint(subreddit, ordering)
    result = requests.get(endpoint, headers=headers)

    if result.ok:
        output_dict = add_data_from_json(result, output_dict)
    else:
        result.raise_for_status()

    return output_dict


def format_dataframe(df):
    df["subreddit"] = df["permalink"].apply(lambda x: x.split("/")[2])
    df["created"] = pd.to_datetime(df["created"], unit="s")
    df = df[SAVE_DATA_COLS]
    return df


def pull_posts():
    access_token = get_access_token()
    headers = get_default_headers(access_token)
    post_cols_dict = create_cols_dict(POST_DATA_COLS)
    for subreddit, ordering in itertools.product(SUBREDDIT_LIST, ORDERING_LIST):
        post_cols_dict = pull_posts_from_subreddit(
            subreddit, ordering, headers, post_cols_dict
        )
    output_df = pd.DataFrame(data=post_cols_dict)
    output_df = format_dataframe(output_df)
    save_df(output_df, CSV_PATH)


if __name__ == "__main__":
    pull_posts()
