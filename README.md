README – Authentication Token System (Flask + Firebase)
📌 Project Overview
This project is a secure token-based authentication system built using Python Flask and Firebase Firestore. It allows users to register, log in, receive a signed JWT token, and validate that token. The system uses bcrypt for password hashing and HS256 for JWT signing to ensure secure access control.
📁 Folder Structure

auth_token_system/
├── app.py                 # Main Flask app with all routes
├── utils.py               # Helper functions: save, verify, generate/validate token
├── firebase_key.json      # Firebase service account key (DO NOT share this publicly)
├── requirements.txt       # Python dependencies
├── templates/             # HTML frontend using Bootstrap
│   ├── register.html
│   ├── login.html
│   ├── dashboard.html
│   └── validate.html
└── static/                # (Optional) CSS/JS files

🚀 How to Run the App

1. Clone the project or download the ZIP.
2. Create and activate a virtual environment:
   - `python -m venv venv`
   - `source venv/bin/activate` (Linux/macOS) or `venv\Scripts\activate` (Windows)
3. Install dependencies:
   - `pip install -r requirements.txt`
4. Add your `firebase_key.json` into the root folder.
5. Run the Flask app:
   - `python app.py`
6. Open `http://127.0.0.1:5000` in your browser.

🔐 Features

- User Registration with bcrypt password hashing
- Login and session management using Flask
- JWT token generation with HS256 signing
- Token includes email, access level, system name, issue/expiry time
- Token validation and error handling (expired/invalid)
- Firebase Firestore used for user data storage

🛡️ Security Notes

- Passwords are hashed using bcrypt with salt.
- JWTs are signed using a shared secret (`supersecretkey` in this demo).
- Tokens expire after 15 minutes.
- All user data is securely stored in Firebase Firestore.

📚 Requirements

- Python 3.8+
- Flask
- bcrypt
- PyJWT
- firebase-admin


