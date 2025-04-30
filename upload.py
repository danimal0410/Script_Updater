import os
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient import discovery

load_dotenv()


# https://developers.google.com/display-video/api/guides/getting-started/configure

# Set up a flow object to create the credentials using the
# client secrets file and OAuth scopes.
credentials = InstalledAppFlow.from_client_secrets_file(
    path-to-client-secrets-file, oauth-scopes).run_local_server()

# Build the discovery document URL.
discovery_url = f'https://displayvideo.googleapis.com/$discovery/rest?version=v4'

# Build the API service.
service = discovery.build(
    'displayvideo',
    'v4',
    discoveryServiceUrl=discovery_url,
    credentials=credentials)
