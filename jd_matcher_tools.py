import os
import json
import pdfplumber
from semantic_kernel.functions import kernel_function, KernelArguments


class JDMatcherTools:

    def __init__(self):
        self.root_dir = os.path.abspath(os.path.dirname(__file__))  # Already at project root
        self.cv_dir = os.path.normpath(os.path.join(self.root_dir, "data", "resumes"))
        # self.cv_dir = "data/resumes"
        # self.root_dir = os.path.dirname(os.path.abspath(__file__))
        # self.root_dir = os.path.dirname(self.root_dir)  # Move up one level to the root workspace
        # self.cv_dir = os.path.normpath(os.path.join(self.root_dir, self.cv_dir))
        # self.cv_dir = os.path.normpath(
        #     os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "resumes")
        # )

    def extract_text_from_pdf(self, path):
        with pdfplumber.open(path) as pdf:
            return ' '.join(page.extract_text() for page in pdf.pages if page.extract_text()).lower()

    def load_and_parse_resumes(self):
        parsed_resumes = {}
        for filename in os.listdir(self.cv_dir):
            if filename.lower().endswith(".pdf"):
                file_path = os.path.join(self.cv_dir, filename)
                text = self.extract_text_from_pdf(file_path)
                parsed_resumes[filename] = text
        return parsed_resumes

    @kernel_function(
        name="load_and_parse_resumes",
        description="Parses all resume PDFs in data/resumes and returns a dict of filename -> text."
    )
    def parse_resumes_tool(self) -> str:
        resumes = self.load_and_parse_resumes()
        return json.dumps(resumes)  # To be passed into the next tool

    # @kernel_function(
    #     name="embed_and_store",
    #     description="Creates embeddings for resumes and a given job description, and stores them in Pinecone."
    # )
    # def embed_and_store(self, resumes: str, job_description: str) -> str:
    #     try:
    #         resumes = json.loads(resumes)
    #     except Exception as e:
    #         return f"❌ Failed to parse resume input: {e}"

    #     resume_embeddings = create_resume_embeddings(resumes)
    #     jd_embedding = create_jd_embedding(job_description)

    #     upsert_to_pinecone(resume_embeddings, namespace="resumes")
    #     upsert_to_pinecone([jd_embedding], namespace="job_description")

    #     return "✅ Embeddings stored in Pinecone successfully."