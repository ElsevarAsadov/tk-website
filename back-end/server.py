import shutil
import os
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from os.path import isfile, join
from sqlite3 import connect
from PIL import Image


class Server(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # news db path
        self.db_path = join("back-end", "database", "news.db")
        
        # checking if there is db or not if not then creates
        self.check_db()

        @self.route('/admin/parol=<int:password>', methods=["GET", "POST"])
        # admin page route
        def admin_page(password):
            # admin password to access
            if password == 1917:

                if request.method == "POST":

                    image_file = request.files.get("image")
                    header = request.form.get("header")
                    main = request.form.get("main")

                    # checking whether all necessary infos are given or not
                    if all((image_file, header, main)):
                        # Open the uploaded image
                        
                        img = Image.open(image_file.stream)
                        #last id in the db.
                        id = insertnews(header, main)
                                          
                        # Convert the image to PNG format and save it to the server
                        img.save(join("static", "media", "news", f"NEWS-{id}", "photo.png"), "png")

                return render_template("admin.html")

        @self.route("/")
        @self.route("/home")
        def home():
            title="Ana Səhifə"
            return render_template("home.html", title=title)

        @self.route("/about")
        def about():
            title="Kafedra Haqqında"
            return render_template("about.html", title=title)

        @self.route("/table")
        def table():
            title="Cədvəl"
            return render_template("table.html", title=title)

        @self.route("/sabah")
        def sabah():
            title="SABAH"
            return render_template("sabah.html", title=title)

        @self.route("/news")
        def news():
            title="Xəbərlər"
            return render_template("news.html", title=title)

        @self.route("/science")
        def science():
            title="Elmi Şura"
            return render_template("science.html", title=title)
        
        @self.route("/genius")
        def genius():
            title="Dahi Şəxsiyyətlər"
            return render_template("genius.html", title=title)
        
        @self.route("/tyutors")
        def tyutors():
            title="Tyutorlar"
            return render_template("tyutors.html", title=title)
        
        @self.route("/dissert")
        def dissert():
            title="Dissertasiya İşləri"
            return render_template("dissert.html", title=title)
        
        @self.route("/korea")
        def korea():
            title="Koreya Mərkəzi"
            return render_template("korea.html", title=title)

        # Functionality
        @self.template_global("getsemester")
        def gettime() -> str:
            """This function gets current time and determines
            the semester to show."""
            now = datetime.now()

            if isfile("static/cedvel/cedvel.pdf"):

                if datetime(now.year, 9, 15) <= now < datetime(now.year+1, 2, 16):
                    return f"{now.year} PAYIZ SEMESTERİ üçün nəzərdə tutulub!"

                elif datetime(now.year, 2, 15) <= now < datetime(now.year, 6, 15):
                    return f"{now.year} YAZ SEMESTERİ üçün nəzərdə tutulub!"

                else:
                    return "Hal hazırda yay tetili ilə əlaqadər cedvəl hazır deyil."

            else:
                return "Hal hazırda cədvəl hazır deyil"
              
        @self.template_global("insertnews")
        def insertnews(header: str, main: str, date=datetime.now().strftime("%Y-%m-%d")) -> str:
            """this function inserts news to the server"""

            conn = connect(self.db_path)
            curr = conn.cursor()

            curr.execute("SELECT MAX(rowid) FROM news")

            #greatest id 
            id = curr.fetchone()[0]
            
            #if there is no id then id=0
            if not id:
              id = 0
            
            curr.execute("""
                         INSERT INTO news (header, main, date, id) VALUES (?, ?, ?, ?)
                         """, (header, main, date, id+1))

            conn.commit()

            # getting latest news id
            id = curr.lastrowid
            
            conn.close()
            
            news_path = join("static", "media", "news", f"NEWS-{id}")

            os.makedirs(news_path)

            return id

        @self.template_global("deletenews")
        def deletenews(id: int) -> str:
            """This function deletes news from server"""

            conn = connect(self.db_path)

            c = conn.cursor()

            c.execute("DELETE FROM news WHERE rowid=?", (id,))
            conn.commit()

            conn.close()

            news_path = join("static", "media", "news")

            # deleting images of deleted news
            for dirpath, dirnames, filenames in os.walk(news_path):
                if f"NEWS-{id}" in dirnames:
                    dir_to_delete = os.path.join(dirpath, f"NEWS-{id}")
                    shutil.rmtree(dir_to_delete)

            return "XƏBƏRLƏR BAŞARIYLA SİLİNDİ"

        @self.template_global("getlatestnews")
        def getlatestnews() -> list[str, str, str, int]:
            """this function returns latest 4 news from db
            
            THERE SHOULD BE AT LEAST 4 NEWS IN DB TO WORK USER INTERFACE PROPERLY!!!!
            
            """

            conn = connect(self.db_path)

            c = conn.cursor()
            
            c.execute("SELECT * FROM news ORDER BY rowid DESC LIMIT 4")
            conn.commit()

            re = c.fetchall()

            conn.close()
            

            return re

        @self.template_global("getnews")
        def getnews(id: int) -> str:
            """this function returns corresponding news to id"""

            conn = connect(self.db_path)

            c = conn.cursor()

            c.execute(f"SELECT * FROM news WHERE rowid={id}")
            conn.commit()

            re = c.fetchall()

            c.close()

            return re
        
        
    def check_db(self):
      
      """is there is not db file then it creates db file
      and corresponging table"""
      
      if not isfile(self.db_path):
        conn = connect(join("back-end", "database", "news.db"))

        curr = conn.cursor()

        curr.execute("""
          CREATE TABLE IF NOT EXISTS news(
            header text,
            main text,
            date integer,
            id integer)
          
          """)
        conn.commit()
        conn.close()

if __name__ == "__main__":

    server = Server(
        import_name=__name__,
        template_folder="../front-end/template",
        static_folder="../static")

    server.run(debug=True)
