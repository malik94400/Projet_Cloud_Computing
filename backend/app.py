from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///files.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

AZURE_STORAGE_ACCOUNT = os.getenv("AZURE_STORAGE_ACCOUNT")
AZURE_STORAGE_KEY = os.getenv("AZURE_STORAGE_KEY")
AZURE_CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME")

connection_string = (
    f"DefaultEndpointsProtocol=https;"
    f"AccountName={AZURE_STORAGE_ACCOUNT};"
    f"AccountKey={AZURE_STORAGE_KEY};"
    f"EndpointSuffix=core.windows.net"
)

blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    blob_url = db.Column(db.String(500), nullable=True)

@app.route("/")
def home():
    return "Flask API running with Azure Blob!"

@app.route("/files", methods=["GET"])
def get_files():
    files = File.query.all()
    return jsonify([
        {
            "id": f.id,
            "filename": f.filename,
            "blob_url": f.blob_url
        }
        for f in files
    ])

@app.route("/files", methods=["POST"])
def add_file():
    data = request.json
    if not data or "filename" not in data:
        return jsonify({"error": "filename is required"}), 400

    new_file = File(filename=data["filename"])
    db.session.add(new_file)
    db.session.commit()
    return jsonify({"message": "File added"})

@app.route("/files/<int:file_id>", methods=["PUT"])
def update_file(file_id):
    file = File.query.get(file_id)

    if not file:
        return jsonify({"error": "File not found"}), 404

    data = request.json
    if not data or "filename" not in data:
        return jsonify({"error": "filename is required"}), 400

    file.filename = data["filename"]
    db.session.commit()

    return jsonify({"message": "File updated"})

@app.route("/files/<int:file_id>", methods=["DELETE"])
def delete_file(file_id):
    file = File.query.get(file_id)
    if not file:
        return jsonify({"error": "File not found"}), 404

    db.session.delete(file)
    db.session.commit()
    return jsonify({"message": "File deleted"})

@app.route("/upload", methods=["POST"])
def upload_file():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400

        uploaded_file = request.files["file"]

        if uploaded_file.filename == "":
            return jsonify({"error": "Empty filename"}), 400

        blob_client = container_client.get_blob_client(uploaded_file.filename)
        blob_client.upload_blob(uploaded_file, overwrite=True)

        blob_url = f"https://{AZURE_STORAGE_ACCOUNT}.blob.core.windows.net/{AZURE_CONTAINER_NAME}/{uploaded_file.filename}"

        new_file = File(filename=uploaded_file.filename, blob_url=blob_url)
        db.session.add(new_file)
        db.session.commit()

        return jsonify({
            "message": "File uploaded to Azure Blob Storage",
            "filename": uploaded_file.filename,
            "blob_url": blob_url
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/blobs", methods=["GET"])
def list_blobs():
    blobs = container_client.list_blobs()
    return jsonify([blob.name for blob in blobs])

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5001)