from flask import Flask, Blueprint, jsonify, request, g
from playhouse.shortcuts import model_to_dict
import models
import  string, random





DEBUG = True
PORT = 8000



app = Flask(__name__)



# ##########
@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response

##########

def shorten_url():
    letters = string.ascii_lowercase + string.ascii_uppercase
    loopControl = 0
    while True:
        print(loopControl)
        if loopControl== 100:
            break
        random_letters = random.choices(letters, k=6)
        random_letter_join = "".join(random_letters)
        loopControl = loopControl + 1
        try:
            short_url=models.Urls.get(models.Urls.short_url == random_letter_join)
        except models.DoesNotExist:
            shorten_url = "/" + random_letter_join
            return shorten_url




@app.route('/')
def index():
    return "Welcome to the url shortner"



# Pass in any URL using Json as {url: "Any URL"}
@app.route('/',  methods=["POST"])
def get_shoter_url():
    try:
        payload = request.get_json()
        print(payload)
        query = models.Urls.get(models.Urls.orginal_url == payload['url'])
        query_id= query.id
        print(query)
        query = models.Urls.update(count=query.count + 1).where(models.Urls.id==query.id)
        query.execute()
        url_query = model_to_dict(models.Urls.get_by_id(query_id))
        return jsonify(data=url_query, status={"code": 302, "message": "Url Already exists"})
    except models.DoesNotExist:
        short_url= shorten_url()
        print("\n\n\n")
        print(short_url)
        new_query = models.Urls.create(orginal_url=payload['url'], short_url=short_url)
        url_query = model_to_dict(models.Urls.get_by_id(new_query.id))
        return jsonify(data=url_query, status={"code": 201, "message": "New Url Created"}) 
    except:
        return jsonify({"Bad Request": 'Code Paramater not found'}, status= status.HTTP_400_BAD_REQUEST)




# Run the app when the program starts!
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)