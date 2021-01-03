back-pockt
==========

back-pockt is a cli utility for offline achiving and indexing of Pocket articles.

Usage
=====

Download Articles
^^^^^^^^^^^^^^^^^

``$ python3 backpockt/get_pocket_data.py -k customer_key -t access_token``

Download Recent
^^^^^^^^^^^^^^^

``$ python3 backpockt/get_pocket_delta.py -k customer_key -t access_token -s unix_timestamp``

How To
======

Pocket Access Token

The following are the manual steps to retrieve a Pocket access token. The process to generate an access token requires 
visiting the https://www.getpocket.com website to allow a user to authorize the "app" and verify the user's 
credentials. The app only needs to be authorized once for each access token. Once the app has been authorized by a 
user, an access token can be created and used to interact with the Pocket APIs.

The web authorization page redirects the "user" to a web page specificed by the user. In a non-cli application, this 
would be the apps web page or app. In this case, it's just a blank page.

If for some reason access is revoked, a new access token can be created using these steps. For development purposes, 
access can be revoked by visiting the web page https://getpocket.com/connected_accounts .

See https://getpocket.com/developer/docs/authentication for the authorization API details.

Step 1
^^^^^^
Obtain a platform consumer key

- See for list of your development apps at
- https://getpocket.com/developer/apps/
- Example customer key... ae940261-4c91-4f07-9c73-a65d6a975e5d

Step 2
^^^^^^
Obtain a request token

- Retrieve a request token using the customer key from step #1 and generic redirect URL.

Request::

    curl 
        -i \\
        -H "X-Accept: application/json" \\
        -H "Content-Type: application/json; charset=UTF8" \\
        -d "{\"consumer_key\":\"ae940261-4c91-4f07-9c73-a65d6a975e5d\", \"redirect_uri\":\"back-pockt:authorizationFinished\"}" \\
        -X POST https://getpocket.com/v3/oauth/request

Response::

    {"code":"4948c13f-d836-4055-b65b-66338bc42a09","state":null}

Step 3
^^^^^^
Redirect user to Pocket to continue authorization

- This step needs to be done once manually in a web browser for each access token
- Once the access token is created, store in a secure place to for use with the Pocket APIs.

URL

https://getpocket.com/auth/authorize?request_token=4948c13f-d836-4055-b65b-66338bc42a09&redirect_uri=back-pockt:authorizationFinished

Step 4
^^^^^^
Receive the callback from Pocket

- Pocket redirects the user to the redirect_uri which simply tries to load a non-existent web page

Step 5
^^^^^^
Convert a request token into a Pocket access token

Request::

    curl 
        -i \
        -H "X-Accept: application/json" \
        -H "Content-Type: application/json; charset=UTF8" \
        -d "{\"consumer_key\":\"ae940261-4c91-4f07-9c73-a65d6a975e5d\", \"code\":\"4948c13f-d836-4055-b65b-66338bc42a09\"}" \
        -X POST https://getpocket.com/v3/oauth/authorize

Response::

    {"access_token":"6c14c378-ca68-4673-b544-cfc8fcae61ca","username":"curent_user"}


Example API Request
^^^^^^^^^^^^^^^^^^^
Retrieve Pocket articles using the access token with the Pocket API::

    curl 
        -i \
        -H "Content-Type: application/json; charset=UTF8" \
        -d "{\"consumer_key\":\"ae940261-4c91-4f07-9c73-a65d6a975e5d\", \"access_token\":\"6c14c378-ca68-4673-b544-cfc8fcae61ca\", \"count\":\"10\", \"detailType\":\"complete\"}" \
        -X GET https://getpocket.com/v3/get
