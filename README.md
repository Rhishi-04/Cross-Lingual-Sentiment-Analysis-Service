# Cross-Lingual Sentiment Analysis Service

A REST API service that performs sentiment analysis on text in multiple languages. The service automatically detects the language, translates non-English text to English, and then applies a pre-trained sentiment analysis model to determine if the sentiment is positive, negative, or neutral.

## Features

-  **Multi-language Support**: Automatically detects and translates text from 100+ languages
-  **3-Class Sentiment Analysis**: Classifies text as positive, negative, or neutral
-  **FastAPI**: Modern, fast, async REST API framework
-  **Dockerized**: Easy deployment with Docker
-  **Detailed Scores**: Returns confidence scores for all sentiment classes
-  **Human-Readable Output**: Returns full language names (e.g., "French", "German") instead of codes

## Technologies

- Python 3.11+, FastAPI, Hugging Face Transformers, deep-translator, Docker

## Quick Start

### Local Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the service
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker Setup

```bash
# Build and run
docker build -t sentiment-service .
docker run -d -p 8000:8000 --name sentiment-service sentiment-service
```

**Access:** http://localhost:8000/docs (Interactive API documentation)

## API Usage

### Analyze Sentiment

**POST** `/analyze`

**Only `text` is required** - language is automatically detected!

```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "Je suis très heureux"}'
```

**Request (minimal - only text needed):**
```json
{
  "text": "Je suis très heureux aujourd'hui"
}
```

**Optional:** You can specify language if needed:
```json
{
  "text": "Je suis très heureux",
  "language": "fr"
}
```

**Response:**
```json
{
  "sentiment": "positive",
  "confidence": 0.98,
  "scores": {
    "positive": 0.98,
    "negative": 0.01,
    "neutral": 0.01
  },
  "original_text": "Je suis très heureux aujourd'hui",
  "translated_text": "I am very happy today",
  "detected_language": "French",
  "was_translated": true
}
```

### Other Endpoints

- **GET** `/health - Health check
- **GET** `/languages - List supported languages

## Example Usage

### Python

```python
import requests

# Only text is needed - language is auto-detected
response = requests.post(
    "http://localhost:8000/analyze",
    json={"text": "Je suis très heureux"}
)

result = response.json()
print(f"Sentiment: {result['sentiment']}")
print(f"Language: {result['detected_language']}")
```

### JavaScript

```javascript
// Only text is needed - language is auto-detected
const response = await fetch('http://localhost:8000/analyze', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    text: 'Je suis très heureux'
  })
});

const result = await response.json();
console.log('Sentiment:', result.sentiment);
console.log('Language:', result.detected_language);
```

## Configuration

Create a `.env` file (see `ENV_EXAMPLE.txt`):

- `API_HOST`: Host to bind to (default: `0.0.0.0`)
- `API_PORT`: Port to bind to (default: `8000`)
- `SENTIMENT_MODEL_NAME`: Hugging Face model (default: `cardiffnlp/twitter-roberta-base-sentiment-latest`)
- `LOG_LEVEL`: Logging level (default: `INFO`)

## Architecture

For detailed architecture diagrams and system flow, see [ARCHITECTURE.md](ARCHITECTURE.md).

**Request Flow:** `Client → FastAPI → Translation Service → Sentiment Analyzer → Response`

## Project Structure

```
├── app/
│   ├── main.py          # FastAPI application
│   ├── models.py        # Pydantic models
│   ├── translator.py    # Translation service
│   ├── sentiment.py     # Sentiment analysis
│   └── config.py        # Configuration
├── requirements.txt
├── Dockerfile
└── ARCHITECTURE.md      # System architecture
```

## Limitations

- Translation uses Google Translate's free API (may have rate limits)
- Model is optimized for English text (translation performed first)
- Model loading takes time on first startup (cached after download)

## License

MIT License
