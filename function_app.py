import azure.functions as func
import logging

import pylanche

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        try:
            pylanche.receive()
        except Exception as error:
            logging.error(str(error))
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        try:
            # Send events to the event hub.
            pylanche.send()
            logging.info('The function sent events to the event hub.')
        except Exception as error:
            logging.error(str(error))
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )