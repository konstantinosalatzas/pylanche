# p(y)lanche

pylanche is a Python Azure Function for Event Hubs

It is deployed to a Function App with an HTTP trigger to:

* receive events from an Event Hub for a time duration with an Azure Blob Storage container as a checkpoint store or
* send a number of events and the data read from a CSV file stored in an Azure Blob Storage container as events to an Event Hub

## Input parameters

The HTTP trigger expects the input parameter `operation` with the value `receive` or `send` of the operation to perform.

If the value of `operation` is:

* `receive`, then another input parameter `duration` is expected with the number of seconds to receive.
* `send`, then another input parameter `count` is expected with the number of events to send.

## Configuration

The configuration of Event Hub, checkpoint store and send file is done with environment variables or the JSON file:

[pylanche/config.json](https://github.com/konstantinosalatzas/pylanche/blob/main/pylanche/config_template.json)

## Extra features

If the HTTP trigger is executed with the value `anonymize` as the input parameter `operation`, then it expects another input parameter `text` and performs anonymization of names contained in `text`, replacing them with masked values in the response text.

The anonymization is performed with the Azure Language service and the [Named Entity Recognition (NER)](https://learn.microsoft.com/en-us/azure/ai-services/language-service/named-entity-recognition/overview) technique.

The configuration of the Azure Language service is done with environment variables or the configuration JSON file.