from flask import Flask, render_template

app = Flask(__name__)

@app.route('/director_homepage')
def director_homepage():
    return render_template('director_homepage.html')

if __name__ == "__main__":
    app.run(debug=True)