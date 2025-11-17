from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = "Super_Secret_Key"

API_KEY = "Comida"
API_SEARCH = "https://api.nal.usda.gov/fdc/v1/foods/search"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_food():
    food_name = request.form.get('food_name', '').strip()

    if not food_name:
        flash("Por favor ingresa un alimento", "error")
        return redirect(url_for('index'))

    try:
        params = {
            "api_key": API_KEY,
            "query": food_name
        }

        resp = requests.get(API_SEARCH, params=params)

        if resp.status_code == 200:
            data = resp.json()

            if not data.get("foods"):
                flash(f'El alimento "{food_name}" no fue encontrado', "error")
                return redirect(url_for('index'))

            food = data["foods"][0]  # primer resultado

            food_info = {
                "description": food["description"],
                "fdcId": food["fdcId"],
                "brandOwner": food.get("brandOwner", "No disponible"),
                "score": food.get("score", "N/A"),
                "nutrients": food.get("foodNutrients", [])
            }

            return render_template("food.html", food=food_info)

        else:
            flash("Error al buscar el alimento", "error")
            return redirect(url_for('index'))

    except requests.exceptions.RequestException:
        flash("Error al conectar con la API USDA", "error")
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
