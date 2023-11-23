from transformers import pipeline
from langchain.llms import HuggingFacePipeline
from langchain.docstore.document import Document
from langchain.chains.question_answering import load_qa_chain

class LLM_model:
    def __init__(self, model:str) -> None:
        generator = pipeline("text-generation", model=model, max_new_tokens=50, device_map="auto")
        generator.tokenizer.pad_token_id = generator.model.config.eos_token_id
        llm = HuggingFacePipeline(pipeline=generator)

        self.chain = load_qa_chain(llm=llm)
    
    def query(self, documents:list[Document], query:str) -> str:
        response = self.chain.run(input_documents=documents, question=query)
        return response.replace('[[:alnum:]]([\\s]{2,})', '')
