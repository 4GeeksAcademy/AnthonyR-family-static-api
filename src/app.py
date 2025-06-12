"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    if not members:
        return jsonify({"msg": "No members found"}), 404
    try:
        return jsonify(members), 200
    except Exception as e:
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500
    

@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    
    member = jackson_family.get_member(id)
    if not member:
        return jsonify({"msg": "Member not found"}), 404
    try:
        return jsonify(member), 200
    except Exception as e:
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500


@app.route('/members', methods=['POST'])
def add_new_member():
    data = request.get_json()
    if not data:
        return jsonify({"msg": "No data provided"}), 400
    if "first_name" not in data or "age" not in data or "lucky_numbers" not in data:
        return jsonify({"msg": "Missing required data"}), 400
    
    new_member = {
        "first_name": data["first_name"],
        "age": data["age"],
        "lucky_numbers": data["lucky_numbers"]
    }

    try:
        new_member_add = jackson_family.add_member(new_member)
        return jsonify(new_member_add), 200
    except Exception as e:
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500


@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    
    member = jackson_family.get_member(id)
    if not member:
        return jsonify({"msg": "Member not found"}), 404

    try:
        member_delete = jackson_family.delete_member(id)
        return jsonify({"done": True}), 200
    except Exception as e:
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500


# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
