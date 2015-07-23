#!/usr/bin/env python
#https://github.com/reddit/reddit/wiki/OAuth2-Python-Example
CLIENT_ID = "p-jcoLKBynTLew"
CLIENT_SECRET = "gko_LXELoV07ZBNUXrvWZfzE3aI"
REDIRECT_URI = "http://localhost:65010/reddit_callback"
GETTOKEN_URI = "https://graph.api.smartthings.com/oauth/authorize?response_type=code&client_id=eee56833-a696-439d-a30f-5b4c01b8416e&scope=app&redirect_uri=https%3A%2F%2Fgraph.api.smartthings.com%2Foauth%2Fcallback"
BASE_URI = "https://graph.api.smartthings.com/"
OAUTH_URL = "https://graph.api.smartthings.com/oauth/authorize?response_type=code&client_id=%s&scope=app&redirect_uri=%s"
REDIRECT_URI = "https%3A%2F%2Fgraph.api.smartthings.com%2Foauth%2Fcallback"

 #os.getenv('DATABASE_URL',     'mysql://root:biteme13@localhost/FrameWork')



from flask import Flask
app = Flask(__name__)
@app.route('/')
def homepage():
    text = '<a href="%s">Authenticate with reddit</a>'
    return text % make_authorization_url()

def make_authorization_url():
    # Generate a random string for the state parameter
    # Save it for use later to prevent xsrf attacks
    from uuid import uuid4
    state = str(uuid4())
    save_created_state(state)
    params = {"client_id": CLIENT_ID,
              "response_type": "code",
              "state": state,
              "redirect_uri": REDIRECT_URI,
              "duration": "temporary",
              "scope": "identity"}
    import urllib
    url = "https://ssl.reddit.com/api/v1/authorize?" + urllib.urlencode(params)
    return url
  
import requests
import requests.auth
def get_token(code):
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    post_data = {"grant_type": "authorization_code",
                 "code": code,
                 "redirect_uri": REDIRECT_URI}
    response = requests.post("https://ssl.reddit.com/api/v1/access_token",
                             auth=client_auth,
                             data=post_data)
    token_json = response.json()
    return token_json["access_token"]
  
def get_username(access_token):
    headers = {"Authorization": "bearer " + access_token}
    response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)
    me_json = response.json()
    return me_json['name']

@app.route('/reddit_callback')
def reddit_callback():
    error = request.args.get('error', '')
    if error:
        return "Error: " + error
    state = request.args.get('state', '')
    if not is_valid_state(state):
        # Uh-oh, this request wasn't started by us!
        abort(403)
    code = request.args.get('code')
    # We'll change this next line in just a moment
    return "got a code! %s" % code
    #return "got an access token! %s" % get_token(code)
    #access_token = get_token(code)
    #return "Your reddit username is: %s" % get_username(access_token)
# Left as an exercise to the reader.
# You may want to store valid states in a database or memcache,
# or perhaps cryptographically sign them and verify upon retrieval.
def save_created_state(state):
    pass
def is_valid_state(state):
    return True


if __name__ == '__main__':
    app.run(debug=True, port=65010)