from deep_translator import GoogleTranslator


class TranslationService:
    """Service for translating text between languages."""
    
    @staticmethod
    def translate_japanese_to_english(text: str) -> str:
        """Translate Japanese text to English."""
        if not text:
            return ""
        
        try:
            translator = GoogleTranslator(source='ja', target='en')
            return translator.translate(text)
        except Exception as e:
            print(f"Translation error: {e}")
            return f"[Translation error: {str(e)}]"


translator = TranslationService()
