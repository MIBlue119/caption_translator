"""Define the app's configuration.
"""


text_engine_choices = {
    "text-davinci-003": "text-davinci-003",
    "gpt-3.5-turbo": "gpt-3.5-turbo",
}  
class AppConfig:
    MAX_TOKENS = 1500
    OVERLAP_SIZE = int(MAX_TOKENS/5)
    TEXT_ENGINE = text_engine_choices["gpt-3.5-turbo"]
    TEXT_ENGINE_TEMPERATURE = 0.5
    LANGUAGE = "zh-tw"
    IS_TEST = True
    TEST_NUM = 20
    FINAL_SUMMARY_TOKENS = 2000
    def set_text_engine(self, text_engine):
        self.TEXT_ENGINE = text_engine_choices[text_engine]