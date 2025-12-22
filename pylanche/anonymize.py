from azure.ai.textanalytics import TextAnalyticsClient

def recognize_names(client: TextAnalyticsClient, documents: list[str]):
    print(documents)
    try:
        result = client.recognize_entities(documents=documents)[0]
        for entity in result['entities']:
            print("Text: ", entity.text,
                  "Category: ", entity.category,
                  "SubCategory: ", entity.subcategory,
                  "Confidence Score: ", round(entity.confidence_score, 2),
                  "Length: ", entity.length,
                  "Offset: ", entity.offset)
    except Exception as error:
        print(error)

def anonymize(client: TextAnalyticsClient):
    documents = ["I trained planche hold to press with Kostas."]
    recognize_names(client, documents)