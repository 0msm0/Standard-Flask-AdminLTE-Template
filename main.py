from app import app, db
import views

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)