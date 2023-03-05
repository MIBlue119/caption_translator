"""Defines the translator class."""
from pathlib import Path
from tqdm import tqdm
from caption_translator.utils import breakup_text_into_chunks,get_model_selection,generate_openai_completion,parse_text_response, count_tokens

class Translator:
    def __init__(self, config, prompter_class, loader,streamlit_progress_bar=None, streamlit_progress_message=None):
        """Initializes the translator class."""
        self.config = config
        self.text_engine = self.config.TEXT_ENGINE
        self.prompter = prompter_class(language=self.config.LANGUAGE)
        self.loader = loader
        self.loaded_lines = None
        self.chunks = None
        self.chunk_responses = []
        self.streamlit_progress_bar = streamlit_progress_bar
        self.streamlit_progress_message = streamlit_progress_message
    
    def load_data(self, file_path):
        """Loads data from file."""
        self.loaded_lines = self.loader.load_data(file_path)

    def translate(self, line:str):
        """Translate a line of text."""
        translation_prompt = self.prompter.get_translation_prompt(line, text_engine=self.text_engine)
        #print(translation_prompt)
        api_settings ={
                **get_model_selection(self.text_engine),
                **translation_prompt,
                "n": 1, 
                "max_tokens" :1024,               
                "temperature": self.config.TEXT_ENGINE_TEMPERATURE,
                "presence_penalty" : 2

        }
        response = generate_openai_completion(text_engine=self.text_engine, api_settings=api_settings)
        translated_text =  parse_text_response(response, text_engine=self.text_engine)                
        return translated_text

    def translate_lines_to_file(self,export_dir):
        """Translate lines to file."""
        if self.streamlit_progress_message is not None:
            self.streamlit_progress_message.markdown("Translating lines to file...")
        if self.streamlit_progress_bar is not None:
            self.streamlit_progress_bar.progress(0)            
        self.loader.translate_lines_to_file(self.config, self.loaded_lines, self.translate, export_dir=export_dir, streamlit_progress_bar=self.streamlit_progress_bar, streamlit_progress_message=self.streamlit_progress_message)

        if self.streamlit_progress_bar is not None:
            self.streamlit_progress_bar.progress(100) 
        if self.streamlit_progress_message is not None:
            self.streamlit_progress_message.markdown("Finished translating.")                       
    def make_translation(self, file_path, export_dir: str = None):
        """Makes the summary."""     
        # Extract file name
        # Load data to lines  
        self.load_data(file_path)
        # Translate lines to file.
        self.translate_lines_to_file(export_dir)