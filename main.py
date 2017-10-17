from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy 


app = Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blog-admin:trump@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(254))
    body = db.Column(db.String(2000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/blog', methods = ['POST', 'GET'])
def index():
    
    blog = Blogs.query.all()
    return render_template("index.html", blogs=blog)

@app.route('/blog_post', methods = ['GET','POST'])
def blogpost():
    Blog_id = request.args.get('id')
    blog = Blogs.query.filter(Blogs.id == blog_id).first()
    return render_template('blog_post.html', blog=blog)



@app.route('/new_post', methods = ['GET','POST'])
def enter_blog():

    if request.method == 'POST':
        title_entry = request.form['title']
        body_entry = request.form['body']
        title_error = ''
        body_error = ''
        

        if body_entry == "" and title_entry == "":
            title_error = "Please put something in the title."
            body_error = "Please put something in the body."
            return render_template('add_entry.html',title_entry = title_entry, body_entry=body_entry, body_error=body_error, title_error=title_error)        
        if title_entry == "":
            title_error = "Please put something in the title."
            return render_template('add_entry.html',title_entry = title_entry, body_entry=body_entry, title_error=title_error)
        if body_entry == "":
            body_error = "Please put something in the body."
            return render_template('add_entry.html',title_entry = title_entry, body_entry=body_entry, body_error=body_error)
        else:
            new_blog = Blogs(title_entry, body_entry)
            db.session.add(new_blog)
            db.session.commit()
            return render_template('blog_post.html', title_entry = title_entry, body_entry = body_entry)

    return render_template('add_entry.html')

if __name__ == "__main__":
    app.run()
