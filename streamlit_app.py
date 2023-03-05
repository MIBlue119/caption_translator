import os
from pathlib import Path
from io import StringIO

import streamlit as st
import openai

from caption_translator.fileloader import WebVttLoader, SrtLoader
from caption_translator.prompter import TranslatorPrompter
from caption_translator.config import AppConfig
from caption_translator.translator import Translator
from caption_translator.utils import LANGUAGES, TO_LANGUAGE_CODE
from caption_translator.config import text_engine_choices

# Initialize the config class
config = AppConfig()
config.TEXT_NUM= 20

st.title("Caption Translator")
st.write("Translate .vtt/.srt files to your desired language.")
transcript_name=st.file_uploader("Upload your .vtt or .srt files",type=['vtt','srt'])
col1,col2=st.columns(2)
openai_key=col1.text_input("OpenAI API Key",type="password")

text_engine_options = ["gpt-3.5-turbo","text-davinci-003"]
default_text_engine_option = "gpt-3.5-turbo"
text_engine_select=col2.selectbox("Text Engine",options=text_engine_options, index=text_engine_options.index(default_text_engine_option), help='Select the Open AI text engine for the summary')

languages_options = sorted(LANGUAGES.values())
default_lang_option = "japanese"
lang_select = col1.selectbox("Language",options=languages_options,index=languages_options.index(default_lang_option), help='Select the target language for the summary')

test=col2.checkbox(f"Just test process {config.TEST_NUM} lines",value=True,help='Select this option to only summarize 4 contents you can easily check')

make_button=st.button("Make Transcript Translation")

st.session_state["summary"]=None
# 如果tmp資料夾不存在，則建立
path="tmp"
if "translated_sucess" not in st.session_state:
    st.session_state["translated_sucess"] = False

if os.path.exists(path) == False:
    os.mkdir(path)

if transcript_name is not None:
    st.session_state["original_transcrpt_name"]=os.path.join(path,transcript_name.name)
    with open(st.session_state["original_transcrpt_name"],"wb") as f:
        f.write(transcript_name.getbuffer())

exported_lang = lang_select.replace("-", "_").replace(" ", "")   
if make_button:
    text_engine = text_engine_choices.get(text_engine_select, "gpt-3.5-turbo") 
    st.session_state["translated_file_name"]=st.session_state["original_transcrpt_name"].split(".")[0]+f"_translated.{exported_lang}."+st.session_state["original_transcrpt_name"].split(".")[1]
    if os.path.exists(st.session_state["translated_file_name"]) == False:
       
        streamlit_progress_bar = st.progress(0)
        streamlit_progress_message = st.markdown(" ")
        summarizing=st.markdown("Translating...")
        message = st.markdown(" ")

        file_path =st.session_state["original_transcrpt_name"]
        # Check the file is .vtt or .srt file
        file_extension = Path(file_path).suffix
        if file_extension not in [".vtt", ".srt"]:
            raise ValueError("File must be a .vtt /.srt file")
        # Initialize the loader class
        if file_extension == ".vtt":
            data_loader = WebVttLoader()
        elif file_extension == ".srt":
            data_loader = SrtLoader()

        config.set_text_engine(text_engine)
        config.LANGUAGE = lang_select
        if test:
            config.IS_TEST = True
        else:
            config.IS_TEST = False
        # Initialize the Summarizer class
        openai.api_key = openai_key
        summarizer = Translator(config,TranslatorPrompter, data_loader, streamlit_progress_bar=streamlit_progress_bar, streamlit_progress_message=streamlit_progress_message)
        summarizer.make_translation(file_path=st.session_state["original_transcrpt_name"], export_dir=path)
        streamlit_progress_bar.progress(100)
        streamlit_progress_message = st.markdown(" ")
        summarizing.markdown("Processing Done.")
        
    with open(st.session_state["translated_file_name"],"rb") as f:
        st.session_state["summary"]=f.read()
    st.session_state["translated_sucess"]=True

# delete the file
if st.session_state["translated_sucess"]==True:
    try:
        os.remove(st.session_state["translated_file_name"])
        os.remove(st.session_state["original_transcrpt_name"])
        # 删除path目录下所有文件
        for file in os.listdir(path):
            os.remove(os.path.join(path, file))
    except:
        pass 

if st.session_state["translated_sucess"]==True and st.session_state["summary"] is not None:
    download_button=st.download_button(
        label="Download",
        data=st.session_state["summary"],
        file_name=transcript_name.name.split(".")[0]+f"_translated.{exported_lang}."+transcript_name.name.split(".")[1],
    ) 
        
