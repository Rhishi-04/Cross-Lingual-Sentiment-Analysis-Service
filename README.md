# Cross-Lingual Sentiment Analysis Service

A REST API service that performs sentiment analysis on text in multiple languages. The service automatically detects the language, translates non-English text to English, and then applies a pre-trained sentiment analysis model to determine if the sentiment is positive, negative, or neutral.

## Features

- 🌍 **Multi-language Support**: Automatically detects and translates text from 100+ languages
- 🎯 **3-Class Sentiment Analysis**: Classifies text as positive, negative, or neutral
- 🚀 **FastAPI**: Modern, fast, async REST API framework
- 🐳 **Dockerized**: Easy deployment with Docker
- 📊 **Detailed Scores**: Returns confidence scores for all sentiment classes
- 🔍 **Language Detection**: Automatic language detection with full language name reporting
- 📝 **Human-Readable Output**: Returns full language names (e.g., "French", "German") instead of codes

## Technologies

- **Python 3.11+**
- **FastAPI**: Modern web framework for building APIs
- **Hugging Face Transformers**: Pre-trained sentiment analysis models
- **Google Translate API**: Translation service (via deep-translator library)
- **Docker**: Containerization

## Project Structure

```
cross-lingual-sentiment-service/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── models.py            # Pydantic models
│   ├── translator.py        # Translation service
│   ├── sentiment.py         # Sentiment analysis
│   └── config.py            # Configuration
├── requirements.txt
├── Dockerfile
├── .env.example
├── README.md
└── ARCHITECTURE.md          # System architecture diagrams
```

## System Architecture

For detailed architecture diagrams, system flow, and component documentation, see [ARCHITECTURE.md](ARCHITECTURE.md).

### Quick Overview

The system follows a layered architecture:

1. **API Layer** (FastAPI): Handles HTTP requests, validation, and response formatting
2. **Translation Layer**: Detects language and translates non-English text to English
3. **Sentiment Analysis Layer**: Analyzes sentiment using a pre-trained RoBERTa model
4. **External Services**: Google Translate API and Hugging Face Hub

**Request Flow:**
```
Client → FastAPI → Translation Service → Sentiment Analyzer → Response
```

## Setup and Installation

### Prerequisites

- Python 3.11 or higher
- Docker (optional, for containerized deployment)
- Internet connection (for downloading models and translation)

### Local Development Setup

1. **Clone or navigate to the project directory**

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create environment file (optional)**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` if you need to customize settings.

5. **Run the service**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   Or use Python directly:
   ```bash
   python -m app.main
   ```

6. **Access the API**
   - API: http://localhost:8000
   - Interactive Docs (Swagger): http://localhost:8000/docs
   - Alternative Docs (ReDoc): http://localhost:8000/redoc
   - Health Check: http://localhost:8000/health

### Docker Deployment

1. **Build the Docker image**
   ```bash
   docker build -t cross-lingual-sentiment:latest .
   ```

2. **Run the container**
   ```bash
   docker run -d -p 8000:8000 --name sentiment-service cross-lingual-sentiment:latest
   ```

3. **Check if it's running**
   ```bash
   docker ps
   curl http://localhost:8000/health
   ```

4. **View logs**
   ```bash
   docker logs sentiment-service
   ```

5. **Stop the container**
   ```bash
   docker stop sentiment-service
   docker rm sentiment-service
   ```

## API Usage

### Endpoints

#### 1. Analyze Sentiment
**POST** `/analyze`

Analyzes the sentiment of text in any supported language.

**Request Body:**
```json
{
  "text": "Je suis très heureux aujourd'hui",
  "language": "auto"
}
```

**Parameters:**
- `text` (required): The text to analyze
- `language` (optional): Language code (e.g., "fr", "es", "de") or "auto" for auto-detection. Defaults to "auto". Note: The response will return the full language name (e.g., "French", "Spanish", "German").

**Response:**
```json
{
  "sentiment": "positive",
  "confidence": 0.95,
  "scores": {
    "positive": 0.95,
    "negative": 0.03,
    "neutral": 0.02
  },
  "original_text": "Je suis très heureux aujourd'hui",
  "translated_text": "I am very happy today",
  "detected_language": "French",
  "was_translated": true
}
```

**Response Fields:**
- `sentiment`: The predicted sentiment ("positive", "negative", or "neutral")
- `confidence`: Confidence score of the prediction (0.0 to 1.0)
- `scores`: Detailed scores for each sentiment class
- `original_text`: The original input text
- `translated_text`: The translated text (null if no translation was needed)
- `detected_language`: The detected language name (e.g., "French", "German", "Spanish", "English")
- `was_translated`: Boolean indicating whether translation occurred

#### 2. Health Check
**GET** `/health`

Returns the health status of the service.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

#### 3. Get Supported Languages
**GET** `/languages`

Returns a list of all supported languages for translation.

**Response:**
```json
{
  "supported_languages": {
    "en": "English",
    "fr": "French",
    "es": "Spanish",
    ...
  },
  "count": 107
}
```

## Sample Requests

### Using cURL

**Analyze sentiment (auto-detect language):**
```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Je suis très heureux aujourd'hui",
    "language": "auto"
  }'
```

**Analyze sentiment (specify language):**
```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Estoy muy feliz hoy",
    "language": "es"
  }'
```

**Analyze English text:**
```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "I am very happy today!",
    "language": "en"
  }'
```

**Health check:**
```bash
curl http://localhost:8000/health
```

**Get supported languages:**
```bash
curl http://localhost:8000/languages
```

### Using Python

```python
import requests

# Analyze sentiment
response = requests.post(
    "http://localhost:8000/analyze",
    json={
        "text": "Je suis très heureux aujourd'hui",
        "language": "auto"
    }
)

result = response.json()
print(f"Sentiment: {result['sentiment']}")
print(f"Confidence: {result['confidence']}")
print(f"Scores: {result['scores']}")
print(f"Detected Language: {result['detected_language']}")
print(f"Translated: {result['was_translated']}")
if result['translated_text']:
    print(f"Translation: {result['translated_text']}")
```

### Using JavaScript/Node.js

```javascript
const response = await fetch('http://localhost:8000/analyze', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    text: 'Je suis très heureux aujourd\'hui',
    language: 'auto'
  })
});

const result = await response.json();
console.log('Sentiment:', result.sentiment);
console.log('Confidence:', result.confidence);
console.log('Scores:', result.scores);
console.log('Detected Language:', result.detected_language);
console.log('Translated:', result.was_translated);
if (result.translated_text) {
  console.log('Translation:', result.translated_text);
}
```

## Example Responses

### Positive Sentiment (French)
**Request:**
```json
{
  "text": "J'adore ce produit, il est fantastique!",
  "language": "auto"
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
  "original_text": "J'adore ce produit, il est fantastique!",
  "translated_text": "I love this product, it's fantastic!",
  "detected_language": "French",
  "was_translated": true
}
```

### Negative Sentiment (Spanish)
**Request:**
```json
{
  "text": "No me gusta este servicio, es terrible",
  "language": "auto"
}
```

**Response:**
```json
{
  "sentiment": "negative",
  "confidence": 0.96,
  "scores": {
    "positive": 0.02,
    "negative": 0.96,
    "neutral": 0.02
  },
  "original_text": "No me gusta este servicio, es terrible",
  "translated_text": "I don't like this service, it's terrible",
  "detected_language": "Spanish",
  "was_translated": true
}
```

### Neutral Sentiment (German)
**Request:**
```json
{
  "text": "Das ist ein normaler Tag",
  "language": "auto"
}
```

**Response:**
```json
{
  "sentiment": "neutral",
  "confidence": 0.87,
  "scores": {
    "positive": 0.08,
    "negative": 0.05,
    "neutral": 0.87
  },
  "original_text": "Das ist ein normaler Tag",
  "translated_text": "This is a normal day",
  "detected_language": "German",
  "was_translated": true
}
```

## Configuration

The service can be configured using environment variables. Create a `.env` file or set environment variables:

- `API_HOST`: Host to bind to (default: `0.0.0.0`)
- `API_PORT`: Port to bind to (default: `8000`)
- `SENTIMENT_MODEL_NAME`: Hugging Face model name (default: `cardiffnlp/twitter-roberta-base-sentiment-latest`)
- `LOG_LEVEL`: Logging level (default: `INFO`)
- `GOOGLE_TRANSLATE_API_KEY`: Optional API key for Google Translate (not required for basic usage)

## Model Information

The service uses the `cardiffnlp/twitter-roberta-base-sentiment-latest` model from Hugging Face, which is a RoBERTa-based model fine-tuned for 3-class sentiment analysis (positive, negative, neutral). The model is automatically downloaded on first use.

## Limitations

- Translation is done via the `deep-translator` library, which uses Google Translate's free API. There may be rate limits.
- The sentiment model is optimized for English text, which is why translation is performed first.
- Model loading takes time on first startup (models are cached after first download).
- Language detection uses heuristics and may not be 100% accurate for all languages; the service will still translate correctly even if detection is imperfect.

## Troubleshooting

### Model Download Issues
If the model fails to download, ensure you have internet connectivity. The model will be cached locally after the first download.

### Translation Errors
If translation fails, the service will fall back to analyzing the original text (assuming it's English). Check your internet connection and Google Translate availability.

### Port Already in Use
If port 8000 is already in use, change it in the `.env` file or use:
```bash
uvicorn app.main:app --port 8080
```

## License

This project is provided as-is for educational and development purposes.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

