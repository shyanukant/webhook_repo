from flask import Flask

from app.webhook.routes import webhook
from .extensions import mongo

# Creating our flask app
def create_app():

    app = Flask(__name__)
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/techBlog'
    # registering all the blueprints

    mongo.init_app(app)
    app.register_blueprint(webhook)
    
    return app
