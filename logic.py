from flask import request, jsonify

from model import app, User, db, Ingredient, Recipe


@app.route('/user_registration', methods=['POST'])
def user_registration():
    data = request.get_json()
    new_user = User(first_name=data['first_name'],
                    last_name=data['last_name'],
                    email=data['email'],
                    username=data['username'],
                    password=data['password']
                    )
    db.session.add(new_user)
    db.session.commit()
    db.session.close()

    return jsonify({"message": "New user created."})


@app.route('/user_login', methods=['POST'])
def user_login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"message": "No such user."})
    if password != user.password:
        return jsonify({"message": "Invalid password"})
    return jsonify({"token": "ovo je token"})


@app.route('/recipe_create', methods=['POST'])
def recipe_create():
    data = request.get_json()
    name = data['name']
    text = data['text']

    existing_recipe = Recipe.query.filter_by(name=name).first()
    if existing_recipe:
        return jsonify({"message": "Recipe with that name already exists"})

    new_recipe = Recipe(
                name=name,
                text=text,
                rating=0.0,
                # user
                )

    db.session.add(new_recipe)
    db.session.commit()
    db.session.close()

    ingredients = data['ingredients'].replace(',', '').split()

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

    return jsonify({"message": "New recipe created."})


@app.route('/recipe_rate', methods=['POST'])
def recipe_rate():
    data = request.get_json()
    recipe_id = data['recipe_id']
    rate = data['rate']

    recipe = Recipe.query.filter_by(id=recipe_id).first()
    if not recipe:
        return jsonify({"message": "Recipe with that id doesn't exist."})
    if recipe.rating == 0.0:
        rating = rate
    else:
        rating = (recipe.rating+rate)/2
    recipe.rating = rating
    db.session.commit()
    db.session.close()

    return jsonify({"Recipe rating": rating})


@app.route('/recipe_list_all')
def recipe_list_all():
    return ""


@app.route('/recipe_list_own')
def recipe_list_own():
    return ""


@app.route('/ingredients_top')
def ingredients_top():
    return ""


if __name__ == '__main__':
    app.run(debug=True)