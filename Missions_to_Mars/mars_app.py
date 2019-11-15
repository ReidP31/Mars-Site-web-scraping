from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo



# Create an instance of Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)



@app.route("/")
def home():

    # Find data from the mongo database
    mars_records = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", mars_records = mars_records)

    
@app.route("/scrape")
def m_scrape():
    import scrape_mars

    # Run the scrape function
    mars_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)