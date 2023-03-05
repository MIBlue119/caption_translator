import tiktoken
import openai
from ratelimiter import RateLimiter
from retrying import retry

def text2token(text: str, encoding: str = "gpt2"):
    """Tokenize a text into a list of tokens.
    
    Ref:
        https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb
        https://github.com/openai/tiktoken
    """
    encoding = tiktoken.get_encoding(encoding)
    tokens = encoding.encode(text)

    return tokens 

def token2text(tokens: list, encoding: str = "gpt2"):
    """Decode a list of tokens into a text."""
    encoding = tiktoken.get_encoding(encoding)
    text = encoding.decode(tokens)

    return text           

def count_tokens(text: str, encoding: str = "gpt2"):
    """Count the number of tokens in a text.
    
    Ref: 
        https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb
        https://github.com/openai/tiktoken
    """
    num_tokens = len(text2token(text, encoding))

    return num_tokens

def breakup_text_into_chunks(text: str, max_tokens: int=2000, overlap_size:int=100, encoding: str = "gpt2"):
    """Break up a text into chunks of a given maximum number of tokens"""
    tokens = text2token(text, encoding)
    def breakup_tokens(tokens, max_tokens, overlap_size):
        """Break up a list of tokens into chunks of a given maximum number of tokens"""
        if len(tokens) <= max_tokens:
            # Return the tokens if they are less than the maximum number of tokens
            yield token2text(tokens)
        else:
            # Break up the tokens into chunks of the maximum number of tokens
            chunk = tokens[:max_tokens]
            # Return the chunk
            yield token2text(chunk)
            yield from breakup_tokens(tokens[max_tokens-overlap_size:], max_tokens, overlap_size)
    
    return list(breakup_tokens(tokens, max_tokens, overlap_size))

def parse_text_response(openai_text_response, text_engine):
    """According to the text engine, parse the response content.
    
    Different text engine support different response structures
    """
    if "text" in text_engine:
        return openai_text_response.choices[0].text.strip()
    elif "gpt-3.5" in text_engine:
        return openai_text_response['choices'][0]['message']['content']

def get_model_selection(text_engine):
    """Return the model selection according to the text engine."""
    model_seletection = {
        "gpt-3.5-turbo": {  "model": text_engine},
        "text-davinci-003": {  "engine": text_engine},
    }
    return model_seletection[text_engine]

def get_engine_method(text_engine):
    """Return the engine method according to the text engine."""
    method_selected = {
        "gpt-3.5-turbo": openai.ChatCompletion.create,
        "text-davinci-003": openai.Completion.create,
    }
    return method_selected[text_engine]

@retry(stop_max_attempt_number=10)
@RateLimiter(max_calls=20, period=60)
def generate_openai_completion(text_engine, api_settings):
    """Generate the completion using OpenAI API.
    
    Append the model selection and engine method according to the text engine.
    Add rate limiter and retry decorator to avoid the rate limit error.

    Ref: https://community.openai.com/t/continuous-gpt3-api-500-error-the-server-had-an-error-while-processing-your-request-sorry-about-that/42239/30?page=2
    Package: 
        https://github.com/RazerM/ratelimiter
        https://github.com/rholder/retrying
    """
    response=get_engine_method(text_engine)(**api_settings)
    return response

# Borrowed from : https://github.com/openai/whisper
LANGUAGES = {
    "en": "english",
    "zh-hans": "simplified chinese",
    "zh-hant": "traditional chinese",
    "de": "german",
    "es": "spanish",
    "ru": "russian",
    "ko": "korean",
    "fr": "french",
    "ja": "japanese",
    "pt": "portuguese",
    "tr": "turkish",
    "pl": "polish",
    "ca": "catalan",
    "nl": "dutch",
    "ar": "arabic",
    "sv": "swedish",
    "it": "italian",
    "id": "indonesian",
    "hi": "hindi",
    "fi": "finnish",
    "vi": "vietnamese",
    "he": "hebrew",
    "uk": "ukrainian",
    "el": "greek",
    "ms": "malay",
    "cs": "czech",
    "ro": "romanian",
    "da": "danish",
    "hu": "hungarian",
    "ta": "tamil",
    "no": "norwegian",
    "th": "thai",
    "ur": "urdu",
    "hr": "croatian",
    "bg": "bulgarian",
    "lt": "lithuanian",
    "la": "latin",
    "mi": "maori",
    "ml": "malayalam",
    "cy": "welsh",
    "sk": "slovak",
    "te": "telugu",
    "fa": "persian",
    "lv": "latvian",
    "bn": "bengali",
    "sr": "serbian",
    "az": "azerbaijani",
    "sl": "slovenian",
    "kn": "kannada",
    "et": "estonian",
    "mk": "macedonian",
    "br": "breton",
    "eu": "basque",
    "is": "icelandic",
    "hy": "armenian",
    "ne": "nepali",
    "mn": "mongolian",
    "bs": "bosnian",
    "kk": "kazakh",
    "sq": "albanian",
    "sw": "swahili",
    "gl": "galician",
    "mr": "marathi",
    "pa": "punjabi",
    "si": "sinhala",
    "km": "khmer",
    "sn": "shona",
    "yo": "yoruba",
    "so": "somali",
    "af": "afrikaans",
    "oc": "occitan",
    "ka": "georgian",
    "be": "belarusian",
    "tg": "tajik",
    "sd": "sindhi",
    "gu": "gujarati",
    "am": "amharic",
    "yi": "yiddish",
    "lo": "lao",
    "uz": "uzbek",
    "fo": "faroese",
    "ht": "haitian creole",
    "ps": "pashto",
    "tk": "turkmen",
    "nn": "nynorsk",
    "mt": "maltese",
    "sa": "sanskrit",
    "lb": "luxembourgish",
    "my": "myanmar",
    "bo": "tibetan",
    "tl": "tagalog",
    "mg": "malagasy",
    "as": "assamese",
    "tt": "tatar",
    "haw": "hawaiian",
    "ln": "lingala",
    "ha": "hausa",
    "ba": "bashkir",
    "jw": "javanese",
    "su": "sundanese",
}

# language code lookup by name, with a few language aliases
TO_LANGUAGE_CODE = {
    **{language: code for code, language in LANGUAGES.items()},
    "burmese": "my",
    "valencian": "ca",
    "flemish": "nl",
    "haitian": "ht",
    "letzeburgesch": "lb",
    "pushto": "ps",
    "panjabi": "pa",
    "moldavian": "ro",
    "moldovan": "ro",
    "sinhalese": "si",
    "castilian": "es",
}

if __name__ == "__main__":
    # Test the function
    text = "Hello, my name is John. I am a software engineer. I like to code."
    tokens = text2token(text)
    print(tokens)
    print(type(tokens))
    # decode the tokens
    print(tiktoken.get_encoding("gpt2").decode(tokens))
    num_tokens = count_tokens(text)
    print(num_tokens)

    