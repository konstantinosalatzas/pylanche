import azure.functions as func
import logging

import pylanche

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

def get_parameter(req: func.HttpRequest, param: str) -> str | None:
    val = req.params.get(param)
    if not val:
        try:
            req_body = req.get_json()
        except ValueError:
            logging.error("The request body does not contain valid JSON data.")
        else:
            val = req_body.get(param)
    return str(val)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    op = get_parameter(req, 'operation')

    if op not in ["receive", "send", "anonymize"]:
        return func.HttpResponse("Pass 'operation' with 'receive' or 'send' value in the query string or in the request body.",
                                 status_code=400)

    if op == "send":
        count = get_parameter(req, 'count')
    if op == "anonymize":
        text = get_parameter(req, 'text')

    try:
        # Create a client and perform the operation.
        client = pylanche.Client(op)
        
        if op == "receive":
            client.perform(op, None)
        if op == "send":
            client.perform(op, count)
        if op == "anonymize":
            anonymized_text = client.perform(op, text)
        
        if op == "receive":
            return func.HttpResponse("The function received events from the event hub.")
        if op == "send":
            return func.HttpResponse("The function sent events to the event hub.")
        if op == "anonymize":
            if anonymized_text == None:
                return func.HttpResponse("The function failed to perform the operation, please check the logs.",
                                         status_code=500)
            return func.HttpResponse(anonymized_text)
    except Exception as error:
        logging.error(str(error))
        return func.HttpResponse("The function failed to perform the operation, please check the logs.",
                                 status_code=500)