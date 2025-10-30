# recommender.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
df = pd.read_csv("data/Food_Recipe.csv") 

# Use only the necessary columns
df = df[['name', 'ingredients_name', 'instructions']]

# Handle missing values
df['ingredients_name'] = df['ingredients_name'].fillna("")
df['instructions'] = df['instructions'].fillna("")

# TF-IDF Vectorization on ingredients
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(df['ingredients_name'])

# Function to recommend recipes
def recommend_recipes(user_input, top_n=5):
    # Convert user query into vector
    user_vec = vectorizer.transform([user_input])
    
    # Compute cosine similarity
    similarities = cosine_similarity(user_vec, tfidf_matrix).flatten()
    
    # Get indices of top matches
    indices = similarities.argsort()[::-1][:top_n]
    
    # Return results as a DataFrame slice
    return df.iloc[indices][['name', 'ingredients_name', 'instructions']]


if __name__ == "__main__":
    # Quick test
    print(recommend_recipes("paneer tomato onion", top_n=3))
