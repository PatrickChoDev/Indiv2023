from abc import ABC, abstractmethod
import dotenv
import openai 
from openai import Embedding
import torch, os, getpass
from transformers import AutoTokenizer, AutoModel
from typing import Union
from huggingface_hub import InferenceClient
from langchain.embeddings.huggingface_hub import HuggingFaceHubEmbeddings

class BaseEmbedddingFunction(ABC):
  def __init__(self) -> None:
    super().__init__()

  @abstractmethod
  def __call__(self,text: str):
    raise NotImplementedError()


class OpenAIEmbeddingFunction(BaseEmbedddingFunction):
    def __init__(self,engine="text-similarity-davinci-001") -> None:
        super().__init__()
        self.__engine = engine
        dotenv.load_dotenv()
        api_token = dotenv.dotenv_values().get('OPENAI_API_TOKEN')
        openai.api_key = api_token if api_token else getpass.getpass("OpenAI API Token: ")
    
    def __call__(self, text: Union[str,list[str]]):
       return Embedding.create(input = [text] if type(text) == "str" else text, model=self.__engine)['data'][0]['embedding']


class LocalHuggingFaceEmbeddingFunction(BaseEmbedddingFunction):
    def __init__(self,model_name="gpt2") -> None:
        super().__init__()
        self.__tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.__model = AutoModel.from_pretrained(model_name)
    
    def __call__(self, text: Union[str,list[str]]):
        tokens = self.__tokenizer.encode(text, add_special_tokens=True, truncation=True)
        inputs = torch.tensor([tokens])
        with torch.no_grad():
            outputs = self.__model(inputs)
            embeddings = outputs.last_hidden_state.mean(dim=1).squeeze()
        return embeddings.tolist()

class HuggingFaceEmbeddingFunction(BaseEmbedddingFunction):
    def __init__(self,repo_id="sentence-transformers/all-mpnet-base-v2") -> None:
        super().__init__()
        dotenv.load_dotenv()
        api_token = dotenv.dotenv_values().get('HUGGINGFACEHUB_API_TOKEN')
        os.environ.update(HUGGINGFACEHUB_API_TOKEN=api_token if api_token else getpass.getpass("HuggingFaceHub API Token: "))
        self.__engine = HuggingFaceHubEmbeddings(repo_id=repo_id)
    
    def __call__(self, text: Union[str,list[str]]):
        return self.__engine.embed_documents([text] if type(text) == "str" else text)
    

class InferenceClientEmbeddingFunction(BaseEmbedddingFunction):
    def __init__(self,repo_id="gpt2") -> None:
        super().__init__()
        dotenv.load_dotenv()
        api_token = dotenv.dotenv_values().get('HUGGINGFACEHUB_API_TOKEN')
        os.environ.update(HUGGINGFACEHUB_API_TOKEN=api_token if api_token else getpass.getpass("HuggingFaceHub API Token: "))
        self.__engine = InferenceClient(model=repo_id)
    
    def __call__(self, text: Union[str,list[str]]):
        texts = [text] if type(text) == "str" else text
        return [self.__engine.feature_extraction(t) for t in texts]

if __name__=='__main__':
    openai_fn = LocalHuggingFaceEmbeddingFunction()
    print(openai_fn("Good morning"))