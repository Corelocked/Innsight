# Innsight - Voice Order System

A modern hotel voice ordering and inquiry system that leverages natural language processing to handle guest requests. Innsight enables hotels to streamline room service orders, amenities requests, and guest inquiries through an intuitive voice-based interface with text fallback.

## 🎯 Features

- **Voice-Based Ordering**: Guest-friendly voice interface with speech-to-text transcription
- **Intent Recognition**: AI-powered natural language processing to understand guest requests
- **Multi-Intent Support**: 
  - Room Service Orders
  - Amenities Requests
  - Inquiries
  - Feedback and Complaints
  - Reservation Requests
  - Check-In/Check-Out Requests
- **User Authentication**: Firebase-based secure authentication for guests and staff
- **Text Alternative**: Full text input support for accessibility
- **Sentiment Analysis**: Detect guest satisfaction levels
- **User Preferences**: Track and remember guest preferences across sessions
- **Real-time Feedback**: Instant feedback mechanism for continuous improvement
- **Production-Ready**: Optimized for serverless deployment on Vercel

## 🏗️ Architecture

The system is built as a full-stack application with three main components:

```
Innsight/
├── voice-order-ui/          # React frontend application
├── api/                     # Vercel serverless API endpoints
├── voice-order-system/      # Voice processing & ML models
└── configuration files      # Deployment & environment setup
```

### Component Breakdown

**Frontend (React)**
- User authentication (login/signup)
- Real-time voice recording and transcription
- Text input fallback
- Order history and user preferences
- Feedback submission

**Backend API (Vercel Functions)**
- Request handling and validation
- Intent recognition and routing
- Response generation
- Feedback logging
- User preference management

**Voice Processing System**
- Speech-to-text transcription
- Intent classification
- Sentiment analysis
- User interaction logging

## 🛠️ Technology Stack

### Frontend
- **React 18.3.1**: UI framework
- **React Router 6.28**: Client-side routing
- **React Bootstrap 2.10.5**: UI components
- **Axios 1.7.7**: HTTP client
- **Firebase 11.0.1**: Authentication & real-time database

### Backend
- **Flask**: Lightweight web framework
- **Python 3.9+**: Runtime
- **pandas 2.2.3**: Data processing
- **NLTK 3.9.1**: Natural language processing
- **FuzzyWuzzy 0.18.0**: String matching for similarity

### Infrastructure
- **Vercel**: Serverless deployment platform
- **Firebase**: Authentication and database
- **SQLAlchemy**: ORM for database operations

## 📂 Project Structure

```
Innsight/
│
├── voice-order-ui/                 # React frontend
│   ├── public/
│   │   ├── index.html
│   │   └── manifest.json
│   ├── src/
│   │   ├── components/
│   │   │   ├── Login.js            # Authentication page
│   │   │   ├── Signup.js           # User registration
│   │   │   └── VoiceOrder.js       # Main voice ordering interface
│   │   ├── App.js                  # Root component with routing
│   │   ├── AuthContext.js          # Authentication context
│   │   ├── firebase.js             # Firebase configuration
│   │   ├── config.js               # App configuration
│   │   └── [styles & utilities]
│   ├── package.json
│   └── firebase.json               # Firebase project config
│
├── api/                            # Vercel serverless functions
│   ├── backend.py                  # Main API endpoint
│   ├── feedback.py                 # Feedback submission handler
│   ├── health.py                   # Health check endpoint
│   ├── voice_order.py              # Voice order processing
│   ├── response_utils.py           # Response generation utilities
│   ├── user_preferences.py         # User preference management
│   ├── inquiries.csv               # Intent-response mappings
│   └── __init__.py
│
├── voice-order-system/             # Voice processing & ML
│   ├── api.py                      # Flask API for voice processing
│   ├── intent_recognizer.py        # Intent classification engine
│   ├── sentiment_analysis.py       # Guest sentiment detection
│   ├── transcribe.py               # Speech-to-text handler
│   ├── user_log.py                 # User interaction logging
│   ├── models/
│   │   ├── inquiry_intent_model.joblib
│   │   ├── logistic_regression_model.joblib
│   │   ├── count_vectorizer.joblib
│   │   └── [training scripts]
│   ├── logs/
│   │   ├── feedback_logs.txt
│   │   └── interaction_logs.txt
│   ├── inquiries.csv
│   └── __pycache__/
│
├── Configuration Files
│   ├── requirements.txt             # Slim dependencies for Vercel
│   ├── requirements-full.txt        # All dependencies including ML
│   ├── vercel.json                 # Vercel deployment config
│   ├── firebase.json               # Firebase setup
│   │
│   └── Documentation
│       ├── DEPLOYMENT.md            # Deployment guide
│       ├── DEPLOYMENT_CHECKLIST.md  # Pre-deployment checklist
│       └── OPTIMIZATION.md          # Performance optimizations
```

## 🚀 Getting Started

### Prerequisites

- **Node.js 14+** and npm for the frontend
- **Python 3.9+** for the backend and voice processing
- **Firebase Project** (free tier available at [firebase.google.com](https://firebase.google.com))
- **Git** for version control

### Development Setup

#### 1. Clone the Repository
```bash
git clone <repository-url>
cd Innsight
```

#### 2. Set Up Firebase

1. Go to [Firebase Console](https://console.firebase.google.com)
2. Create a new project or use existing one
3. Enable Authentication (Email/Password method)
4. Copy your Firebase config
5. Create `voice-order-ui/.env.local`:
```env
REACT_APP_FIREBASE_API_KEY=your_api_key
REACT_APP_FIREBASE_AUTH_DOMAIN=your_auth_domain
REACT_APP_FIREBASE_PROJECT_ID=your_project_id
REACT_APP_FIREBASE_STORAGE_BUCKET=your_storage_bucket
REACT_APP_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
REACT_APP_FIREBASE_APP_ID=your_app_id
```

#### 3. Frontend Setup
```bash
cd voice-order-ui
npm install
npm start
```

The app will open at `http://localhost:3000`

#### 4. Backend Setup (Python)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 5. Voice Processing System (Optional for development)
```bash
cd voice-order-system
pip install speech_recognition pyaudio
python api.py
```

## 📖 Running the Application

### Development Mode

**Terminal 1 - Frontend**
```bash
cd voice-order-ui
npm start
# Runs at http://localhost:3000
```

**Terminal 2 - Backend** (if needed)
```bash
cd voice-order-system
python api.py
# Runs at http://localhost:5000
```

### Production Build
```bash
cd voice-order-ui
npm run build
# Creates optimized build in voice-order-ui/build/
```

## 🔌 API Endpoints

### Health Check
```
GET /api/health.py
Response: { "status": "ok" }
```

### Voice Order Processing
```
POST /api/voice_order.py
Body: {
  "transcription": "I would like to order a pizza",
  "user_id": "guest123"
}
Response: {
  "intent": "Room Service Order",
  "action": "order",
  "item": "pizza",
  "confidence": 0.95
}
```

### Feedback Submission
```
POST /api/feedback.py
Body: {
  "feedback": "Great service!",
  "rating": 5,
  "user_id": "guest123"
}
Response: { "status": "success" }
```

### User Preferences
```
GET /api/user_preferences.py?user_id=guest123
POST /api/user_preferences.py
Body: {
  "user_id": "guest123",
  "preferences": { "favorite_food": "pizza", "dietary_restrictions": [] }
}
```

## 🎓 Intent Recognition

The system can recognize and handle 7 different intent types:

| Intent | Examples | Bot Action |
|--------|----------|-----------|
| **Room Service Order** | "order pizza", "bring me ice cream" | Process food/item order |
| **Amenities Request** | "extra pillows", "more towels" | Fulfill amenities request |
| **Inquiry** | "what time is checkout?", "tell me about..." | Provide information |
| **Feedback/Complaint** | "not happy", "bad experience" | Log feedback, alert staff |
| **Reservation Request** | "book a table", "reserve a spot" | Create reservation |
| **Check-In/Out Request** | "early check-out", "late arrival" | Process request |
| **Negation** | "I don't want..." | Reverse action on positive intent |

## 📊 Data & Models

### CSV Data Files
- **inquiries.csv**: Maps inquiry patterns to responses
- **inquiries_old.csv**: Historical inquiry data

### Pre-trained ML Models
- **inquiry_intent_model.joblib**: Intent classification model
- **logistic_regression_model.joblib**: Sentiment analysis model
- **count_vectorizer.joblib**: Text vectorization

### Training Scripts
Located in `voice-order-system/models/`:
- `model_training.py`: Train intent classifier
- `inquiry_training.py`: Train inquiry-response mappings

## 🚀 Deployment

### Vercel Deployment (Recommended)

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions. Quick summary:

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod

# Set environment variables
vercel env add REACT_APP_FIREBASE_API_KEY production
```

**Key Optimizations Applied:**
- ✅ Slim Python dependencies (only 4 core packages)
- ✅ Function caching with `@lru_cache`
- ✅ Lazy loading of NLTK data
- ✅ CORS support for cross-origin requests
- ✅ Comprehensive input validation
- ✅ Error handling with user-friendly messages
- ✅ Client-side request timeouts (10s)

See [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) before deploying to production.

## 📈 Performance Optimizations

### Frontend Optimizations
- React hooks (`useCallback`, `useMemo`) prevent unnecessary re-renders
- Request timeouts prevent hanging connections
- Client-side input validation reduces server load
- Character counters provide UX feedback

### Backend Optimizations
- NLTK data lazy loading and caching
- `@lru_cache` decorators on frequently called functions
- Minimal dependencies to reduce cold start time
- Comprehensive error handling with graceful fallbacks

### Deployment Optimizations
- `.vercelignore` excludes unnecessary files
- 10-second function timeout for serverless
- Python 3.9 runtime specified for consistency

## 🔒 Security

- **Firebase Authentication**: Secure user authentication
- **CORS Headers**: Proper cross-origin resource sharing
- **Input Validation**: Length limits and sanitization
- **Error Messages**: User-friendly without exposing internals
- **Environment Variables**: Sensitive config stored securely

## 📝 Logging

The system maintains logs for:
- **Interaction Logs** (`voice-order-system/logs/interaction_logs.txt`): All guest interactions
- **Feedback Logs** (`voice-order-system/logs/feedback_logs.txt`): Guest feedback entries

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find process using port 3000 (frontend) or 5000 (backend)
netstat -ano | findstr :3000  # Windows
lsof -i :3000                  # macOS/Linux
```

### Firebase Connection Issues
- Verify Firebase credentials in `.env.local`
- Check Firebase project is active
- Ensure authentication methods are enabled

### Python Dependencies
```bash
# Update pip and install requirements
python -m pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### NLTK Data Missing
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

## 📚 Documentation

- [DEPLOYMENT.md](DEPLOYMENT.md) - Full deployment guide for Vercel
- [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) - Pre-deployment validation
- [OPTIMIZATION.md](OPTIMIZATION.md) - Performance optimization details

## 🤝 Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes and commit: `git commit -m 'Add feature'`
3. Push to branch: `git push origin feature/your-feature`
4. Submit a pull request

## 📄 License

This project is proprietary. All rights reserved.

## 👥 Support

For support, please contact the development team or submit an issue in the project repository.

---

**Last Updated**: March 2026  
**Current Version**: 0.1.0
