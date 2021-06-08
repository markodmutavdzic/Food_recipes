from flask import request, jsonify
from sqlalchemy.sql.functions import count
from sqlalchemy import desc, asc

from clearbit_info import additional_data
from hunter import email_verifier
from model import app, User, db, Ingredient, Recipe


@app.route('/user_registration', methods=['POST'])
def user_registration():
    data = request.get_json()

    user = User.query.filter_by(username=data['username']).first()
    if user:
        return jsonify({"message": "User with that username already exists."}), 400

    if not email_verifier(data['email']):
        return jsonify({"message": "Invalid email"}), 400

    user_data = additional_data(data['email'])

    new_user = User(first_name=data['first_name'],
                    last_name=data['last_name'],
                    email=data['email'],
                    username=data['username'],
                    password=data['password'],
                    user_location=user_data['user_location'],
                    user_title=user_data['user_title'],
                    company_name=user_data['company_name'],
                    company_sector=user_data['company_sector'],
                    )
    db.session.add(new_user)
    db.session.commit()
    db.session.close()

    return jsonify({"message": "New user created."}), 200


@app.route('/user_login', methods=['POST'])
def user_login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"message": "No such user."}), 400
    if password != user.password:
        return jsonify({"message": "Invalid password"}), 400
    return jsonify({"token": "ovo je token"}), 200
    # potrebno uraditi token


@app.route('/recipe_create', methods=['POST'])
def recipe_create():
    data = request.get_json()
    name = data['name']
    text = data['text']
    ingredients = data['ingredients'].replace(',', ' ').split()

    existing_recipe = Recipe.query.filter_by(name=name).first()
    if existing_recipe:
        return jsonify({"message": "Recipe with that name already exists"}), 400
    # dodati usera
    new_recipe = Recipe(
        name=name,
        text=text,
        rating=0.0,
        ingredients=ingredients,
        # user
    )

    db.session.add(new_recipe)
    db.session.commit()
    db.session.close()

    ingredients_db = Ingredient.query.with_entities(Ingredient.name).all()
    ingredients_db_list = [r for (r,) in ingredients_db]

    for ingredient in ingredients:
        if ingredient not in ingredients_db_list:
            new_ingredient = Ingredient(name=ingredient)
            db.session.add(new_ingredient)
            db.session.commit()
            db.session.close()

    ingredient_object = Ingredient.query.all()
    for i in ingredient_object:
        if i.name in ingredients:
            i.recipe.append(new_recipe)

    db.session.commit()
    db.session.close()

    return jsonify({"message": "New recipe created."}), 200


@app.route('/recipe_rate', methods=['POST'])
def recipe_rate():
    data = request.get_json()
    recipe_id = data['recipe_id']
    rate = data['rate']

    recipe = Recipe.query.filter_by(id=recipe_id).first()
    if not recipe:
        return jsonify({"message": "Recipe with that id doesn't exist."}), 400
    if recipe.rating == 0.0:
        rating = rate
    else:
        rating = (recipe.rating + rate) / 2
    recipe.rating = rating
    db.session.commit()
    db.session.close()

    return jsonify({"Recipe rating": rating}), 200


def recipe_response(recipes_db):
    recipes = []
    for recipe in recipes_db:
        recipe_add = {
            "recipe id": recipe.id,
            "recipe name": recipe.name,
            "recipe text": recipe.text,
            "recipe ingredients": recipe.ingredients,
            "recipe rating": recipe.rating,
            "recipe user id": recipe.user_id,
        }
        recipes.append(recipe_add)
    return recipes


@app.route('/recipe_list_all')
def recipe_list_all():
    request_query = request.args.get('filter')
    if not request_query:
        recipes_db = Recipe.query.order_by(Recipe.id).all()
    else:
        recipes_db = (
            db.session.query(Recipe).select_from(Ingredient).join(Ingredient.recipe)
            .group_by(Recipe.id)
            .order_by(desc(count(Ingredient.id)) if request_query == 'max' else asc(count(Ingredient.id))).all()
        )

    recipes = recipe_response(recipes_db)

    return jsonify({"recipes": recipes}), 200


@app.route('/recipe_list_own')
def recipe_list_own():
    # user
    user_id = 1
    recipes_db = Recipe.query.filter_by(user_id=user_id).all()
    recipes = recipe_response(recipes_db)
    return jsonify({"recipes": recipes}), 200


@app.route('/ingredients_top')
def ingredients_top():
    ingredient_top_db = (db.session.query(Ingredient).select_from(Recipe).join(Ingredient.recipe).group_by
                         (Ingredient.id).order_by(count(Recipe.id).desc()).limit(5))

    top_ingredients = [{i.name: i.recipe.count()} for i in ingredient_top_db]

    return jsonify({"Top 5 ingredients": top_ingredients}), 200


@app.route('/recipe_search')
def recipe_search():
    request_query_name = request.args.get('name')
    request_query_text = request.args.get('text')
    request_query_ingredients = request.args.get('ingredients')

    recipes_db = Recipe.query.order_by(Recipe.id).all()
    recipes_list = []

    if request_query_name:
        search = request_query_name.replace(',', ' ').split()
        for recipe in recipes_db:
            recipe_name = recipe.name.replace(',', ' ').split()
            if all(x.lower() in [r.lower() for r in recipe_name] for x in search):
                recipes_list.append(recipe)
    elif request_query_text:
        search = request_query_text.replace(',', ' ').split()
        for recipe in recipes_db:
            recipe_text = recipe.text.replace(',', ' ').split()
            if all(x.lower() in [r.lower() for r in recipe_text] for x in search):
                recipes_list.append(recipe)
    elif request_query_ingredients:
        search = request_query_ingredients.replace(',', ' ').split()
        for recipe in recipes_db:
            recipe_ingredients = recipe.text.replace(',', ' ').split()
            if all(x.lower() in [r.lower() for r in recipe_ingredients] for x in search):
                recipes_list.append(recipe)
    else:
        return jsonify({"message": "Enter search parameter and value"}), 400

    recipes = recipe_response(recipes_list)
    return jsonify({"message": recipes}), 200


if __name__ == '__main__':
    app.run(debug=True)
