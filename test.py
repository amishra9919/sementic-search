import time
from lexical_search import lexical_search
from vector_search import vector_search

query = "How can I make vector retrieval faster?"

start = time.perf_counter()
lexical_search(query, top_k=5)
lexical_time = time.perf_counter() - start

start = time.perf_counter()
vector_search(query, top_k=5)
vector_time = time.perf_counter() - start



print("lexical time: ", lexical_time)
print("vector time: ", vector_time)
