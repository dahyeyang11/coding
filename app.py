from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sprta:test@cluster0.neirhht.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form['bucket_give']
    
    count = list(db.bucket.find({}, {'_id':False}))
    num = len(count)+1

    doc = {
        'bucket':bucket_receive,
'num': num,
'done': 0
    }
    db.bucket.insert_one(doc)
    return jsonify({'msg': '저장 완료'})
    
@app.route("/bucket", methods=["GET"])
def bucket_get():
    all_buckets = list(db.bucket.find({},{'_id':False}))
    return jsonify({'result': all_buckets})

@app.route("/bucket/done", methods=["POST"]) 
def bucket_done(): 
      num_receive = request.form['num_give'] 
      db.bucket.update_one({'num': int(num_receive)}, {'$set': {'done': 1}})   
      return jsonify({'msg': '버킷 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)