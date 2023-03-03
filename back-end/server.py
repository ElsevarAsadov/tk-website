from flask import Flask, render_template
from datetime import datetime
from os.path import isfile

class Server(Flask):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
    #Routes
    
    @self.route("/")
    @self.route("/home")
    def home():
      return render_template("home.html")
    
    @self.route("/about")
    def about():
      return render_template("about.html")
    
    @self.route("/table")
    def table():
      return render_template("table.html")
    
    @self.route("/sabah")
    def sabah():
      return render_template("sabah.html")
  
    #Functionality
    
    @self.template_global("getsemester")
    def gettime():
      
      now = datetime.now()

      if isfile("static/cedvel/cedvel.pdf"):
        
        if datetime(now.year, 9, 15) <= now < datetime(now.year+1, 2, 16):  
          return f"{now.year} PAYIZ SEMESTERİ üçün nəzərdə tutulub!"
        
        elif datetime(now.year, 2, 15) <= now < datetime(now.year, 6, 15):
          return f"{now.year} YAZ SEMESTERİ üçün nəzərdə tutulub!"
        
        else:
          return  "Hal hazırda yay tetili ilə əlaqadər cedvəl hazır deyil."
          
      else:
        return  "Hal hazırda cədvəl hazır deyil"
         
    
if __name__ == "__main__":
  
  server = Server(
    import_name=__name__,
    template_folder="../front-end/template",
    static_folder="../static")
  
  server.run(debug=True)
    
      