import os
from flask import Flask
app = Flask(__name__)

print("env:" + os.environ['FLASK_ENV'] ) 
print("env2:" + app.config['ENV'])

# router handler
@app.route("/")
def hello():
    return "Hello Phu 5001 + flask + env!"

# python direct call
print("File:" + __name__)

if __name__ == "__main__":
    print("Exec Invoked")    
    app.run(host="0.0.0.0", port=int("5002"), debug=True)
else:
    print("Exec Imported")
