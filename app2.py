# from flask import Flask, render_template, request



# app = Flask(__name__)
  


# @app.route("/")
# def index():
#     return render_template("index.html")


# @app.route('/result', methods=['POST'])

# def result():

#   if request.method == 'POST':

#     youtube_url = request.form['videoUrl']
#     print(youtube_url)
#     language = request.form['language']
#     print(language)
#     # Add your logic here to process the URL and language

#     return f"URL: {youtube_url}, Language: {language}"



# if __name__ == '__main__':
#   # app.run(host='192.168.0.105')
#   app.run(debug=True)