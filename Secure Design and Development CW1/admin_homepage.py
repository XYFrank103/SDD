from flask import Flask, render_template

app = Flask(__name__)

@app.route('/admin_homepage')
def admin_homepage():
    return render_template('admin_homepage.html')



if __name__ == "__main__":
    app.run(debug=True)
