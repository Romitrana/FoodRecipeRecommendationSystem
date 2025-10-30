from flask import Flask, render_template, request, jsonify
from recommender import recommend_recipes, df

app = Flask(__name__,
            template_folder="frontend/template",
            static_folder="frontend/static")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    user_input = data.get("ingredient", "")

    if not user_input:
        return jsonify({"error": "Please enter an ingredient."}), 400

    try:
        recommendations = recommend_recipes(user_input)
        results = [
            {
                "name": row["name"],
                "ingredients": row["ingredients_name"],
                "instructions": row["instructions"],
            }
            for _, row in recommendations.iterrows()
        ]
        return jsonify({"recipes": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/recipe/<name>")
def recipe_detail(name):
    recipe = df[df['name'] == name].iloc[0].to_dict()
    return render_template("recipe.html", recipe=recipe)

if __name__ == "__main__":
    app.run(debug=True)
