import json
from flask import Flask, Response, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///simplificando.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Tutorials(db.Model):
   title = db.Column(db.String(150), nullable=False) 
   video_description = db.Column(db.String(500), nullable=False)
   video_key = db.Column(db.String(80), nullable=False)
   video_id = db.Column(db.String(80), nullable=False, primary_key=True,  autoincrement=False)
   
   def to_Json(self):
        return{"title": self.title, "video_description": self.video_description, "video_key": self.video_key, "video_id": self.video_id}

@app.route('/')
def homepage():
    return("Simplificando")
    
@app.route('/v1/tutorials/', methods=['GET'])
def get_tutorial():
    try: 
        tutorials = Tutorials.query.all()
        tutorials_json = [tutorial.to_Json() for tutorial in tutorials]
        return rtn_response(200, "tutorials", tutorials_json)
    except Exception as e:
        return rtn_response(404, "tutorials", e, "Não foi possivel localizar os Tutoriais") 

@app.route('/v1/tutorials/<title>', methods=['GET'])
def search_tutorial(title):
    try:
        tutorials = Tutorials.query.all()
        tutorials_json = [tutorial.to_Json() for tutorial in tutorials]
        tutorials_search = [tutorial for tutorial in tutorials_json if title in tutorial['title']]
        return rtn_response(201, "tutorials", tutorials_search)
    except Exception as e:
        return rtn_response(404, "tutorials", e, "Não foi possivel localizar o Tutorial") 

def rtn_response(status, context_Name, context, mensagem=False):
    body = {}
    body[context_Name] = context
    if(mensagem):
        body["mensagem"] = mensagem 
    
    return Response(json.dumps(body), status=status, mimetype="application/json")

if __name__ == '__main__':
   db.create_all()
   app.run(debug=True)