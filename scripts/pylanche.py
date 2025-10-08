"""Script to receive on repeat"""

import json
import requests

# Read the configuration file.
with open("./pylanche/config.json", "r") as config_file:
    config = json.load(config_file)

# Prepare the request URL to perform the receive operation.
app_name = config['APP_NAME']
function_name = config['FUNCTION_NAME']
url = "https://{}.azurewebsites.net/api/{}?operation=receive".format(app_name, function_name)

# Repeat performing the receive operation.
while True:
    # Request to perform receive operation.
    try:
        resp = requests.post(url=url)
        print(f"{resp.text} ({resp.status_code})")
    except Exception as error:
        print(error)