from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

def recognize_names(client: TextAnalyticsClient, documents: list[str]):
    print(documents)

def anonymize(client: TextAnalyticsClient):
    documents = ["I trained planche hold to press with Kostas."]
    recognize_names(client, documents)