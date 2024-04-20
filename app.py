import datetime
import os
from flask import Flask,render_template,request
from pymongo import MongoClient
from dotenv import load_dotenv


load_dotenv()
def create_app():
    
    app = Flask(__name__)
    client = MongoClient(os.getenv("DB_URI"))
    app.db= client.notesDb
    notes=[]
    @app.route("/",methods=["POST","GET"])
    def home():
        if request.method == "POST":
            note = request.form.get("note")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            app.db.notes.insert_one({
                "note":note,
                "date":formatted_date
            })
        notes_with_date=[
            (
                note["note"],
                note["date"],
                datetime.datetime.strptime(note["date"],"%Y-%m-%d").strftime("%b %d")
            )
            for note in app.db.notes.find().sort({"_id": -1})
        ]
        return render_template("index.html",notes=notes_with_date,num=len(notes_with_date))
    
    return app