# without parameters
curl -X POST https://<APP_NAME>.azurewebsites.net/api/<FUNCTION_NAME>

# with the "operation" parameter as "receive"
curl -X POST https://<APP_NAME>.azurewebsites.net/api/<FUNCTION_NAME>?operation=receive

# with the "operation" parameter as "send"
curl -X POST https://<APP_NAME>.azurewebsites.net/api/<FUNCTION_NAME>?operation=send