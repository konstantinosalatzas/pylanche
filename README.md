# p(y)lanche

pylanche is a Python Azure Function for Event Hubs

It is deployed to a Function App with an HTTP trigger to:

* receive events from an Event Hub for a time duration with an Azure Blob Storage container as a checkpoint store or
* send a number of events and the data read from a CSV file stored in an Azure Blob Storage container as events to an Event Hub

If a received event message is in JSON format, then it is processed (parsed to dictionary).

## Input

The HTTP trigger expects the input parameter `operation` with the value `receive` or `send` of the operation to perform.

## Configuration

The configuration of Event Hub, checkpoint store, receive duration, send file and send count is done with environment variables or the JSON file:

[pylanche/config.json](https://github.com/konstantinosalatzas/pylanche/blob/main/pylanche/config_template.json)

## Extra features

If the HTTP trigger is executed with the value `anonymize` as the input parameter `operation`, then it expects another input parameter `text` and performms anonymization of names contained in `text`, replacing them with masked values in the response text.

The anonymization is performed with the Named Entity Recognition (NER) technique.