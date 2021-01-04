import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from src.auth.auth import requires_auth, AuthError
from src.database.modelss import *


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"*": {"origins": "*"}})
    db = getDBReferance()


    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response




    @app.route("/drinks", methods=["GET"])
    def get_drinks():
        drinks = Drink.query.all()
        return jsonify({
            'success': True,
            'drinks': [x.short() for x in drinks]
        })


    @app.route("/drinks",methods=["POST"])
    @requires_auth("post:drinks")
    def add_drink(payload):
        requestBody = request.get_json()
        try:

            recipe = requestBody['recipe']
            title = requestBody['title']
            newDrink=Drink(recipe=json.dumps(recipe),title=title)
            newDrink.insert()
            return jsonify({'success':True,'drinks':[newDrink.long()]})
        except BaseException as s:
            print(s)
            abort(400)

    @app.route("/drinks-detail", methods=["GET"])
    @requires_auth("get:drinks-detail")
    def get_drinks_detail(payload):
        drinks = Drink.query.all()
        return jsonify({
            'success': True,
            'drinks': [x.short() for x in drinks]
        })

    @app.route("/drinks/<int:id>", methods=["DELETE"])
    @requires_auth("delete:drinks")
    def remove_drink(payload,id):
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        if not drink:
            abort(404)
        try:
            drink.delete()
            return jsonify({"success": True, "delete": id})
        except:
            abort(400)

    @app.route("/drinks/<int:id>", methods=["PATCH"])
    @requires_auth("patch:drinks")
    def update_drink(payload,id):
        drink = Drink.query.filter(Drink.id == id).one_or_none()

        if not drink:
            abort(404)
        try:
            requestBody = request.get_json()
            recipe = requestBody['recipe']
            title = requestBody['title']
            drink.title=title
            drink.recipe=json.dumps(recipe)
            drink.update()
            return jsonify({'success':True,'drinks':[drink.long()]})
        except:
            abort(400)




    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not Found"
        }), 404

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error
        }), error.status_code

    return app
