from pathlib import Path
import time
from tqdm import tqdm

class WebVttLoader:
    def __init__(self)->None:
        self.file_path = None
        pass
    
    def load_data(self, file_path: str):
        """Load data from a WebVTT file.
        
        1.Skip the first line which contains only the WEBVTT header.
        2.Extract text from each line.

        Returns:
            list: List of strings, each string is a line of text.
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
        export_path = Path(export_dir) / f"{file_name}_translated.{exported_lang}.vtt"
        if streamlit_progress_message is not None:
            streamlit_progress_message.text("Start to translate line by line...")
        progress_bar_max = config.TEST_NUM if config.IS_TEST else len(lines)
        progress_bar = tqdm(total=progress_bar_max)
        index = 0
        with open(export_path, "w", encoding="utf-8") as f:
            # Skip the first line which contains the header
            f.write(lines[0])
            lines = lines[1:]
            progress_bar.update(1)
            for i, line in enumerate(lines):
                progress_bar.update(1)
                clean_line_break = line.replace("\n", "")
                if "-->" not in line and len(clean_line_break)>0:
                    #print([clean_line_break])
                    translated_line = translate_func(line)
                    time.sleep(0.1)
                    translated_line = translated_line.replace("\n", "")
                    print(translated_line)
                    f.write(translated_line+"\n")
                else:
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
    def translate_lines_to_file_block_mode(self, lines, translate_function, export_dir: str = None): 

        file_name = Path(self.file_path).stem
        if export_dir is None:
            export_dir = Path(self.file_path).parent
        export_path = Path(export_dir) / f"{file_name}_translated.vtt"

        with open(export_path, "w", encoding="utf-8") as f:
            # Skip the first line which contains the header
            f.write(lines[0])
            lines = lines[1:]
            # Break up the lines into blocks
            blocks = self.breakup_lines_to_blocks(lines, block_size=10)
            for block in blocks:
                translated_block = translate_function(block)
                print(translated_block)
                f.write(translated_block)
                time.sleep(0.1)
                   
    def breakup_lines_to_blocks(self, lines, block_size: int = 10):
        """Split lines into chunks.
        
        Each chunk contains a list of lines.
        Each chunk is a list of lines.
        """
        def breakup_lines(lines,block_size):
            if len(lines) <= block_size:
                # Return the lines if they are less than the block size
                yield "".join(lines)
            else:
                # Break up the lines into blocks
                block = lines[:block_size]
                # Return the block
                yield "".join(block)
                # Recursively call the function to break up the remaining lines
                yield from breakup_lines(lines[block_size:], block_size)
        return list(breakup_lines(lines, block_size))
