# Food_recipes

Create (register) user:
POST
http://127.0.0.1:5000/user_registration

{
"first_name" : "Marko",
"last_name" : "Mutavdzic",
"email" : "marko.mutavdzic@factoryww.com",
"username" : "mare",
"password" : "0147" 
}


User login:
GET
http://127.0.0.1:5000/user_login

basic authentication 
username : "mare"
password : "0147"

Create recipe:
POST
http://127.0.0.1:5000/recipe_create
Header: acess-token :
{
"name" :"Bread",
"text" : "Mix water, flour and egg",
"ingredients" : "water, flour, egg"
}

Recipe rate:
POST
http://127.0.0.1:5000/recipe_rate
Header: acess-token :

{
"recipe_id" : 2,
"rate" : 5 
}



List of all recipes:
GET
opciono Query parametar:filter : max ili min
http://127.0.0.1:5000//recipe_list_all


Recpies list own:
GET
http://127.0.0.1:5000/recipe_list_own
Header: acess-token :

Get most used ingredients (Top 5):
GET
http://127.0.0.1:5000/ingredients_top

Search recipers:
GET
http://127.0.0.1:5000/recipe_search

Query parameters:
name
text
ingrediants

