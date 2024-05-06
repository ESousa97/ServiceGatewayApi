from flask import Flask, request, jsonify
import requests
import logging
from flask_cors import CORS

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app, origins='*')

@app.route('/cluster-tickets', methods=['POST'])
def cluster_tickets():
    tickets = request.get_json()
    descriptions = [
        " ".join([
            ticket.get('cause_by', ''),
            ticket.get('testes_realizados_by', ''),
            ticket.get('solution_by', ''),
            ticket.get('validated_by', '')
        ]).strip()
        for ticket in tickets
    ]

    logging.debug(f"Descriptions: {descriptions}")

    try:
        normalized_response = requests.post('https://service-standardization-text-api.vercel.app/api/normalize', json={"texts": descriptions})
        normalized_response.raise_for_status()
        normalized_texts = normalized_response.json()
        logging.debug(f"Normalized Texts: {normalized_texts}")
    except requests.exceptions.RequestException as e:
        logging.error("Error with normalization service", exc_info=True)
        return jsonify({"error": str(e)}), 500

    try:
        vector_response = requests.post('https://service-vectorization-api.vercel.app/api/vectorize', json={"texts": normalized_texts})
        vector_response.raise_for_status()
        vectors = vector_response.json()
        logging.debug(f"Vectors: {vectors}")
    except requests.exceptions.RequestException as e:
        logging.error("Error with vectorization service", exc_info=True)
        return jsonify({"error": str(e)}), 500

    try:
        cluster_response = requests.post('https://service-group-api.vercel.app/api/cluster', json={"vectors": vectors})
        cluster_response.raise_for_status()
        labels = cluster_response.json()
        logging.debug(f"Labels: {labels}")
    except requests.exceptions.RequestException as e:
        logging.error("Error with clustering service", exc_info=True)
        return jsonify({"error": str(e)}), 500

    clusters = {}
    for idx, label in enumerate(labels):
        clusters.setdefault(label, []).append(tickets[idx])

    logging.debug(f"Clusters: {clusters}")
    return jsonify(clusters)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
