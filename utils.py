import bcrypt
import jwt
import datetime
import firebase_admin
from firebase_admin import credentials, firestore

# 🔐 JWT Configuration
JWT_SECRET = 'supersecretkey'  # Change this to a secure random string in production
JWT_ALGORITHM = 'HS256'

# 🔧 Initialize Firebase Admin SDK
if not firebase_admin._apps:
    cred = credentials.Certificate('firebase_key.json')  # Your downloaded service account key
    firebase_admin.initialize_app(cred)

# 🔗 Connect to Firestore
db = firestore.client()
users_ref = db.collection('users')


# ✅ Save New User (Registration)
def save_user(email, password):
    user_doc = users_ref.document(email).get()
    if user_doc.exists:
        return False  # User already exists

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    users_ref.document(email).set({
        'password': hashed,
        'access': 'user'  # Default access level
    })
    return True


# ✅ Verify User Login
def verify_user(email, password):
    user_doc = users_ref.document(email).get()
    if not user_doc.exists:
        return False

    stored_hash = user_doc.to_dict()['password'].encode('utf-8')
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash)


# 🔎 Load User for Token Generation
def load_user(email):
    user_doc = users_ref.document(email).get()
    return user_doc.to_dict() if user_doc.exists else None


# 🔐 Generate Token (JWT)
def generate_token(email):
    user_data = load_user(email)
    if not user_data:
        return None

    payload = {
        'email': email,
        'access': user_data['access'],
        'system': 'FlaskAuthApp',
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


# 🔍 Validate Token
def validate_token(token):
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return f"✅ Token is valid.\nUser: {decoded['email']}\nAccess: {decoded['access']}\nSystem: {decoded['system']}\nExpires: {datetime.datetime.utcfromtimestamp(decoded['exp'])}"
    except jwt.ExpiredSignatureError:
        return "❌ Token has expired."
    except jwt.InvalidTokenError:
        return "❌ Invalid token (signature broken or tampered)."
