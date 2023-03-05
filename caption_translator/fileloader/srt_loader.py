from pathlib import Path
import time
from tqdm import tqdm

class SrtLoader:
    def __init__(self)->None:
        self.file_path = None
        pass
    
    def load_data(self, file_path: str):
        """Load data from a Srt file.
        
        Extract text from each line.

        Returns:
            str: The text from the Srt file.
        """
        # Load data from file
        with open(file_path, 'r', encoding="utf-8") as file:
            lines = file.readlines()
        self.file_path = file_path
        return lines
           
    def translate_lines_to_file(self,
                                config,  
                                lines, 
                                translate_func, 
                                export_dir: str = None,
                                streamlit_progress_bar=None,
                                streamlit_progress_message=None
                                ): 
        file_name = Path(self.file_path).stem
        if export_dir is None:
            export_dir = Path(self.file_path).parent
        # remove space and replace "-" with "_"
        exported_lang = config.LANGUAGE.replace("-", "_").replace(" ", "")            
        export_path = Path(export_dir) / f"{file_name}_translated.{exported_lang}.srt"
        last_line= ""
        if streamlit_progress_message is not None:
            streamlit_progress_message.text("Start to translate line by line...")
        progress_bar_max = config.TEST_NUM if config.IS_TEST else len(lines)
        progress_bar = tqdm(total=progress_bar_max)
        index = 0

        with open(export_path, "w", encoding="utf-8") as f:
            for i, line in enumerate(lines):
                progress_bar.update(1)
                clean_line_break = line.replace("\n", "")
                if "-->" in last_line and len(clean_line_break)>0:
                    translated_line = translate_func(line)
                    translated_line = translated_line.replace("\n", "")
                    print(translated_line)
                    f.write(translated_line+"\n")
                else:
                    last_line = line
                    print(line)
                    f.write(line)
                index += 1
                if streamlit_progress_bar is not None:
                    if index/progress_bar_max > 1:
                        streamlit_progress_bar.progress(1)
                    else:
                        streamlit_progress_bar.progress(index/progress_bar_max)                    
                if config.IS_TEST and i == config.TEST_NUM:
                    break                    
        progress_bar.close()
if __name__ == "__main__":
    file_path = "/Users/weirenlan/Desktop/self_practice/caption_translator/examples/EP108_humannosis_Podcast.srt"
    loader = SrtLoader()
    text = loader.load_data(file_path)
    print(text)

