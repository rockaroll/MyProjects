import pickle
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from environment import API_KEY
model = SentenceTransformer("BAAI/bge-base-en-v1.5")

class LLMConnection:
  def __init__(self,Model,embeddingmodel,embeddings,content,index):
    self.modelllm=Model
    self.emodel=embeddingmodel
    self.embeddings=embeddings
    self.content=content
    self.index=index

  def Retreiver(self):
    query_embed=self.emodel.encode(self.query)
    qr=query_embed.reshape(-1,1).T
    distances,indexes=self.index.search(qr,self.top_k)
    results=[]
    for i in indexes[0]:
      results.append(self.content[i])
    return results

  def cusopenai(self,input_t):
    response1 =  self.modelllm.responses.create(
     model="gpt-4o",
     input=input_t
    )
    return response1.output_text

  def generate_response_openai(self,query):
    self.query=query
    print('User Query:'+self.query+'\n\n')
    similar_abstracts = self.Retreiver()
    # print(f' Retrive the Documnets  : {similar_abstracts}')
    input_text = f"User query: {self.query}\n\nContext:\n{similar_abstracts}"
    response=self.cusopenai(input_text)
    return response

  def exec(self,query,top_k=10):
    self.top_k=top_k
    self.Genresponse=self.generate_response_openai(query)
    return self.Genresponse
  
empath='Embeddings and Database/embeddings.pkl'
dbpath='Embeddings and Database/index.pkl'
contpath='Embeddings and Database/content.pkl'
embeddings=pickle.load(open(empath,'rb'))
index=pickle.load(open(dbpath,'rb'))
content=pickle.load(open(contpath,'rb'))
client1 = OpenAI(api_key=API_KEY)
LLMconn1=LLMConnection(client1,model,embeddings,content,index)
query='''List out different sources that can be created.'''
response2=LLMconn1.exec(query,top_k=30)
print(response2)