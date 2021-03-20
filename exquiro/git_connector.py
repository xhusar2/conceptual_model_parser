import requests
import os
from pprint import pprint
import json

# takes empty list, token, owner name, repo name and path (initially empty, used for recursive traversing of github repo
# returns filled xmi_files list with urls
def get_xmi_files(xmi_files, token_val, owner, repo, path=""):
    token = os.getenv('GITHUB_TOKEN', token_val)
    if path == "":
        query_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
    else:
        query_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    if token_val != "":
        headers = {'Authorization': f'token {token}'}
        r = requests.get(query_url, headers=headers)
    else:
        r = requests.get(query_url)
    json_data = json.loads(r.text)
    for json_dict in json_data:
        #print(json_dict)
        if "type" in json_dict:
            #print(json_dict['name'])
            if json_dict['type'] == 'file' and (
                    str(json_dict['name']).endswith('.xmi') or str(json_dict['name']).endswith('.xml')):
                #print('downloading file:', json_dict['name'], json_dict['url'])
                xmi_files.append(json_dict['download_url'])
            if json_dict['type'] == 'dir':
                get_xmi_files(xmi_files, token_val, owner, repo, json_dict['path'])
