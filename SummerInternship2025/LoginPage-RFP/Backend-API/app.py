#Imports
from flask import Flask, request , jsonify 
import environment 
import RetrieveDet 
import hashlib
from reset import ChangePassword 
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
#Hashing Function
def HashingFunc(s):
      res1=hashlib.md5(s.encode())
      return res1.hexdigest()
#Routes for backend URLS
@app.route("/health")
def home():
     return jsonify({'message':'testing'})
#Importing configuration files path
configfile=environment.configuratfile 
#Login route for login page
@app.route("/login",methods=['POST'])
def loginauth():
     data=request.get_json()
     username=data['Username']
     password=HashingFunc(data['Password'])
     authinst1=RetrieveDet.Authorization(environment.configuratfile,username,password)
     authinst1.exec()
     message=authinst1.message 
     return jsonify({'message':message}) 
#Change password route
@app.route('/reset',methods=['POST'])
def resetpassword():
     data=request.get_json()
     email=data['Email1']
     email=email.replace(" ","")
     password=HashingFunc(data['Password3'])
     rpassword=HashingFunc(data['rPassword3'])
     if(password==rpassword):
          resetpasscode=ChangePassword(environment.configuratfile,password,email)
          resetpasscode.exec()
          message=resetpasscode.message
          return jsonify({"message":message})
     else:
          return jsonify({"message":"Original password and retyped password are not the same"})
if __name__=="__main__":
   app.run(debug=True, port=8081)

