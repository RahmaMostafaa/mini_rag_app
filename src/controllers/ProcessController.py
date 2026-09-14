from .BaseController import BaseController
from .ProjectController import ProjectController
import os

from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from models import ProcessingEnums


class ProcessController(BaseController):

    def __init__(self , project_id:str):
        super().__init__()

        self.project_id=project_id
        self.project_path=ProjectController().get_project_path(project_id=project_id)

# Get file extension from file path

    def get_file_extension(self, file_id:str):
        return os.path.splitext(file_id)[-1]
# Handle methods of loading file contents based on files extensions

    def get_file_loader(self, file_id:str):

        file_ext= self.get_file_extension(file_id=file_id)
        #To get file path (project_path + file_id)
        file_path=os.path.join(
            self.project_path,
            file_id
        )
        if file_ext == ProcessingEnums.TEXT_EXT.value:
            return TextLoader(file_path, encoding ="utf_8")

        if file_ext == ProcessingEnums.PDF_EXT.value:
            return PyPDFLoader(file_path)

        return None
# Use help get_file_loader to load the content
    def get_file_content(self, file_id:str):

        Loader = self.get_file_loader(file_id=file_id)
        return Loader.load()
# To extract file content+metadata then make chunking
    def process_file_content(self, file_content:list, file_id:str, chunk_size:int=100, overlap_size: int=20): #file_content=>Documents(content+Metadata)

        text_splitter= RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap_size,
            length_function=len,
        )

       #To get content
        file_content_texts=[
            rec.page_content
            for rec in file_content
        ]

        #To get metadata
        file_content_metadata=[
            rec.metadata
            for rec in file_content
        ]
        
        #Chunking the data
        chunks= text_splitter.create_documents(
            file_content_texts,
            metadatas=file_content_metadata
        )

        return chunks