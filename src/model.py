import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def train(movies):
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(movies['tags']).toarray()

    similarity = cosine_similarity(vectors)

    return cv, similarity

def save_model(movies, similarity):
    pickle.dump(movies, open('model/movies.pkl', 'wb'))
    pickle.dump(similarity, open('model/similarity.pkl', 'wb'))

def load_model():
    movies = pickle.load(open('model/movies.pkl', 'rb'))
    similarity = pickle.load(open('model/similarity.pkl', 'rb'))
    return movies, similarity