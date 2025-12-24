# receive
curl -X POST https://<APP_NAME>.azurewebsites.net/api/<FUNCTION_NAME>?operation=receive

# send
curl -X POST https://<APP_NAME>.azurewebsites.net/api/<FUNCTION_NAME>?operation=send

# anonymize
curl -X POST https://<APP_NAME>.azurewebsites.net/api/<FUNCTION_NAME>?operation=anonymize&text=<TEXT>