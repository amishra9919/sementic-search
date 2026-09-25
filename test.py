from lexical_search import lexical_search
from vector_search import vector_search


lex_search = lexical_search('PostgreSQL supports full text search for searching textual information. Documents can be transformed into searchable representations and indexes can improve the performance of lexical search.')
vec_search = vector_search('PostgreSQL supports full text search for searching textual information. Documents can be transformed into searchable representations and indexes can improve the performance of lexical search.')

scores={}

for itr, result in enumerate(lex_search):

    rrf = 1/(60+itr)

    scores[result['id']] = scores.get(result['id'], 0)
    scores[result['id']] += rrf


for itr, result in enumerate(vec_search):

    rrf = 1/(60+itr)
    
    scores[result['id']] = scores.get(result['id'], 0)
    scores[result['id']] += rrf

print(scores)

ranked = sorted(
    scores.items(),
    key=lambda x:x[1],

)

print(ranked)

# result = [
#     {
#         'id' : scores[key],
#         'document_id' : 7
#     }
#     for key in scores.keys()
# ]
# print(result)
    