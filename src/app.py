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
    

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    
    member = jackson_family.get_member(member_id)
    if not member:
        return jsonify({"msg": "Member not found"}), 404
    try:
        return jsonify({"member": member}), 200
    except Exception as e:
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500


@app.route('/member', methods=['POST'])
def add_new_member():
    data = request.get_json()
    if not data:
        return jsonify({"msg": "No data provided"}), 400
    
    new_member = {
        "first_name": data["first_name"],
        "age": data["age"],
        "lucky_numbers": data["lucky_numbers"]
    }

    try:
        new_member_add = jackson_family.add_member(new_member)
        return jsonify({"msg": "New member created",
                        "member": new_member_add}), 201
    except Exception as e:
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500


@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    
    member = jackson_family.get_member(member_id)
    if not member:
        return jsonify({"msg": "Member not found"}), 404

    try:
        member_delete = jackson_family.delete_member(member_id)
        return jsonify({"msg": "Member deleted",
                        "member": member}), 200
    except Exception as e:
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500


# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
