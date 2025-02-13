from flask import Flask, render_template

app = Flask(__name__)

@app.route('/artist_homepage')
def artist_homepage():
    return render_template('artist_homepage.html')

if __name__ == "__main__":
    app.run(debug=True)
