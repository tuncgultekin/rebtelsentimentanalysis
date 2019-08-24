import os
import json
from flasgger import Swagger
from flask import Flask, request, jsonify
from model import SentimentPredictionModel

app = Flask(__name__)

params = {
    "flask_port": os.getenv('flask_port', 5050),
	"base_path": os.getenv('base_path',""),
}

app.config['SWAGGER'] = {
    "title": "Rebtel Sentiment Analysis Api",
    "description": "Rebtel Sentiment Analysis Api Specs",
    "termsOfService": "",
    "specs_route": params["base_path"]+"/api-docs/",
	"specs": [
        {
            "endpoint": params["base_path"]+'apispec_1',
            "route": params["base_path"]+'/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": params["base_path"]+"/flasgger_static",
	"basePath": params["base_path"]
}
swagger = Swagger(app)
model = SentimentPredictionModel()

@app.route(params["base_path"]+"/api/execute",methods=['post'])
def execute():
    """
    Sentiment Api Executor
    ---
    tags:
        - Model
    parameters:
        - in: body
          name: bodydata
          description: Run Model
          schema:
            type: object
            required:
              - data
            properties:
              data:
                type: string
    responses:
        200:
            description: Return a successful message
        400:
            description: Bad Request
        500:
            description: Server Internal error
    """
    try:
        post_data = request.get_json(force=True)  
        result = model.execute(post_data["data"])

        return jsonify(result)
    except Exception as e:
        return jsonify(str(e))

# Cross origin
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin','*')
    response.headers.add('Access-Control-Allow-Headers', "Authorization, Content-Type")
    response.headers.add('Access-Control-Expose-Headers', "Authorization")
    response.headers.add('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE, OPTIONS")
    response.headers.add('Access-Control-Allow-Credentials', "true")
    response.headers.add('Access-Control-Max-Age', 60 * 60 * 24 * 20)
    return response
	
app.secret_key = ''
app.config['SESSION_TYPE'] = 'filesystem'
app.run(host='0.0.0.0', port=params["flask_port"])