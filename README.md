# LLMs

**Help desk** allows you to create a Question Answering bot with a streamlit UI using your company Confluence data.

<p align="center">
  <img src="./docs/help_desk.gif" alt="animated" />
</p>

## How to use

- Create a virtual environnement:
  - `python3.10 -m venv .venv`
  - `source .venv/bin/activate`
  - `pip install -r requirements.txt`

- Copy the env.template and fill your environment variables
  - `cp .env.template .env`

- Check the `config.py` and `env.template` file.
- To collect data from Confluence you will have to:
  - Create your own Conluence space with page informations
  - Create and feed your API key [here]('https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/')
  - Update the `.env` file
- To run the streamlit app run:

    ```bash
    python3 -m streamlit run main.py
    ```

## How it works ?

```
.
├── docs/                       # Documentation files
├── src/                        # The main directory for computer demo
    ├── __init__.py
    ├── load_db.py              # Load data from confluence and creates smart chunks
    ├── help_desk.py            # Instantiates the LLMs, retriever and chain
    └── main.py                 # Run the Chatbot in streamlit where you can ask your own questions
├── config.py
├── .env.template               # Environment variables to feed
├── .gitignore
├── LICENSE                     # MIT License
├── README.md                   # Where to start
└── requirements.txt            # The dependencies
```

The process is the following:

- Loading data from Confluence
  - You can keep the Markdown style using the `keep_markdown_format` option added in our [MR]('https://github.com/langchain-ai/langchain/pull/8246')
  - See the `help_desk.ipynb` for a more deep dive analysis
  - Otherwise you cannot split text in a smart manner using the [MarkdownHeaderTextSplitter]('https://python.langchain.com/docs/modules/data_connection/document_transformers/text_splitters/markdown_header_metadata')
- Load data
- Markdown and RecursiveCharacterTextSplitter
- LLM used: Open AI LLM and embedding
- The QARetrievalChain
- Streamlit as a data interface
