import json
import requests

# Read the configuration file.
with open("./pylanche/config.json", "r") as config_file:
    config = json.load(config_file)

app_name = config['APP_NAME']
function_name = config['FUNCTION_NAME']
url = "https://{}.azurewebsites.net/api/{}?operation=receive".format(app_name, function_name)

# Request to perform receive operation.
try:
    resp = requests.post(url=url)
    print(resp.status_code)
except Exception as error:
    print(error)