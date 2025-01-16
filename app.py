from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Message
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    session = Session()
    if request.method == 'POST':
        try:
            data = request.json
            print("Data received:", data)  # Log data yang diterima
            new_message = Message(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                phone=data['phone'],
                message=data['message']
            )
            session.add(new_message)
            session.commit()
            print("Data inserted successfully")
            return jsonify({'success': True, 'message': 'Message sent successfully!'})
        except Exception as e:
            print("Error:", e)  # Log pesan kesalahan
            session.rollback()
            return jsonify({'success': False, 'message': str(e)})
        finally:
            session.close()  # Pastikan sesi ditutup

    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
