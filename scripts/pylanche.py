import json
import requests

# Read the configuration file.
with open("./pylanche/config.json", "r") as config_file:
    config = json.load(config_file)

app_name = config['APP_NAME']
function_name = config['FUNCTION_NAME']