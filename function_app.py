import azure.functions as func
import logging

import pylanche

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    op = req.params.get('operation')
    if not op:
        try:
            req_body = req.get_json()
        except ValueError:
            logging.error("The request body does not contain valid JSON data.")
        else:
            op = req_body.get('operation')

    if op not in ["receive", "send", "anonymize"]:
        return func.HttpResponse(
                "Pass 'operation' with 'receive' or 'send' value in the query string or in the request body.",
                status_code=400
        )

    if op == "anonymize":
        text = req.params.get('text')
        if not text:
            try:
                req_body = req.get_json()
            except ValueError:
                logging.error("The request body does not contain valid JSON data.")
            else:
                text = req_body.get('text')

    try:
        # Create a client and perform the operation.
        client = pylanche.Client(op)
        
        if op in ["receive", "send"]:
            client.perform(op, None)
        if op == "anonymize":
            text = client.perform(op, text)
        
        if op == "receive":
            return func.HttpResponse("The function received events from the event hub.")
        if op == "send":
            return func.HttpResponse("The function sent events to the event hub.")
        if op == "anonymize":
            if text == None:
                return func.HttpResponse("The function failed to perform the operation, please check the logs.",
                                         status_code=500)
            return func.HttpResponse(text)
    except Exception as error:
        logging.error(str(error))
        return func.HttpResponse(
                "The function failed to perform the operation, please check the logs.",
                status_code=500
        )