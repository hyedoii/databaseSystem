from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "hello wwwwwwwwwwwwfwefwwworld"

if __name__ == ("__main__"):
  # docker
  #app.run(debug=True, host='0.0.0.0', port=5090)
  # other
  app.run(debug=True)
