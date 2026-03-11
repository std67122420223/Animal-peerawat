from animal import create_app
from animal.extensions import db

app = create_app()
app.secret_key = "secret123"

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)