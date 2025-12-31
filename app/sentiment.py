"""Sentiment analysis module using Hugging Face Transformers."""
import logging
from typing import Dict
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline
import torch

from app.config import settings

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """Service for analyzing sentiment of text."""
    
    def __init__(self, model_name: str = None):
        """
        Initialize the sentiment analyzer.
        
        Args:
            model_name: Name of the Hugging Face model to use
        """
        self.model_name = model_name or settings.sentiment_model_name
        self.tokenizer = None
        self.model = None
        self.pipeline = None
        self._load_model()
    
    def _load_model(self):
        """Load the sentiment analysis model and tokenizer."""
        try:
            logger.info(f"Loading sentiment model: {self.model_name}")
            
            # Use pipeline for easier inference
            self.pipeline = pipeline(
                "sentiment-analysis",
                model=self.model_name,
                tokenizer=self.model_name,
                device=0 if torch.cuda.is_available() else -1
            )
            
            logger.info("Sentiment model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load sentiment model: {e}")
            raise
    
    def analyze(self, text: str) -> Dict[str, any]:
        """
        Analyze sentiment of the given text.
        
        Args:
            text: Text to analyze (should be in English)
            
        Returns:
            Dictionary with sentiment analysis results
        """
        try:
            # Run sentiment analysis
            result = self.pipeline(text)[0]
            
            # Extract label and score
            label = result['label'].upper()
            score = result['score']
            
            # Map labels to standard format (positive/negative/neutral)
            # The model might use different labels, so we normalize them
            label_mapping = {
                'POSITIVE': 'positive',
                'NEGATIVE': 'negative',
                'NEUTRAL': 'neutral',
                'LABEL_0': 'negative',  # Some models use label indices
                'LABEL_1': 'neutral',
                'LABEL_2': 'positive',
            }
            
            normalized_label = label_mapping.get(label, label.lower())
            
            # For 3-class models, we need to get all scores
            # Some models return only the top class, so we'll handle both cases
            scores = self._get_all_scores(text, normalized_label, score)
            
            return {
                'sentiment': normalized_label,
                'confidence': score,
                'scores': scores
            }
            
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            raise
    
    def _get_all_scores(self, text: str, predicted_label: str, predicted_score: float) -> Dict[str, float]:
        """
        Get scores for all sentiment classes.
        
        Args:
            text: Input text
            predicted_label: Predicted sentiment label
            predicted_score: Confidence score for predicted label
            
        Returns:
            Dictionary with scores for positive, negative, and neutral
        """
        try:
            # Try to get all class scores by running inference with return_all_scores
            results = self.pipeline(text, return_all_scores=True)[0]
            
            # Initialize scores dictionary
            scores = {'positive': 0.0, 'negative': 0.0, 'neutral': 0.0}
            
            # Map results to our standard format
            label_mapping = {
                'POSITIVE': 'positive',
                'NEGATIVE': 'negative',
                'NEUTRAL': 'neutral',
                'LABEL_0': 'negative',
                'LABEL_1': 'neutral',
                'LABEL_2': 'positive',
            }
            
            for item in results:
                label = item['label'].upper()
                score = item['score']
                normalized = label_mapping.get(label, label.lower())
                
                if normalized in scores:
                    scores[normalized] = score
            
            # Normalize scores to sum to 1.0
            total = sum(scores.values())
            if total > 0:
                scores = {k: v / total for k, v in scores.items()}
            
            return scores
            
        except Exception as e:
            logger.warning(f"Could not get all scores, using predicted score: {e}")
            # Fallback: distribute scores based on predicted label
            scores = {'positive': 0.0, 'negative': 0.0, 'neutral': 0.0}
            scores[predicted_label] = predicted_score
            
            # Distribute remaining probability equally among other classes
            remaining = (1.0 - predicted_score) / 2
            for key in scores:
                if key != predicted_label:
                    scores[key] = remaining
            
            return scores


# Global sentiment analyzer instance (lazy loading)
_sentiment_analyzer = None


def get_sentiment_analyzer() -> SentimentAnalyzer:
    """Get or create the global sentiment analyzer instance."""
    global _sentiment_analyzer
    if _sentiment_analyzer is None:
        _sentiment_analyzer = SentimentAnalyzer()
    return _sentiment_analyzer

