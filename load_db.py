import os
import logging
import shutil
import time
from langchain_chroma import Chroma

from config import (
    CONFLUENCE_SPACE_NAME,
    CONFLUENCE_SPACE_KEY,
    CONFLUENCE_USERNAME,
    CONFLUENCE_API_KEY,
    PERSIST_DIRECTORY,
)

from langchain_community.document_loaders import ConfluenceLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import MarkdownHeaderTextSplitter


class DataLoader:
    """Create, load, save the DB using the confluence Loader"""

    def __init__(
        self,
        confluence_url=CONFLUENCE_SPACE_NAME,
        username=CONFLUENCE_USERNAME,
        api_key=CONFLUENCE_API_KEY,
        persist_directory=PERSIST_DIRECTORY,
    ):

        self.confluence_url = confluence_url
        self.username = username
        self.api_key = api_key
        self.persist_directory = persist_directory
        try:
            # create persist directory recursively
            os.makedirs(self.persist_directory, exist_ok=True)
        except Exception as e:
            logging.warning("%s", e)

    def load_from_confluence_loader(self):
        """Load HTML files from Confluence"""
        loader = ConfluenceLoader(
            url=self.confluence_url,
            token=self.api_key,
            cloud=False,
            space_key=CONFLUENCE_SPACE_KEY,
            # page_ids=["XXXXX", "XXXXX"],  # single pages (go to page settings then "Page info" and copy the page id in the URL)
            limit=50,
            max_pages=1000,
            min_retry_seconds=2,
            max_retry_seconds=10,
            include_comments=True,
            # include_attachments=True,
        )
        docs = loader.load()
        print("Number of documents retrieved:", len(docs))
        return docs

    def split_docs(self, docs):
        # Markdown
        headers_to_split_on = [
            ("#", "Titre 1"),
            ("##", "Sous-titre 1"),
            ("###", "Sous-titre 2"),
        ]

        markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=headers_to_split_on
        )

        # Split based on markdown and add original metadata
        md_docs = []
        for doc in docs:
            md_doc = markdown_splitter.split_text(doc.page_content)
            for i in range(len(md_doc)):
                md_doc[i].metadata = md_doc[i].metadata | doc.metadata
            md_docs.extend(md_doc)

        # RecursiveTextSplitter
        # Chunk size big enough
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=512,
            chunk_overlap=20,
            separators=["\n\n", "\n", "(?<=\. )", " ", ""],
        )

        splitted_docs = splitter.split_documents(md_docs)
        return splitted_docs

    def save_to_db(self, splitted_docs, embeddings):
        """Save chunks to Chroma DB"""
        for i, sub_splitted_doc in enumerate(splitted_docs):
            print(f"Saving paragraph to DB: {i+1}/{len(splitted_docs)}")
            time.sleep(0.05)  # rate-limiting API calls to OpenAI
            db = Chroma.from_documents(
                [sub_splitted_doc], embeddings, persist_directory=self.persist_directory
            )
        return db

    def load_from_db(self, embeddings):
        """Loader chunks to Chroma DB"""
        db = Chroma(
            persist_directory=self.persist_directory, embedding_function=embeddings
        )
        return db

    def set_db(self, embeddings):
        """Create, save, and load db"""
        try:
            shutil.rmtree(self.persist_directory)
        except Exception as e:
            logging.warning("%s", e)

        # Load docs
        docs = self.load_from_confluence_loader()

        # Split Docs
        splitted_docs = self.split_docs(docs)

        # Save to DB
        db = self.save_to_db(splitted_docs, embeddings)

        return db

    def get_db(self, embeddings):
        """Create, save, and load db"""
        db = self.load_from_db(embeddings)
        return db


if __name__ == "__main__":
    pass
