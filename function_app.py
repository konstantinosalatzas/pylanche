import azure.functions as func
import logging

import pylanche

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

op_to_param = {"receive": "duration",
               "send": "count",
               "anonymize": "text"} # Map the value of the operation input parameter to the name of the combined input parameter.

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
        return func.HttpResponse("The request parameter combination is not supported.",
                                 status_code=400)

    # Get the operation-specific input parameter.
    if op == "receive":
        param = get_parameter(req, 'duration')
    if op == "send":
        param = get_parameter(req, 'count')
    if op == "anonymize":
        param = get_parameter(req, 'text')

    try:
        # Create a client and perform the operation.
        client = pylanche.Client(op)
        ret = client.perform(op, param)
        
        if op == "receive":
            return func.HttpResponse("The function received events from the event hub.")
        if op == "send":
            return func.HttpResponse("The function sent events to the event hub.")
        if op == "anonymize":
            if ret == None:
                return func.HttpResponse("The function failed to perform the operation, please check the logs.",
                                         status_code=500)
            return func.HttpResponse(ret) # Respond with the anonymized text.
    except Exception as error:
        logging.error(str(error))
        return func.HttpResponse("The function failed to perform the operation, please check the logs.",
                                 status_code=500)