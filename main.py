from src.preprocess import load_data, preprocess
from src.model import train, save_model

# load + preprocess
movies = load_data("data/movies.csv")
movies = preprocess(movies)

# train
cv, similarity = train(movies)

# save
save_model(movies, similarity)

print("Model trained and saved ✅")