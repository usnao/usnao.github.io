from flask import Flask, jsonify, request, render_template , redirect, url_for

from pymongo import MongoClient

connection_string = "mongodb://admin:lWSe9cgHKzHZFfEm@gradebook-cluster0-shard-00-00-l24me.mongodb.net:27017,gradebook-cluster0-shard-00-01-l24me.mongodb.net:27017,gradebook-cluster0-shard-00-02-l24me.mongodb.net:27017/test?ssl=true&replicaSet=GradeBook-Cluster0-shard-0&authSource=admin&retryWrites=true"

connection = MongoClient(connection_string)
db = connection['newport-rocketry']

members = db.members
articles = db.articles

app = Flask(__name__, static_url_path = "", static_folder = "static")
app.url_map.strict_slashes = False

@app.route("/index")
def index():
    return render_template("index.html")
    
@app.route("/tarc")
def tarc():
    return render_template("tarc.html")

@app.route("/sli")
def sli():
    return render_template("sli.html")

@app.route("/news")
def news():
    colors = ['#ffbcbc', '#ffc657', '#6e6bff', '#ba6dae', '#ea7272', '#6b94ff']
    list_articles = [[document['title'], 
                      colors[i % len(colors)],
                      document['link']] for i, document in enumerate(articles.find())]
    
    return render_template("news.html", titles = list_articles)

@app.route('/news/<article>')
def show_article(article):
    # Search for the article
    article = articles.find_one({
        "link" : '/news/' + article
    })

    if (article):
        return render_template('article.html', title = article['title'], markdown = article['markdown'])
    else:
        return 'hello',404

@app.route("/sponsorship")
def sponsorship():
    return render_template("sponsorship.html")

@app.route("/article")
def article():
    return render_template("article.html")

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if (request.method == 'GET'):
        return render_template('login.html')
    else:
        password = request.form.get('password')
        if password == 'rocketry':
            return redirect(url_for("admin"))
        else:
            return redirect(url_for("login"))

@app.route('/admin')
def admin():
    return render_template('admin_control.html')

@app.route("/change-members")
def show_change_members():
    documents = members.find()

    return render_template("change_members.html", members = documents)

@app.route('/members')
def show_members():

    # Oh my god please fix this soon
    
    documents = members.find()
    documents = {document.get('name') : document for document in documents if document.get('name') != None} 

    order = members.find_one({
        "thing" : "order"
    })

    return render_template('members.html', members = [documents.get(name) for name in order['order']])

@app.route('/remove-member', methods = ['POST'])    # might want to merge this with change members later
def remove_member():
    name = request.form.get("name")
    print(name);
    member = members.delete_one({
        "name": name
    })

    print(member)

    if (member):
        return '', 200
    else:
        return '', 404

@app.route('/update-member-order', methods = ['POST'])    # might want to merge this with change members later
def update_member_order():

    return '', 200

@app.route('/create-article')
def create_article():
    return render_template('create_article.html')

@app.route("/publish-article", methods = ['POST'])
def publish_article():
    title = request.form.get('title')
    markdown = request.form.get('markdown')

    if (title == None or markdown == None):
        return "bad request"
    else:
        articles.insert_one({
            "title" : title,
            "markdown" : markdown,
            "link" : '/news/' + clean_title(title)
        })

        return jsonify({
            "status" : "success!"
        })

def clean_title(title):
    res = ''
    for a in title:
        if a.lower() in 'abcdefghijklmnopqrstuvwxyz0123456789-_':
            res += a.lower()
        elif a == ' ':
            res += '-'
    
    return res

app.run(debug = True)
