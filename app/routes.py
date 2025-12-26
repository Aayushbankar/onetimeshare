
from flask import Blueprint, current_app, request, jsonify
from config import Config
import os 
import uuid
import redis
from datetime import datetime
from werkzeug.utils import secure_filename



bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return 'OneTimeShare is running!'

@bp.route('/hello')
def hello():
    return 'Hello, World!'


@bp.route('/upload', methods=['POST'])
def upload_file():
    try:
#  
# 
#   try -1 copied this from teh offical docs to learn 
#  {{{      # if 'file' not in request.files:
        #     return jsonify({"error": "No file part in request"}), 400
        
        # file = request.files['file']
        
        # if file.filename == '':
        #     return jsonify({"error": "No file selected"}), 400
        
        # os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        # file_name = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
        # filepath = os.path.join(Config.UPLOAD_FOLDER, file_name)
        # # file.save(filepath)
        
        # return jsonify({
        #     "status": "success",
        #     "filename": file_name,
        #     "content_type": file.content_type
        # }), 201}}}



        # try 3 imlementation 


        if 'file' not in request.files:
            return jsonify({"error": "No file part in request"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        #check teh file extenion from teh allowed extenions 

        if file.filename.rsplit('.', 1)[1].lower() not in Config.ALLOWED_EXTENSIONS:
            return jsonify({"error": "File type not allowed"}), 400

        #check if file size is less then 20 Mib

        if file.content_length > Config.MAX_FILE_SIZE:
            return jsonify({"error": "File size too large"}), 400

        #generate a unique file name 
        file_name = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
        filepath = os.path.join(Config.UPLOAD_FOLDER, file_name)
        
        #SAVE FILE TO REDIS DB 
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True) 
        file.save(filepath)
        redis_client = redis.Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0,decode_responses=True)
        #add data to redis db tehn normal store with ttl of 5 hours 

        redis_client.hset(file_name, mapping={
            "filename": file_name,
            "content_type": file.content_type,
            "upload_time": datetime.utcnow().isoformat()
        })
        redis_client.expire(file_name,Config.REDIS_TTL)


        return jsonify({
            "status": "success",
            "filename": file_name,
            "real_filename":secure_filename(file.filename),
            "content_type": file.content_type,
            "upload_time": datetime.utcnow().isoformat(),
            "token": file_name,
        }), 201
        

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/test-redis')
def test_redis():
    try:
        r = current_app.redis_client
        hits = r.incr('hit_counter')
        return f"Hello! This page has been seen {hits} times. Redis is ALIVE."
    except Exception as e:
        return f"Redis Error: {str(e)}"


@bp.route('/list-files', methods=['GET'])
def list_files():
    try:
        r = current_app.redis_client
        files = r.keys('*')
        return jsonify({"files": files}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/info/<token>', methods=['GET'])
def file_info(token):
    try:
        r = current_app.redis_client
        file_info = r.hgetall(token)
        return jsonify(file_info), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500