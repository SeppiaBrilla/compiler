from plugin_manager import Plugin_manager
from chat_manager import Chat_manager
import torch
from transformers import pipeline, AutoTokenizer
from langchain.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.chains.question_answering import load_qa_chain



conf = [
    {
        'name': 'list-folder-content',
        'parameters': 'ls:folder',
        'description':'lists all the file in a given folder'
    },
    {
        'name': 'say hello',
        'parameters': 'echo hello!:',
        'description':'say hello to you'
    }
]
# Chat_manager().run()

manager = Plugin_manager(conf)
generator = pipeline("text-generation", model="mistralai/Mistral-7B-v0.1", max_new_tokens=150, device_map="auto", offload_folder='model')
generator.tokenizer.pad_token_id = generator.model.config.eos_token_id
llm = HuggingFacePipeline(pipeline=generator)

chain = load_qa_chain(llm=llm)

query = '''These data describe a set of command you can use to fullfill some requests you can use them by calling the function followed by the charachter ":" and its parameters. 
The function call must be sourranded by the charachters _$ and $_. 
Example:
    function = list-folder-content
    correct call = _$list-folder-content:folder$_

Does exists a function that says hello to someone? if so, use it'''

response = chain.run(input_documents=str(manager), question=query)
print(response)
