import faiss
import pickle
import yaml
import json
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-base-en-v1.5")

class RAGImplementation:
  def __init__(self,context_s,context_d,context_c,embeddingmodel,embedding_path='',faiss_path='',content_path=''):
    self.context_s=context_s
    self.context_d=context_d
    self.context_c=context_c
    self.model=embeddingmodel
    self.system_path=embedding_path
    self.system_path1=faiss_path
    self.system_path2=content_path

  def BuildContext(self):
    content=[]
    for i in self.context_s[0].items():
        content.append(yaml.dump(i[1],sort_keys=False))
    for j in self.context_d[0].items():
        content.append(yaml.dump(j[1],sort_keys=False))
    for k in self.context_c[0].items():
        content.append(yaml.dump(k[1],sort_keys=False))
    if(self.system_path2!=''):
      pickle.dump(content,open(self.system_path2,'wb'))
    return content

  def GenEmbeddings(self):
    embeddings=self.model.encode(self.Content)
    if(self.system_path!=''):
      pickle.dump(embeddings,open(self.system_path,'wb'))
    return embeddings

  def opFaiss(self):
    embeddings_dim=self.embeddings.shape[1]
    index=faiss.IndexFlatIP(embeddings_dim)
    emb_mat=self.embeddings.reshape(-1,embeddings_dim).astype("float32")
    index.add(emb_mat)
    if(self.system_path1!=''):
      pickle.dump(index,open(self.system_path1,'wb'))
    return index

  def Exec(self):
    self.Content=self.BuildContext()
    self.embeddings=self.GenEmbeddings()
    self.DatabaseIndex=self.opFaiss()
    return self.Content,self.embeddings,self.DatabaseIndex


Sample_Source_Payload=json.load(open('Data Failes/Sample-Database(s).json','rb'))
Sample_Destination_Payload=json.load(open('Data Failes/Sample-Database(d).json','rb'))
Sample_Connection_Payload=json.load(open('Data Failes/Sample-Database(c).json','rb'))
empath='Embeddings and Database/embeddings.pkl'
dbpath='Embeddings and Database/index.pkl'
contpath='Embeddings and Database/content.pkl'

RAG1=RAGImplementation(Sample_Source_Payload,Sample_Destination_Payload,Sample_Connection_Payload,model,empath,dbpath,contpath)
content,emb,ind=RAG1.Exec()
print(content)