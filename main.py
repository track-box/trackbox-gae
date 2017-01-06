import logging
import os
import json
import uuid

from flask import Flask, request, jsonify
from google.cloud import storage

app = Flask(__name__)

# Configure this environment variable via app.yaml
CLOUD_STORAGE_BUCKET = os.environ['CLOUD_STORAGE_BUCKET']

gcs = storage.Client()
bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)



@app.route('/create', methods=['POST'])
def upload():
    track_data = request.json

    print(track_data)

    if not track_data:
        return 'No track data uploaded.', 400

    track_id = create_track_json(track_data)
    create_edit_json(track_data, track_id)

    return jsonify({ 'message': 'ok' })


def create_track_json(track_data):
    track_id = generate_track_id()
    track_data['track_id'] = track_id

    upload_json(track_data, 'track/' + track_id)
    return track_id


def generate_track_id():
    id = uuid.uuid4().hex[:9] # 9byte

    while bucket.blob('track/' + id).exists():
        id = uuid.uuid4().hex[:9] # 9byte

    return id

def create_edit_json(track_data):
    edit_id = generate_edit_id()
    track_data['track_id'] = track_id
    track_data['edit_id'] = edit_id

    upload_json(track_data, 'edit/' + edit_id)


def generate_edit_id():
    id = uuid.uuid4().hex[:12] # 12byte

    while bucket.blob('edit/' + id).exists():
        id = uuid.uuid4().hex[:12] # 12byte

    return id


def upload_json(data, filename):
    blob = bucket.blob(filename)
    blob.upload_from_string(
        json.dumps(data),
        content_type='application/json'
    )


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
