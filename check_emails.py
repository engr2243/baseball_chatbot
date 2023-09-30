from app_creation import db, create_app
from models import User
from flask import (
    Flask,
    render_template,
    redirect,
    flash,
    url_for,
    session,
    jsonify,
    request
)

app = create_app()

@app.route('/emails')
def index():
    emails = User.query.all()
    num_emails = len([x.email for x in emails])
    return str(num_emails)

if __name__ == "__main__":
    app.run(port=8080)