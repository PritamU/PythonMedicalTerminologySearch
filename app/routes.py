from flask import Blueprint, render_template, request, jsonify
from app.models import Diagnosis
from app import db
from app.searchLogics import search_concepts

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/search_suggestions')
def search_suggestions():
    # Fetch first 5 rows to confirm data presence
    try:

        query = request.args.get('q', '').lower()
        type = request.args.get('type', '').lower()
        if not (query or type):
            return jsonify([])
    
        results = search_concepts(query,type)

        print('results',results)

        return jsonify([
            dict(row._mapping) for row in results
        ])
    except Exception as e:
        print('something went wrong',e)
        return jsonify([])
