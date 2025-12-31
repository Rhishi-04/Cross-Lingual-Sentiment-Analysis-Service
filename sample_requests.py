#!/usr/bin/env python3
"""
Sample Python requests for Cross-Lingual Sentiment Analysis Service
"""
import requests
import json

BASE_URL = "http://localhost:8000"


def print_response(title, response):
    """Pretty print API response."""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(json.dumps(response, indent=2, ensure_ascii=False))


def main():
    # Health check
    response = requests.get(f"{BASE_URL}/health")
    print_response("Health Check", response.json())

    # Get supported languages
    response = requests.get(f"{BASE_URL}/languages")
    languages = response.json()
    print_response("Supported Languages (showing first 10)", {
        "count": languages["count"],
        "sample": dict(list(languages["supported_languages"].items())[:10])
    })

    # Test cases
    test_cases = [
        {
            "title": "French - Positive Sentiment",
            "text": "Je suis très heureux aujourd'hui",
            "language": "auto"
        },
        {
            "title": "Spanish - Negative Sentiment",
            "text": "No me gusta este servicio, es terrible",
            "language": "auto"
        },
        {
            "title": "German - Neutral Sentiment",
            "text": "Das ist ein normaler Tag",
            "language": "auto"
        },
        {
            "title": "English - Positive Sentiment",
            "text": "I love this product, it's fantastic!",
            "language": "en"
        },
        {
            "title": "Italian - Positive Sentiment",
            "text": "Questo prodotto è meraviglioso!",
            "language": "it"
        },
        {
            "title": "Japanese - Positive Sentiment",
            "text": "この製品は素晴らしいです！",
            "language": "auto"
        }
    ]

    for test_case in test_cases:
        response = requests.post(
            f"{BASE_URL}/analyze",
            json={
                "text": test_case["text"],
                "language": test_case["language"]
            }
        )
        print_response(test_case["title"], response.json())


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API.")
        print("Make sure the service is running on http://localhost:8000")
    except Exception as e:
        print(f"Error: {e}")

