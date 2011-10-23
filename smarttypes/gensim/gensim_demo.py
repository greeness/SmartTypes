

import gensim
from collections import defaultdict

#small social network (following, link_weight)
social_network = [
    [(1,1), (2,1)],
    [],
    [(1,1), (2,1)],
    [(4, 1)],
    [(3, 1)],
]

#user_corpus
user_text = [
    ['survey', 'user', 'computer', 'system', 'response', 'time'],
    ['eps', 'user', 'interface', 'system'],
    ['user', 'response', 'time'],
    ['graph', 'trees'],
    ['graph', 'minors', 'survey'],
]
user_corpus_dictionary = gensim.corpora.Dictionary(user_text)
user_corpus = [user_corpus_dictionary.doc2bow(text) for text in user_text]

#communities
num_communities = 3
community_lda = gensim.models.ldamodel.LdaModel(social_network, 
                                                num_topics=num_communities, 
                                                update_every=0, passes=20)
communities = community_lda.show_topics(topics=-1, formatted=False)

#map user_corpus to community_text
community_text = defaultdict(lambda: defaultdict(int))
for i in range(len(communities)):
    for user_participation_score, user_index in communities[i]:
        for word_id, default_score in user_corpus[int(user_index)]:
            community_text[i][word_id] += 1 * user_participation_score

#convert community_text to community_corpus
community_corpus = []
for i in range(num_communities):
    community_corpus.append(
        [(word_id, score) for word_id, score in community_text[i].items()])
#this isn't working right
#community_corpus_tfidf = gensim.models.TfidfModel(community_corpus, id2word=user_corpus_dictionary)
#community_corpus = community_corpus_tfidf[community_corpus]

#community_corpus_topics
num_topics = 3
topic_lda = gensim.models.ldamodel.LdaModel(
    community_corpus, id2word=user_corpus_dictionary, 
    num_topics=num_topics, update_every=0, passes=20)
topics = topic_lda.show_topics(topics=-1, formatted=False)





