"""Defines the prompter class for the Translator."""
class TranslatorPrompter:
    def __init__(self, language):
        self.language = language

    def get_translation_prompt(self, chunk, text_engine="text-davinci-003"):
        chunk_prompt = f"Translate [{chunk}] to [lang:{self.language}], Don't explain and only return translated text."
        #chunk_prompt = f"Translate [{chunk}] to [lang:{self.language}] and keep the original format, Don't explain and don't return original language text."
        #chunk_prompt = f"Please translate these to #lang:{self.language} and keep the originalformat.\n{chunk}"
        if "text" in text_engine:
            return {
                "prompt": chunk_prompt,
            }
        elif "gpt-3.5" in text_engine:
            return {
                "messages":[
                {"role": "system", "content": chunk_prompt}
                ]
            }
        return chunk_prompt
