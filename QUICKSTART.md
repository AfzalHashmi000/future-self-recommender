# Quick Start Guide 🚀

## Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

## Step 2: Run the Application

### Option A: Using Batch Files (Windows - Easiest)
1. Double-click `start_backend.bat` to start the API server
2. Double-click `start_frontend.bat` to start the UI (in a new window)

### Option B: Using Command Line
**Terminal 1 (Backend):**
```bash
cd backend
python app.py
```

**Terminal 2 (Frontend):**
```bash
cd frontend
streamlit run streamlit_app.py
```

## Step 3: Access the Application
- **Frontend UI:** http://localhost:8501 (opens automatically)
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

## Step 4: Use the System
1. Enter your future-self goal (e.g., "I want to become a CTO")
2. Click "Generate Recommendations"
3. Explore your personalized content matches!

## Example Goals to Try
- "I want to become a CTO"
- "I want to be a data scientist"
- "I want to start a successful startup"
- "I want to master machine learning and leadership"
- "I want to be fit, mindful, and entrepreneurial"

## Troubleshooting
- **"Module not found"** → Run: `pip install -r requirements.txt`
- **"Cannot connect to API"** → Make sure backend is running (step 2)
- **Port already in use** → Close other applications using port 8000/8501

---
**That's it! You're ready to discover your future-self! 🎯**
