from flask   import Flask, render_template
from json    import loads
from scripts import mongio

app = Flask(__name__)

# ======== Routing =========================================================== #

@app.route('/', methods=['GET'])
def index():
    volume, sentiment = {}, {}
    for document in mongio.db.logs.find():
        logs = loads(document['logs'])
        t = [i['timestamp'] for i in logs]
        v = [i['volume'] for i in logs]
        s = [i['sentiment'] for i in logs]
        volume[document['query']] = [{'x': i, 'y': j} for i, j in zip(t, v)]
        sentiment[document['query']] = [{'x': i, 'y': j} for i, j in zip(t, s)]
    
    return render_template('index.html', v=volume, s=sentiment)

# ======== Main ============================================================== #

if __name__ == "__main__":
    app.run(debug=True)