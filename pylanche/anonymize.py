import logging

from azure.ai.textanalytics import TextAnalyticsClient

def replace_mapped(text: str, map: dict[str, str]) -> str:
    # Replace names in text with their anonymized forms.
    for s in map:
        text = text.replace(s, map[s])
    return text

def anonymize_text(text: str) -> str:
    anonymized_text = "X"*len(text) # Replace all letters with "X".
    return anonymized_text

def recognize_names(client: TextAnalyticsClient, text: str) -> dict[str, str] | None:
    try:
        anonymization = {} # Map names to their anonymized forms.
        result = client.recognize_entities(documents=[text])[0]

        # Recognize named entities.
        for entity in result['entities']:
            print("Text: {}, Category: {}, Subcategory: {}, Confidence Score: {}, Length: {}, Offset: {}".format(entity.text, entity.category, entity.subcategory, entity.confidence_score, entity.length, entity.offset))
            logging.info("Text: {}, Category: {}, Subcategory: {}, Confidence Score: {}, Length: {}, Offset: {}".format(entity.text, entity.category, entity.subcategory, entity.confidence_score, entity.length, entity.offset))
            if entity.category == "Person":
                anonymized_text = anonymize_text(entity.text)
                anonymization[entity.text] = anonymized_text

        return anonymization
    except Exception as error:
        logging.info(str(error))
        return None

def anonymize(client: TextAnalyticsClient, text: str) -> str | None:
    print("Input text: {}".format(text))
    logging.info("Input text: {}".format(text))

    names = recognize_names(client, text)
    if names == None:
        return None

    print("Anonymization map: {}".format(names))
    logging.info("Anonymization map: {}".format(names))

    anonymized_text = replace_mapped(text, names)

    print("Anonymized text: {}".format(anonymized_text))
    logging.info("Anonymized text: {}".format(anonymized_text))

    return anonymized_text