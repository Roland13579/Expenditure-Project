import requests
from flask import Flask, render_template, request, redirect
from cs50 import SQL

app=Flask(__name__)

app.config["DEBUG"]=True
app.config["TEMPLATES_AUTO_RELOAD"] = True

db=SQL("sqlite:///expenditures.db")

CATEGORIES = [
    "fashion",
    "skincare",
    "transport",
    "food",
    "hobbies",
    "travel",
    "essentials",
    "activities",
    "others"
]

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cashe, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
    
    
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        item = request.form.get("item")
        category = request.form.get("category")
        cost = request.form.get("cost")
        remarks = request.form.get("remarks")
        
        if not item:
            return render_template("error.html")
        elif not cost:
            return render_template("error.html")
        elif not category:
            return render_template("trial.html")
        
            
        db.execute("INSERT INTO expenditure (item, category, remarks, cost) VALUES( ?, ?, ? ,?)", item, category, remarks, cost)
        return redirect("/")
        
    else:
        
        COSTS = []
        total_cost = 0
        costs = db.execute("SELECT cost FROM expenditure")
        # note that the output given by the database is eg. [{'cost': 10}, {'cost'}]
        for value in costs:
            COSTS.append(value['cost'])
            
        for i in COSTS:
            total_cost += i

        expenditure = db.execute("SELECT * FROM expenditure")
        return render_template("layout.html", categories=CATEGORIES, expenditure=expenditure, total_cost = total_cost)
    
    