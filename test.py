# pii_detector.py
import time
import json
from gliner import GLiNER
from rich import print
from concurrent.futures import ThreadPoolExecutor, as_completed

# ---------- Load model once ----------
model = GLiNER.from_pretrained(
    "knowledgator/gliner-pii-base-v1.0"
)

PII_LABELS = [
    "PERSON", "EMAIL", "PHONE", "ADDRESS",
    "CREDIT_CARD", "SSN", "PASSPORT",
    "API_KEY", "JWT", "IP_ADDRESS"
]


def process_single_text(text: str) -> tuple[str, list]:
    """
    Process a single text for PII detection
    Returns: (text, entities_list)
    """
    entities = model.predict_entities(text, PII_LABELS)
    return text, entities


def gliner_pii_batch(texts: list[str]):
    """
    Batch PII detection using GLiNER with parallel processing
    GLiNER's predict_entities doesn't accept a list, so we process each text individually
    and parallelize using ThreadPoolExecutor
    """
    results = []
    max_workers = min(len(texts), 10)  # Limit to 10 workers max
    
    # Use ThreadPoolExecutor to parallelize processing
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_text = {
            executor.submit(process_single_text, text): text
            for text in texts
        }
        
        # Collect results in order
        text_to_entities = {}
        for future in as_completed(future_to_text):
            text, entities = future.result()
            text_to_entities[text] = entities
    
    # Build results maintaining original order
    for text in texts:
        ents = text_to_entities[text]
        results.append({
            "text": text,
            "entities": [
                {
                    "label": e["label"],
                    "text": e["text"],
                    "start": e["start"],
                    "end": e["end"],
                    "score": round(e["score"], 3),
                    "source": "model"
                }
                for e in ents
            ]
        })
    
    return results


def detect_pii_batch(texts: list[str]):
    results = gliner_pii_batch(texts)
    return {
        "batch_size": len(texts),
        "contains_pii": any(r["entities"] for r in results),
        "results": results
    }


if __name__ == "__main__":
    texts = [
        "My name is John Doe and I live in New York.",
        "Please contact me at alice.smith@gmail.com for further details.",
        "My phone number is +1-415-555-2671.",
        "The credit card used was 4111 1111 1111 1111.",
        "Passport number A12345678 was verified successfully.",
        "Send the package to 221B Baker Street, London.",
        "My SSN is 123-45-6789.",
        "Login attempt from IP address 192.168.1.45.",
        "The API key used was sk_live_51N8abcdEfgh.",
        "JWT token detected: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.",
        "Please call emergency contact at 9876543210.",
        "Customer name: Michael Johnson, account verified.",
        "Employee email id: hr-support@company.org.",
        "Payment made using card number 5500 0000 0000 0004.",
        "User location: 1600 Amphitheatre Parkway, Mountain View, CA.",
        "SSN of the applicant was recorded as 987-65-4321.",
        "Incoming request from IP 10.0.0.12.",
        "Temporary API key: api_test_9f8e7d6c5b4a.",
        "User named Sarah Connor registered successfully.",
        "No sensitive data in this sentence."
    ]

    start_time = time.perf_counter()
    output = detect_pii_batch(texts)
    end_time = time.perf_counter()

    print(json.dumps(output, indent=4))
    print(f"\nTotal time for batch of {len(texts)}: {end_time - start_time:.4f} seconds")
    print(f"Avg per text: {(end_time - start_time) / len(texts):.4f} seconds")

