# receive
curl -X POST https://<APP_NAME>.azurewebsites.net/api/<FUNCTION_NAME>?operation=receive&duration=3

# send
curl -X POST https://<APP_NAME>.azurewebsites.net/api/<FUNCTION_NAME>?operation=send&count=3

# anonymize
curl -X POST https://<APP_NAME>.azurewebsites.net/api/<FUNCTION_NAME>?operation=anonymize&text=<TEXT>