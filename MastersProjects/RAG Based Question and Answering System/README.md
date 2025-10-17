# CMPS 6730 RAG Based Question and Answering system

# Goals:

Our goal in this project was to create a RAG Bases Question and Answering system and exeperiment with various chunking methods
in order to get the best results

# Methods Used:

Our goal is to develop a chatbot that leverages the Retrieval-Augmented Generation (RAG) architecture to provide accurate and contextually relevant responses with minimal retraining. The system comprises of two main modules: a retrieval module that fetches relevant information from the knowledge base and the large language model that generates the final response based on the user query and the retrieved context (see Figure 1 for a high-level diagram)
![image](https://github.com/user-attachments/assets/f7ab0b0e-1cd3-405b-b3a1-b0b3bb32a646)

The system first takes a user query and uses the retrieval module to identify the top five most relevant documents from the knowledge base. These retrieved documents, along
with the original user query, are then fed into the large language model to generate the response.

1. Retrieval Module:

  The retrieval module or component of our chatbot operates as follows: 

• Knowledge Base: Our knowledge base is the MS MARCO[2] dataset, an open-source, human-generated machine reading comprehension dataset curated for question answering.
• Embedding Generation: To represent both user queries and documents within the MS-MARCOdataset as dense vectors, we utilize the Sentence Transformer all-MiniLM-L6
  v2[5] model. This model is known for generating effective sentence embeddings.
• Indexing and Similarity Search: For efficient storage and retrieval of these vector embeddings, we employ the FAISS. Specifically, we use the IndexFlatL2[3] index, which
  performs a flat (brute-force) k-nearest neighbors search based on the Euclidean distance (L2 norm) between the query vector and the document vectors.
• Retrieval Process: When a user inputs a query (Xq), it is first encoded into an embedding Q(Xq) using the Sentence Transformer model. We then calculate the Euclidean 
  distance between this query embedding and all document embeddings within our FAISS index. The top five documents with the smallest Euclidean distances (i.e., the most 
  similar) are retrieved as context.

2. Large Language Model:
   The generative component of our chatbot is powered by the microsoft/phi-3-mini-instruct[1] model. This instruction-tuned LLM is designed for high-quality reasoning and 
   was trained on a publicly available dataset. The retrieved top five documents, along with the original user query, are provided as context to this parameterized LLM (Pθ) 
   to generate a relevant and informative response. The LLM processes both the non-parametric memory (retrieved documents) and its internal parametric knowledge to produce 
   the final output.

In this project we had experimented with two different chunking stratagies. Chunking is the process of dividing a pargraph into smaller pieces and converting these smaller
chunks into embeddings for storage into our vector database. These are the following chunking stratagies we have implemented:
1. Recursive Based Chunking
2. Token Based Chunking

# Experimentation:

In hopes to find the best performing system we have experimented with both these methods in hopes to find the more effective choice for a system. The following experiments
were conducted on 50 randomized queries:
1. Token Based Chunking with Chunk size=200 and no overlapping
2. Recursive Based Chunking with Chunk size=200 and no overlapping
3. Recursive Based Chunking with Chunk size=200 and 20% overlapping
4. Recursive Based Chunking with Chunk size=200 and 50% overlapping

# Conclusions:

Based on our observations, the choice of document chunking strategy significantly impacts the performance of the RAG-based question answering system, as measured by the ROUGE-L score. While the average performance is relatively close, the introduction of overlap within the recursive chunking method demonstrates a promising avenue for improvement. Specifically, the recursive strategy with a 50% overlap yielded the highest mean and median ROUGE-L scores across our evaluation set. This suggests that providing more continuous contextual information to the language model can lead to better alignment with the reference answers.


![image](https://github.com/user-attachments/assets/041a878b-e8ca-4ef3-9f2c-c540fc447ec0)

# Notes:

1. The code does not currently include a Hugging Face API key. You can generate this key from your personal Hugging Face account. Please add your API key in the designated cell within the notebook.
2. During module installation, you may be prompted to restart the session. If this happens, restart the session as instructed, but do not re-run the same command or any commands that precede it.
