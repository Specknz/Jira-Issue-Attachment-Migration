import requests
from requests.auth import HTTPBasicAuth
import base64
import sys

SERVER_TICKET = sys.argv[1]
CLOUD_TICKET = sys.argv[2]

SERVER_DOMAIN = "https://SERVERDOMAIN"
CLOUD_DOMAIN = "https://CLOUDDOMAIN.atlassian.net"

__API_TOKEN = "TOKEN"
__USERNAME = "USERNAME"
__EMAIL = "EMAIL"
__PASSWORD = "PASSWORD"
__CREDENTIALS = __USERNAME + ":" + __PASSWORD


def get_credentials() -> str:
    return __CREDENTIALS

class EncodedCredentials:
    def __init__(self):
        self.encoded_credentials = self.__encode_credentials(get_credentials())

    def __encode_credentials(self, creds) -> str:
        return base64.b64encode(creds.encode("ascii")).decode("utf-8")


def get_issue_data() -> list:
    credentials = EncodedCredentials().encoded_credentials
    endpoint = f"{SERVER_DOMAIN}/rest/api/2/issue/{SERVER_TICKET}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {credentials}"
    }
    with requests.get(url=endpoint, headers=headers) as response:
        response.raise_for_status()
        response_json = response.json()
        return [i["content"] for i in response_json["fields"]["attachment"]]


def post_attachment(attachment_url) -> None:
    credentials = EncodedCredentials().encoded_credentials
    attachment_name = attachment_url.split('/')[-1]
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {credentials}"
    }
    with requests.get(url=attachment_url, headers=headers) as f:
        endpoint = f"{CLOUD_DOMAIN}/rest/api/2/issue/{CLOUD_TICKET}/attachments"
        auth = HTTPBasicAuth(__EMAIL, __API_TOKEN)
        headers = {
            "X-Atlassian-Token": "no-check"
        }
        with requests.post(url=endpoint, auth=auth, headers=headers, files={f"file": (attachment_name, f.content)}) as response:
            response.raise_for_status()


attachment_url_list = get_issue_data()
for attachment_url in attachment_url_list:
    post_attachment(attachment_url)