"""Translation service wrapper for Google Translate API."""
import logging
import re
from typing import Optional, Tuple
from deep_translator import GoogleTranslator
from app.config import settings

logger = logging.getLogger(__name__)


class TranslationService:
    """Service for translating text to English."""
    
    def __init__(self):
        """Initialize the translation service."""
        self.translator = None  # Will be initialized lazily
        # Common language codes supported by Google Translate
        self.supported_languages = {
            'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German',
            'it': 'Italian', 'pt': 'Portuguese', 'ru': 'Russian', 'ja': 'Japanese',
            'ko': 'Korean', 'zh': 'Chinese', 'ar': 'Arabic', 'hi': 'Hindi',
            'nl': 'Dutch', 'pl': 'Polish', 'tr': 'Turkish', 'sv': 'Swedish',
            'da': 'Danish', 'fi': 'Finnish', 'no': 'Norwegian', 'cs': 'Czech',
            'hu': 'Hungarian', 'ro': 'Romanian', 'el': 'Greek', 'th': 'Thai',
            'vi': 'Vietnamese', 'id': 'Indonesian', 'he': 'Hebrew', 'uk': 'Ukrainian'
        }
        # Common non-English words/phrases to help detect if text is likely English
        self.non_english_indicators = {
            'fr': ['je', 'tu', 'il', 'elle', 'nous', 'vous', 'être', 'avoir', 'très', 'aujourd\'hui'],
            'es': ['yo', 'tú', 'él', 'ella', 'nosotros', 'vosotros', 'ser', 'estar', 'muy', 'hoy'],
            'de': ['ich', 'du', 'er', 'sie', 'wir', 'ihr', 'sein', 'haben', 'sehr', 'heute'],
            'it': ['io', 'tu', 'lui', 'lei', 'noi', 'voi', 'essere', 'avere', 'molto', 'oggi'],
            'pt': ['eu', 'tu', 'ele', 'ela', 'nós', 'vós', 'ser', 'estar', 'muito', 'hoje'],
        }
    
    def _get_translator(self, source: str = 'auto', target: str = 'en'):
        """Get or create translator instance."""
        try:
            return GoogleTranslator(source=source, target=target)
        except Exception as e:
            logger.error(f"Failed to create translator: {e}")
            raise
    
    def _simple_language_detection(self, text: str) -> str:
        """
        Simple heuristic-based language detection.
        
        Args:
            text: Text to analyze
            
        Returns:
            Detected language code or 'en' if uncertain
        """
        text_lower = text.lower()
        word_count = {}
        
        # Check for common words in different languages
        for lang, words in self.non_english_indicators.items():
            count = sum(1 for word in words if word in text_lower)
            if count > 0:
                word_count[lang] = count
        
        if word_count:
            # Return the language with the most matches
            detected = max(word_count.items(), key=lambda x: x[1])[0]
            logger.debug(f"Detected language via heuristics: {detected}")
            return detected
        
        # Check for non-ASCII characters (likely not English)
        if re.search(r'[^\x00-\x7F]', text):
            # Could be various languages, but we'll try to detect
            # For now, return 'auto' to let translator handle it
            return "auto"
        
        # Default to English if no indicators found
        return "en"
    
    def detect_language(self, text: str) -> Tuple[str, float]:
        """
        Detect the language of the given text.
        
        Args:
            text: Text to detect language for
            
        Returns:
            Tuple of (language_code, confidence)
        """
        try:
            # Use simple heuristic detection
            detected = self._simple_language_detection(text)
            confidence = 0.7 if detected != "auto" else 0.5
            return detected, confidence
        except Exception as e:
            logger.warning(f"Language detection failed: {e}. Assuming 'en'")
            return "en", 0.0
    
    def is_english(self, language_code: str) -> bool:
        """
        Check if the language code represents English.
        
        Args:
            language_code: Language code to check
            
        Returns:
            True if the language is English
        """
        # Don't treat 'auto' as English
        return language_code.lower() in ['en', 'en-us', 'en-gb', 'en-ca', 'en-au']
    
    def translate_to_english(self, text: str, source_language: Optional[str] = None, return_language_name: bool = True) -> Tuple[str, str, bool]:
        """
        Translate text to English.
        
        Args:
            text: Text to translate
            source_language: Source language code (optional, will auto-detect if not provided)
            return_language_name: If True, returns full language name instead of code
            
        Returns:
            Tuple of (translated_text, detected_language, was_translated)
            where detected_language is either code or full name based on return_language_name
        """
        try:
            original_text = text
            
            # If source language is explicitly provided and it's English, return as-is
            if source_language and source_language != "auto" and self.is_english(source_language):
                return text, "English" if return_language_name else "en", False
            
            # Detect language if not provided or if "auto"
            if not source_language or source_language == "auto":
                detected_lang, _ = self.detect_language(text)
                source_language = detected_lang
            
            # If detected as English, return as-is
            if self.is_english(source_language):
                return text, "English" if return_language_name else "en", False
            
            # Translate to English
            translator = self._get_translator(source=source_language, target='en')
            translated_text = translator.translate(text)
            
            # Check if translation actually changed the text
            # Normalize both texts for comparison
            original_normalized = original_text.lower().strip()
            translated_normalized = translated_text.lower().strip()
            
            was_translated = (
                original_normalized != translated_normalized and
                len(translated_text) > 0
            )
            
            # Convert language code to name if requested
            language_output = self.get_language_name(source_language) if return_language_name else source_language
            
            if was_translated:
                logger.info(f"Translated from {source_language} to English: '{original_text[:50]}...' -> '{translated_text[:50]}...'")
            else:
                logger.info(f"Text appears to be already in English or translation unchanged")
                language_output = "English" if return_language_name else "en"
            
            return translated_text, language_output, was_translated
            
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            # Fallback: return original text and assume English
            logger.warning("Falling back to original text (assuming English)")
            return text, "English" if return_language_name else "en", False
    
    def get_language_name(self, language_code: str) -> str:
        """
        Convert language code to full language name.
        
        Args:
            language_code: Language code (e.g., 'fr', 'de', 'es')
            
        Returns:
            Full language name (e.g., 'French', 'German', 'Spanish')
        """
        if not language_code:
            return "Unknown"
        
        code_lower = language_code.lower()
        # Handle common variations
        if code_lower in ['en', 'en-us', 'en-gb', 'en-ca', 'en-au']:
            return "English"
        
        return self.supported_languages.get(code_lower, language_code.title())
    
    def get_supported_languages(self) -> dict:
        """
        Get list of supported languages.
        
        Returns:
            Dictionary of language codes and names
        """
        return self.supported_languages


# Global translation service instance
translation_service = TranslationService()

