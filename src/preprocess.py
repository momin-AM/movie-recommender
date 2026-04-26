import pandas as pd
import ast

def convert(obj):
    L = []
    try:
        for i in ast.literal_eval(obj):
            L.append(i['name'])
    except:
        pass
    return L

def get_director(obj):
    try:
        for i in ast.literal_eval(obj):
            if i['job'] == 'Director':
                return i['name']
    except:
        pass
    return ""

def load_data(path):
    return pd.read_csv(path)

def preprocess(movies):
    movies['cast'] = movies['cast'].apply(convert)
    movies['crew'] = movies['crew'].apply(get_director)

    movies['cast'] = movies['cast'].apply(lambda x: x[:3])

    movies['cast'] = movies['cast'].apply(lambda x: [i.replace(" ", "") for i in x])
    movies['crew'] = movies['crew'].apply(lambda x: x.replace(" ", ""))

    movies['tags'] = movies['cast'].apply(lambda x: " ".join(x)) + " " + movies['crew']
    movies['tags'] = movies['tags'].apply(lambda x: x.lower())

    return movies[['movie_id', 'title', 'tags']]