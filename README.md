# Caption Translator

- A caption translator package based on open ai api

## Usage

- install dependencies `pip install -r requirements.txt`
- Set your openai api key with `export OPENAI_API_KEYOPENAI="sxxxxxxxx"`
- Arguments

  - Necessary
    - `--file_path`: Set the transcript file path. Current only support `.vtt` and `.srt` format
  - Options
    - `--text_engine`: Set the open ai text engine. Default text engine is `gpt-3.5-turbo`
    - `--language`: Set the target translated language. Default language is `japanese`
      - support  other language `korean` / `german` / `traditional chinese` / `simplified chinese` / `french /`dutch
        - please see the LANGUAGES definition at [caption_translator/utils.py](./caption_translator/utils.py)
    - `--test`: Whether to test part of content
    - `--test_num`: How many number of contents do you want to summarize?
- Example

  ```
  $python -m caption_translator.app --file_path ./examples/EP108_humanosis_Podcast.vtt --test --language ja
  ```

# Resources

- https://blog.devgenius.io/creating-meeting-minutes-using-openai-gpt-3-api-f79e5fc15eb1
- https://blog.devgenius.io/counting-tokens-for-openai-gpt-3-api-59c8e0812eeb
- Open AI's open source tokenizer `tiktoken`: https://github.com/openai/tiktoken
  - Tokenization algorithm Byte Pair Encoding(1994 A New Algorithm for Data Compression) : https://zhuanlan.zhihu.com/p/424631681
    - data compression
  - Open AI cookbook's example to use tiktoken: https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynbhttps://huggingface.co/course/chapter6/5?fw=p
- Hugging face Tokenizer
  - BPE tokenization introduction: https://huggingface.co/course/chapter6/5?fw=pt
- Process long input
  - https://github.com/openai/openai-cookbook/blob/main/examples/Embedding_long_inputs.ipynb
  - https://github.com/openai/openai-cookbook/blob/main/examples/book_translation/translate_latex_book.ipynb
  - https://github.com/openai/openai-cookbook/blob/main/examples/fine-tuned_qa/olympics-1-collect-data.ipynb
  - oepnai web crawl qa: https://github.com/openai/openai-cookbook/blob/main/apps/web-crawl-q-and-a/web-qa.ipynb
  - [splitting-chunking-large-input-text-for-summarisation-greater-than-4096-tokens](https://community.openai.com/t/splitting-chunking-large-input-text-for-summarisation-greater-than-4096-tokens/18494/14)
    - recursive summary: https://github.dev/daveshap/RecursiveSummarizer
    - other tools: https://github.com/miso-belica/sumy
- Others
  - https://help.openai.com/en/articles/5072263-how-do-i-use-stop-sequences

## Prompt

- source: https://github.com/openai/openai-cookbook/blob/main/text_explanation_examples.md

```
Summarize the following text.

Text:
"""
Two independent experiments reported their results this morning at CERN, Europe's high-energy physics laboratory near Geneva in Switzerland. Both show convincing evidence of a new boson particle weighing around 125 gigaelectronvolts, which so far fits predictions of the Higgs previously made by theoretical physicists.

"As a layman I would say: 'I think we have it'. Would you agree?" Rolf-Dieter Heuer, CERN's director-general, asked the packed auditorium. The physicists assembled there burst into applause.
"""

Summary:
```
