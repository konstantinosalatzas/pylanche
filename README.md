# p(y)lanche

pylanche is a Python Azure Function for Event Hubs

It is deployed to a Function App with an HTTP trigger to:

* receive events from an Event Hub for a time duration with an Azure Blob Storage container as a checkpoint store or
* send a number of events to an Event Hub

If the received event message is in JSON format, then it is processed (parsed to dictionary).