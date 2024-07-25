# Imports
# Env var
import os
from dotenv import load_dotenv, find_dotenv

# Env variables
_ = load_dotenv(find_dotenv())

CURRENT_DIR=os.path.dirname(os.path.abspath(__file__))

OPEN_AI_API_KEY = os.environ['OPENAI_API_KEY']
MODEL_TYPE_INFERENCE = os.environ['MODEL_TYPE_INFERENCE']
MODEL_TYPE_EMBEDDING = os.environ['MODEL_TYPE_EMBEDDING']
FORCE_EMBEDDINGS_DB_RELOAD = True if os.environ['FORCE_EMBEDDINGS_DB_RELOAD'].lower() == 'true' else False
CONFLUENCE_SPACE_NAME = os.environ['CONFLUENCE_SPACE_NAME']
CONFLUENCE_API_KEY = os.environ['CONFLUENCE_PRIVATE_API_KEY']

# Hint: space_key and page_id can both be found in the URL of a page in Confluence
# https://yoursite.atlassian.com/wiki/spaces/<space_key>/pages/<page_id>
# or https://confluence.domain.com/
CONFLUENCE_SPACE_KEY = os.environ['CONFLUENCE_SPACE_KEY']

CONFLUENCE_USERNAME = os.environ['TOKEN_NAME']
PATH_NAME_SPLITTER = f'{CURRENT_DIR}/splitted_docs.jsonl'
PERSIST_DIRECTORY = f'{CURRENT_DIR}/db/chroma/'
EVALUATION_DATASET = f'{CURRENT_DIR}/data/evaluation_dataset.tsv'
