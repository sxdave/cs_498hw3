from flask import Flask, jsonify, request
from pymongo import MongoClient, ReadPreference
from pymongo.write_concern import WriteConcern
from bson import ObjectId

app = Flask(__name__)

MONGO_URI = "mongodb+srv://shriyaxdave_db_user:wxrCEkHjTld0zcTp@cluster0.whar3xe.mongodb.net/?appName=Cluster0"
DB_NAME   = "ev_db"
COLL_NAME = "vehicles"

client = MongoClient(MONGO_URI)
db     = client[DB_NAME]
coll   = db[COLL_NAME]

@app.route("/insert-fast", methods=["POST"])
def insert_fast():
    record = request.get_json()
    if not record:
        return jsonify({"error": "No JSON body provided"}), 400

    fast_coll = coll.with_options(
        write_concern=WriteConcern(w=1)
    )
    result = fast_coll.insert_one(record)
    return jsonify({"inserted_id": str(result.inserted_id)}), 201

@app.route("/insert-safe", methods=["POST"])
def insert_safe():
    record = request.get_json()
    if not record:
        return jsonify({"error": "No JSON body provided"}), 400

    safe_coll = coll.with_options(
        write_concern=WriteConcern(w="majority")
    )
    result = safe_coll.insert_one(record)
    return jsonify({"inserted_id": str(result.inserted_id)}), 201

@app.route("/count-tesla-primary", methods=["GET"])
def count_tesla_primary():
    primary_coll = coll.with_options(
        read_preference=ReadPreference.PRIMARY
    )
    count = primary_coll.count_documents({"Make": "TESLA"})
    return jsonify({"count": count})

@app.route("/count-bmw-secondary", methods=["GET"])
def count_bmw_secondary():
    secondary_coll = coll.with_options(
        read_preference=ReadPreference.SECONDARY_PREFERRED
    )
    count = secondary_coll.count_documents({"Make": "BMW"})
    return jsonify({"count": count})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
