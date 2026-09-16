bm_results = [
    {
        "id": 3,
        "content": "Python is widely used for machine learning and data science.",
        "score": 2.056936016079452
    },
    {
        "id": 1,
        "content": "PostgreSQL is a relational database system.",
        "score": 0.0
    },
    {
        "id": 2,
        "content": "My name is Arpit and i am working on Mac",
        "score": 0.0
    },
    {
        "id": 4,
        "content": "PostgreSQL can store structured relational data in tables.",
        "score": 0.0
    },
    {
        "id": 5,
        "content": "A car needs regular maintenance to keep the engine healthy.",
        "score": 0.0
    }
]


vector_search = [
    {
        "id": 8,
        "content": "Neural networks learn patterns from training data.",
        "score": 0.47542999611584436
    },
    {
        "id": 3,
        "content": "Python is widely used for machine learning and data science.",
        "score": 0.6614864748071931
    },
    {
        "id": 11,
        "content": "Windows are simpler than Mac",
        "score": 0.7862445244557423
    },
    {
        "id": 13,
        "content": "Postgres is good to learn for resume",
        "score": 0.807790987793174
    },
    {
        "id": 2,
        "content": "My name is Arpit and i am working on Mac",
        "score": 0.8762589431173462
    }
]

scores = {}
k = 60

for rank, result in enumerate(bm_results, start=1):
    scores[result['id']] = scores.get(result['id'], 0)
    """OR (ABOVE LINE)
    if doc_id not in rrf_scores:
        rrf_scores[doc_id] = 0
    """
    scores[result['id']] += 1/(k+rank)

for rank, result in enumerate(vector_search, start=1):
    scores[result['id']] = scores.get(result['id'], 0)
    scores[result['id']] += 1/(k+rank)
print(scores)
ranked = sorted(
    scores.items(),
    key = lambda x:x[1],
    reverse=True
)
print(ranked)

