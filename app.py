import json
from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///simplificando.sqlite3'
db = SQLAlchemy(app)

class Tutorials(db.Model):
   title = db.Column(db.String(150), nullable=False)
   video_description = db.Column(db.String(500), nullable=False)
   video_key = db.Column(db.String(80), nullable=False)
   video_id = db.Column(db.String(80), nullable=False, primary_key=True,  autoincrement=False)
   
   def to_Json(self):
        return{"title": self.title, "video_description": self.video_description, "video_key": self.video_key, "video_id": self.video_id}

@app.route('/')
def index():
    try: 
        tutorials = Tutorials.query.all()
        tutorials_json = [tutorial.to_Json() for tutorial in tutorials]
        return rtn_response(200, "tutorials", tutorials_json)
    except Exception as e:
        return rtn_response(400, "tutorials", e, "Não foi possivel localizar os Tutoriais") 

@app.route('/new', methods=['POST'])
def new():
    try:
        body = request.get_json()
        tutorial = Tutorials(title=body['title'], video_description=body['video_description'], video_key=body['video_key'],  video_id=body['video_id'])
        db.session.add(tutorial)
        db.session.commit()
        return rtn_response(201, "tutorials", "Tutorial criado com sucesso")
    except Exception as e:
        return rtn_response(400, "tutorials", e, "Não foi possivel Criar o Tutorial") 


# @app.route('/<id>')
# def musica_pelo_id(id):
#    musica = Musica.query.get(id)
#    return render_template('index.html', musica=musica)

# @app.route('/edit/<id>', methods=['GET', 'POST'])
# def edit(id):
#    musica = Musica.query.get(id)
#    if request.method == "POST":
#       musica.nome = request.form['nome']
#       musica.artista = request.form['artista']
#       musica.link = request.form['link']
#       db.session.commit()
#       return redirect('/#playlist')
#    return render_template('edit.html', musica=musica)

# @app.route('/delete/<id>')
# def delete(id):
#    musica = Musica.query.get(id)
#    db.session.delete(musica)
#    db.session.commit()
#    return redirect('/#playlist')

def rtn_response(status, context_Name, context, mensagem=False):
    body = {}
    body[context_Name] = context
    if(mensagem):
        body["mensagem"] = mensagem 
    
    return Response(json.dumps(body), status=status, mimetype="application/json")

if __name__ == '__main__':
   db.create_all()
   app.run(debug=True)