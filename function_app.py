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
            pass
        else:
            op = req_body.get('operation')

    try:
        # Create a client and perform the operation.
        client = pylanche.Client(op)
        client.perform(op)
    except Exception as error:
        logging.error(str(error))

    if op == "receive":
        return func.HttpResponse("The function received events from the event hub.")
    elif op == "send":
        return func.HttpResponse("The function sent events to the event hub.")
    else:
        return func.HttpResponse(
             "Pass an operation in the query string or in the request body to receive or send events.",
             status_code=400
        )