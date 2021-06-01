from flask import request, jsonify

from model import app, User, db


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


@app.route('/recipe_create')
def recipe_create():
    return ""


@app.route('/recipe_rate')
def recipe_rate():
    return ""


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