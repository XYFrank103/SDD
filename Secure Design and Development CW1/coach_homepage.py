from flask import Flask, render_template

app = Flask(__name__)

@app.route('/coach_homepage')
def coach_homepage():
    return render_template('coach_homepage.html')

if __name__ == "__main__":
    app.run(debug=True)
