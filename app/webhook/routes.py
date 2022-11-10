from flask import Blueprint, request, render_template, jsonify
from ..extensions import mongo

webhook = Blueprint('Webhook', __name__)


@webhook.route('/receiver', methods=["POST"])
def receiver():
    
    if request.headers['Content-Type'] == 'application/json':
        data = request.json
        # print(data)
        if 'commits' in data:
            REQUEST_ID = data['commits'][0]['id']
            ACTION = 'Push'
            AUTHOR = data['commits'][0]['author']['name']
            TO_BRANCH = data['ref'][11:]
            FROM_BRANCH = ''
            TIMESTAMP = data['repository']['updated_at']

        elif 'pull_request' in data:
            if data['action'] == 'closed':
                MERGE_PULL = 'Merge'
                ID = data['pull_request']['head']['sha']
                TIME = data['pull_request']['merged_at']
            else:
                print('pull request')
                MERGE_PULL = 'Pull Request'
                ID = data['pull_request']['merge_commit_sha']
                TIME = data['pull_request']['created_at']

            REQUEST_ID = ID
            ACTION = MERGE_PULL
            AUTHOR = data['pull_request']['author_association']
            FROM_BRANCH = data['pull_request']['head']['ref']
            TO_BRANCH = data['pull_request']['base']['ref']
            TIMESTAMP = TIME

        collection = mongo.db.assignment
        collection.insert_one({
        'request_id': REQUEST_ID,
        'author': AUTHOR,
        'action': ACTION,
        'from_branch': FROM_BRANCH,
        'to_branch': TO_BRANCH,
        'timestamp': TIMESTAMP 
        })

        return jsonify(data)

    # return render_template('index.html', data)
    # return render_template('index.html')

@webhook.route('/')
def home():
    actions = list(mongo.db.assignment.find().sort("_id", -1).limit(1))
    act = actions[0]
    return render_template('index.html', actions = act)
    # return actions