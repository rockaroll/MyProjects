from flask import Flask,request,jsonify
from flask_cors import CORS 
from environment import SUPABASE_URL,SUPABASE_KEY 
# import os
# import toml
from Dataoperations import Dataops
app=Flask(__name__)
CORS(app)
@app.route('/safety',methods=['GET'])
def Safety():
    return jsonify({"message":"everything is working"})
@app.route('/retrieve',methods=['GET'])
def Retrieve():
    instance1=Dataops(SUPABASE_URL,SUPABASE_KEY)
    instance1.exec()
    data=instance1.data
    count=instance1.count
    return jsonify({"count":count,"message":data})
if __name__=='__main__':
    app.run(debug=True)