
from flask import Flask,render_template
from flask import request
import time;
app = Flask(__name__)

import pyrebase
config = {
  "apiKey": "AIzaSyCvlDFWtgRFya0sGR7-Me5BQhQXQYCN9h0",
  "authDomain": "sample-c594e.firebaseapp.com",
  "databaseURL": "https://sample-c594e.firebaseio.com",
  "storageBucket": "sample-c594e.appspot.com",
  # "serviceAccount": "path/to/serviceAccountCredentials.json"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

@app.route('/checkin',methods=['POST'])
def index():
    
   UserId =request.form['UserId'];
   Ratings=request.form['Ratings'];
   ResName=request.form['ResName'];
   ResId=request.form['ResId'];
   Review=request.form['Text'];
   Username=db.child("Users").child(UserId).get().val().values()[4];
   
   db_User = db.child("Users").child(UserId).child("Reviews")
   review_data = {"ResName":ResName, "Ratings":Ratings,"Created_At":time.time(),"ResId":ResId,"Text":Review}
   pushed_data=db.push(review_data)
   push_key=pushed_data.get('name')
   
   db_restaurants=db.child("Restaurants").child(ResId).child("attr_short").child("res_user_reviews").child(push_key)
   res_data={"profile_pic_small" : "Pic_url","review" :Review,"uid" : UserId,"username" : Username}
   db_restaurants.set(res_data)
   return 'Thanks For The Review'


@app.route('/',methods=['GET',	'POST'])
def imyform():

   return render_template('forms.html')  

   

if __name__ == '__main__':
   app.run(debug = True)