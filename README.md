# Setup

```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

echo username={your username} >> .env
echo password={your password} >> .env
echo client_id={your client id} >> .env
echo secret_token={your secret token} >> .env
```

Get client id and secret token from https://www.reddit.com/prefs/apps/.
