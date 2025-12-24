import logging

from azure.ai.textanalytics import TextAnalyticsClient

def replace_mapped(text: str, map: dict[str, str]) -> str:
    for s in map:
        text = text.replace(s, map[s])
    return text

def anonymize_text(text: str) -> str:
    anonymized_text = "X"*len(text) # Replace all letters with "X".
    return anonymized_text

def recognize_names(client: TextAnalyticsClient, text: str) -> dict[str, str] | None:
    try:
        result = client.recognize_entities(documents=[text])[0]
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
                anonymization[entity.text] = anonymized_text
        return anonymization
    except Exception as error:
        logging.info(str(error))
        return None

def anonymize(client: TextAnalyticsClient, text: str) -> str:
    print(text)
    names = recognize_names(client, text)
    print(names)
    text = replace_mapped(text, names)
    print(text)
    return text