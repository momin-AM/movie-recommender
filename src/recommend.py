import pickle

movies = pickle.load(open('model/movies.pkl', 'rb'))
similarity = pickle.load(open('model/similarity.pkl', 'rb'))

def recommend(movie):
    # case-insensitive + partial match
    matches = movies[movies['title'].str.lower().str.contains(movie.lower())]

    if matches.empty:
        print("Movie not found 😢")
        return

    # pick first match
    movie_index = matches.index[0]
    movie_title = movies.iloc[movie_index].title

    print(f"\nShowing results for: {movie_title}\n")

    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    for i in movies_list:
        print(movies.iloc[i[0]].title)