To implement **Theme 1: The Hallucination Lie Detector**, you are essentially building a "Judge" LLM that sits on top of your RAG pipeline. Its sole purpose is to verify the relationship between the **Retrieved Context** and the **Generated Answer**.

### Understanding Theme 1: Faithfulness & Adherence

In a standard RAG setup, the LLM sometimes relies on its "internal knowledge" (pre-training data) rather than the documents you provided. This is a "hallucination" in the context of RAG, even if the statement is factually true in the real world.

#### The "Shadow Knowledge" Example

* **User Question:** "What is our company's policy on remote work in France?"
* **Retrieved Context:** "Employees in the Paris office must be in-person 2 days a week."
* **LLM Answer:** "Our policy allows for full remote work globally, including France."
* **The Problem:** The LLM "remembered" a general trend or a different document it saw during training, completely ignoring the specific Paris office constraint provided in the context.

---

### How Our Solution Solves This (The "NLI" Approach)

We solve this using **Natural Language Inference (NLI)**. Instead of just "guessing" if the answer is right, our platform breaks the verification into two distinct technical steps: **Claim Extraction** and **Entailment Checking**.

#### 1. Claim Extraction

We use a high-speed LLM (like GPT-4o-mini or Claude Haiku) to break the bot's answer into individual atomic facts.

* *Answer:* "The policy requires 2 days in-office and offers a €500 home-office stipend."
* *Atomic Claims:*
1. "Policy requires 2 days in-office."
2. "Policy offers a €500 home-office stipend."



#### 2. Entailment (The Cross-Examination)

For each atomic claim, we ask the Judge LLM: *"Based ONLY on the provided context, is this claim supported, refuted, or neutral?"*

* If the context says nothing about a stipend, the second claim is flagged as **"Not Supported" (Hallucination)**.

---

### Technical Implementation

Our platform implements this using a two-stage LLM pipeline that automatically extracts and verifies claims from RAG-generated responses.

#### How It Works

1. **Claim Extraction**: The LLM response is broken down into individual atomic claims using GPT-4.1
2. **Claim Verification**: Each claim is cross-examined against the retrieved context to determine if it's supported
3. **Score Calculation**: A faithfulness score is calculated as the ratio of supported claims to total claims

---

## API Endpoint: Evaluate Faithfulness

### Endpoint

```
POST /api/v1/agent/evaluate-faithfulness
```

**Base URL:** `http://localhost:8000` (development)

### Authentication

Requires API key authentication via the `X-API-Key` header.

### Request Body

The endpoint accepts a JSON payload with the following structure:

```json
{
  "query": "What is the company's remote work policy?",
  "context_retrieved": {
    "chunk_1": {
      "content": "The company requires employees to work 2 days per week in the office. Remote workers receive a €500 monthly stipend for home office setup.",
      "chunk_id": "chunk_1",
      "score": 0.95
    },
    "chunk_2": {
      "content": "All employees must attend mandatory team meetings on Mondays and Wednesdays.",
      "chunk_id": "chunk_2",
      "score": 0.87
    }
  },
  "llm_response": "The company requires 2 days in-office per week and offers a €500 home-office stipend. All employees must attend mandatory meetings on Mondays and Wednesdays."
}
```

#### Request Schema

- **query** (string, required): The original user query that triggered the RAG response
- **context_retrieved** (object, required): Dictionary of context chunks retrieved from the vector database
  - Each chunk contains:
    - **content** (string): The text content of the chunk
    - **chunk_id** (string): Unique identifier for the chunk
    - **score** (float): Relevance score between 0.0 and 1.0
- **llm_response** (string, required): The LLM-generated response to be evaluated

### Response

The endpoint returns a comprehensive evaluation result with verdicts for each claim and an overall faithfulness score.

#### Success Response (200 OK)

```json
{
    "verdicts": [
        {
            "claim_text": "The company requires 2 days in-office per week.",
            "verdict": "SUPPORTED",
            "reasoning": "Chunk 1 explicitly states: 'The company requires employees to work 2 days per week in the office.'"
        },
        {
            "claim_text": "The company offers a €500 home-office stipend.",
            "verdict": "SUPPORTED",
            "reasoning": "Chunk 1 states: 'Remote workers receive a €500 monthly stipend for home office setup,' which supports the claim."
        },
        {
            "claim_text": "All employees must attend mandatory meetings on Mondays.",
            "verdict": "SUPPORTED",
            "reasoning": "Chunk 2 states: 'All employees must attend mandatory team meetings on Mondays and Wednesdays.' Thus, mandatory meetings on Mondays are supported."
        },
        {
            "claim_text": "All employees must attend mandatory meetings on Wednesdays.",
            "verdict": "SUPPORTED",
            "reasoning": "Chunk 2 states: 'All employees must attend mandatory team meetings on Mondays and Wednesdays.' Thus, mandatory meetings on Wednesdays are supported."
        }
    ],
    "total_claims": 4,
    "supported_claims": 4,
    "not_supported_claims": 0,
    "faithfullness_score": 1.0
}
```

#### Response Schema

- **verdicts** (array): List of claim verification results
  - **claim_text** (string): The exact claim that was verified
  - **verdict** (string): Either `"SUPPORTED"` or `"NOT_SUPPORTED"`
  - **reasoning** (string): Brief explanation of why the verdict was chosen
- **total_claims** (integer): Total number of claims extracted from the LLM response
- **supported_claims** (integer): Number of claims that are supported by the context
- **not_supported_claims** (integer): Number of claims that are not supported by the context
- **faithfullness_score** (float): Calculated as `supported_claims / total_claims`, ranges from 0.0 to 1.0
  - **1.0**: All claims are supported (perfectly faithful)
  - **0.0**: No claims are supported (complete hallucination)

#### Error Responses

- **500 Internal Server Error**: Failed to extract claims or verify them (e.g., LLM processing error)
- **401 Unauthorized**: Invalid or missing API key

### Example Use Case

When a CTO sees a dashboard showing that **15% of their bot's answers contain claims not found in their documentation**, the "fear" becomes a quantifiable risk. You aren't just selling "safety"; you are selling the **visibility** they currently lack.

### Future Enhancements

#### Citation Validation (Planned)

To implement the **Citation Validation** feature, the platform will intercept metadata from the Vector Database:

1. **Extract:** Look for Markdown-style citations in the LLM response (e.g., `[Source 1]`)
2. **Verify:** Cross-reference `Source 1` with the unique IDs returned by the retriever in that specific session
3. **Flag:** If the LLM cites a source that wasn't in the top-k retrieved chunks, mark it as a "Fabricated Citation"