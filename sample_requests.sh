#!/bin/bash
# Sample requests for Cross-Lingual Sentiment Analysis Service

BASE_URL="http://localhost:8000"

echo "=== Health Check ==="
curl -X GET "${BASE_URL}/health"
echo -e "\n\n"

echo "=== Get Supported Languages ==="
curl -X GET "${BASE_URL}/languages"
echo -e "\n\n"

echo "=== Analyze Sentiment - French (Positive) ==="
curl -X POST "${BASE_URL}/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Je suis très heureux aujourd'\''hui",
    "language": "auto"
  }'
echo -e "\n\n"

echo "=== Analyze Sentiment - Spanish (Negative) ==="
curl -X POST "${BASE_URL}/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "No me gusta este servicio, es terrible",
    "language": "auto"
  }'
echo -e "\n\n"

echo "=== Analyze Sentiment - German (Neutral) ==="
curl -X POST "${BASE_URL}/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Das ist ein normaler Tag",
    "language": "auto"
  }'
echo -e "\n\n"

echo "=== Analyze Sentiment - English (Positive) ==="
curl -X POST "${BASE_URL}/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "I love this product, it'\''s fantastic!",
    "language": "en"
  }'
echo -e "\n\n"

echo "=== Analyze Sentiment - Italian (Positive) ==="
curl -X POST "${BASE_URL}/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Questo prodotto è meraviglioso!",
    "language": "it"
  }'
echo -e "\n"

