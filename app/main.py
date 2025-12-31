"""FastAPI main application for Cross-Lingual Sentiment Analysis Service."""
import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.config import settings
from app.models import SentimentRequest, SentimentResponse, HealthResponse, SentimentScores
from app.translator import translation_service
from app.sentiment import get_sentiment_analyzer

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events."""
    # Startup
    logger.info("Starting Cross-Lingual Sentiment Analysis Service...")
    logger.info("Loading sentiment model (this may take a moment)...")
    
    try:
        # Pre-load the sentiment analyzer
        get_sentiment_analyzer()
        logger.info("Service started successfully!")
    except Exception as e:
        logger.error(f"Failed to start service: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down service...")


# Create FastAPI application
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="A REST API service for cross-lingual sentiment analysis using translation and ML models",
    lifespan=lifespan
)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "service": settings.api_title,
        "version": settings.api_version,
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version=settings.api_version
    )


@app.post("/analyze", response_model=SentimentResponse, tags=["Analysis"])
async def analyze_sentiment(request: SentimentRequest):
    """
    Analyze sentiment of text in any language.
    
    The service will:
    1. Detect the language of the input text (if not specified)
    2. Translate to English if needed
    3. Analyze sentiment using a pre-trained model
    4. Return sentiment scores and metadata
    """
    try:
        # Get the sentiment analyzer
        analyzer = get_sentiment_analyzer()
        
        # Step 1: Translate to English if needed
        source_lang = request.language if request.language != "auto" else None
        translated_text, detected_language, was_translated = translation_service.translate_to_english(
            request.text,
            source_language=source_lang,
            return_language_name=True  # Return full language names instead of codes
        )
        
        # Step 2: Analyze sentiment
        sentiment_result = analyzer.analyze(translated_text)
        
        # Step 3: Build response
        response = SentimentResponse(
            sentiment=sentiment_result['sentiment'],
            confidence=sentiment_result['confidence'],
            scores=SentimentScores(**sentiment_result['scores']),
            original_text=request.text,
            translated_text=translated_text if was_translated else None,
            detected_language=detected_language,
            was_translated=was_translated
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error analyzing sentiment: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze sentiment: {str(e)}"
        )


@app.get("/languages", tags=["Info"])
async def get_supported_languages():
    """Get list of supported languages for translation."""
    try:
        languages = translation_service.get_supported_languages()
        return {
            "supported_languages": languages,
            "count": len(languages)
        }
    except Exception as e:
        logger.error(f"Error getting supported languages: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get supported languages: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )

