from flask import Flask, request, jsonify, abort
import requests
import logging
from flask_cors import CORS
from werkzeug.urls import url_encode

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app, origins='*')

@app.route('/cluster-tickets', methods=['POST'])
def cluster_tickets():
    data = request.get_json()
    if not data or 'tickets' not in data or not isinstance(data['tickets'], list):
        logging.error("Invalid data format: JSON body must be a list of ticket dictionaries.")
        abort(400, description="Bad Request: JSON body must be a list of ticket dictionaries.")
    
    tickets = data['tickets']
    descriptions = [
        " ".join([
            ticket.get('cause_by', ''),
            ticket.get('testes_realizados_by', ''),
            ticket.get('solution_by', ''),
            ticket.get('validated_by', '')
        ]).strip()
        for ticket in tickets if isinstance(ticket, dict)
    ]

    logging.info("Descriptions collected for normalization: %s", descriptions)

    try:
        normalized_response = requests.post('https://service-standardization-text-api.vercel.app/normalize', json={"texts": descriptions})
        normalized_response.raise_for_status()
        normalized_texts = normalized_response.json()
        logging.info("Normalized Texts received: %s", normalized_texts)
    except requests.exceptions.RequestException as e:
        logging.error("Error with normalization service: %s", e, exc_info=True)
        return jsonify({"error": str(e)}), 500

    try:
        logging.info("Sending descriptions to vectorization service.")
        vector_response = requests.post('https://service-vectorization-api.vercel.app/vectorize', json={"texts": normalized_texts})
        vector_response.raise_for_status()
        vectors = vector_response.json()
        logging.info("Vectors received from vectorization service: %s", vectors)
    except requests.exceptions.RequestException as e:
        logging.error("Error with vectorization service: %s", e, exc_info=True)
        return jsonify({"error": str(e)}), 500

    try:
        logging.info("Sending vectors to clustering service.")
        cluster_response = requests.post('https://service-group-api.vercel.app/cluster', json={"vectors": vectors})
        cluster_response.raise_for_status()
        labels = cluster_response.json()
        logging.info("Labels received from clustering service: %s", labels)
    except requests.exceptions.RequestException as e:
        logging.error("Error with clustering service: %s", e, exc_info=True)
        return jsonify({"error": str(e)}), 500

    clusters = {}
    for idx, label in enumerate(labels):
        clusters.setdefault(label, []).append(tickets[idx])

    logging.info("Final clusters formed: %s", clusters)
    return jsonify(clusters)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
