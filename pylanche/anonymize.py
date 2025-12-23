import logging

from azure.ai.textanalytics import TextAnalyticsClient

def anonymize_text(text: str) -> str:
    anonymized_text = "X"*len(text) # Replace all letters with "X".
    return anonymized_text

def recognize_names(client: TextAnalyticsClient, documents: list[str]):
    try:
        result = client.recognize_entities(documents=documents)[0]
        anonymization = {} # Map names to their anonymized forms.
        for entity in result['entities']:
            print("Text:", entity.text,
                  "Category:", entity.category,
                  "Subcategory:", entity.subcategory,
                  "Confidence Score:", round(entity.confidence_score, 2),
                  "Length:", entity.length,
                  "Offset:", entity.offset)
            if entity.category == "Person":
                anonymized_text = anonymize_text(entity.text)
                print(entity.text, "->", anonymized_text)
                anonymization[entity.text] = anonymized_text
    except Exception as error:
        logging.info(str(error))

def anonymize(client: TextAnalyticsClient):
    documents = ["I trained planche hold to press with Konstantinos."]
    recognize_names(client, documents)