"""Pydantic models for request and response validation."""
from pydantic import BaseModel, Field
from typing import Optional, Dict


class SentimentRequest(BaseModel):
    """Request model for sentiment analysis."""
    text: str = Field(..., description="Text to analyze for sentiment", min_length=1)
    language: Optional[str] = Field(
        default="auto",
        description="Language code (e.g., 'fr', 'es', 'de') or 'auto' for auto-detection"
    )


class SentimentScores(BaseModel):
    """Sentiment scores for each class."""
    positive: float = Field(..., ge=0.0, le=1.0)
    negative: float = Field(..., ge=0.0, le=1.0)
    neutral: float = Field(..., ge=0.0, le=1.0)


class SentimentResponse(BaseModel):
    """Response model for sentiment analysis."""
    sentiment: str = Field(..., description="Predicted sentiment: positive, negative, or neutral")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score of the prediction")
    scores: SentimentScores = Field(..., description="Detailed scores for each sentiment class")
    original_text: str = Field(..., description="Original input text")
    translated_text: Optional[str] = Field(None, description="Translated text (if translation was needed)")
    detected_language: Optional[str] = Field(None, description="Detected language name (e.g., 'French', 'German', 'Spanish')")
    was_translated: bool = Field(..., description="Whether the text was translated")


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")

