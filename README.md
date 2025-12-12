# Future-Self Recommendation System 🎯

A goal-driven content recommendation system that recommends content based on your **Future Identity**, not your past behavior.

## 🌟 Core Concept

Unlike traditional recommenders (e.g., "You watched cat videos, here are more cat videos"), this system:
1. Takes your future-self goal (e.g., "I want to become a CTO")
2. Converts it into a 7-dimensional skill vector
3. Finds content (Books, Videos, Courses) matching that vector using Cosine Similarity

## 🏗️ Project Structure

```
future_self_project/
│── requirements.txt          # Python dependencies
│── README.md                 # This file
│── backend/
│   ├── app.py               # FastAPI REST API server
│   ├── recommender.py       # ML engine (data generation + recommendations)
│── frontend/
│   ├── streamlit_app.py     # Streamlit UI
```

## 🔧 Tech Stack

- **Language:** Python 3.10+
- **Backend:** FastAPI (REST API)
- **Frontend:** Streamlit (Interactive UI)
- **ML:** Scikit-Learn (Cosine Similarity), Pandas, NumPy
- **Visualization:** Plotly (Radar Charts)
- **Data:** Auto-generated dummy dataset (18 items)

## 📊 Skill Dimensions

The system evaluates content across 7 dimensions:
1. **Coding** - Programming and software development
2. **Data Science** - ML, AI, analytics
3. **Leadership** - Management and executive skills
4. **Communication** - Public speaking, writing, influence
5. **Fitness** - Physical health and exercise
6. **Mindfulness** - Meditation, mental wellness
7. **Entrepreneurship** - Startups, business creation

## 🚀 Installation & Setup

### Step 1: Install Dependencies

```bash
# Navigate to project directory
cd future_self_project

# Install all required packages
pip install -r requirements.txt
```

### Step 2: Start the Backend API

```bash
# Navigate to backend folder
cd backend

# Start FastAPI server
python app.py
```

The API will be available at:
- Main API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

### Step 3: Start the Frontend UI

Open a **new terminal** window:

```bash
# Navigate to frontend folder
cd future_self_project/frontend

# Start Streamlit app
streamlit run streamlit_app.py
```

The UI will open automatically in your browser at http://localhost:8501

## 📖 Usage Guide

1. **Enter Your Goal:** Type your future-self aspiration (e.g., "I want to become a data scientist and entrepreneur")
2. **Generate Recommendations:** Click the button to get personalized content
3. **Explore Results:**
   - View list of recommended books, videos, and courses
   - See match scores (0-100%)
   - Compare skill profiles with radar charts
4. **Take Action:** Click on content links to start learning

## 🎯 Example Goals

Try these example inputs:
- "I want to become a CTO"
- "I want to be a machine learning engineer"
- "I want to start a successful startup"
- "I want to be fit and mindful"
- "I want to master public speaking and leadership"

## 🔌 API Endpoints

### POST /recommend_content
Generate recommendations based on user goal.

**Request:**
```json
{
  "goal": "I want to become a CTO",
  "top_k": 5
}
```

**Response:**
```json
{
  "user_goal": "I want to become a CTO",
  "goal_vector": [0.5, 0.2, 0.94, 0.8, 0.0, 0.2, 0.6],
  "skill_dimensions": ["Coding", "Data Science", "Leadership", ...],
  "recommendations": [...]
}
```

### GET /health
Check API health status.

### GET /stats
Get system statistics (total content, dimensions, types).

### GET /content/all
Retrieve all available content items.

### GET /skills
Get all skill dimensions.

## 🧪 Testing the System

### Test the Backend API

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test recommendation endpoint
curl -X POST http://localhost:8000/recommend_content \
  -H "Content-Type: application/json" \
  -d '{"goal": "I want to become a CTO"}'
```

### Test the Recommender Engine Directly

```bash
cd backend
python recommender.py
```

## 🎨 Features

### Frontend (Streamlit)
- ✅ Clean, intuitive UI
- ✅ Real-time API connection status
- ✅ Interactive radar charts (Plotly)
- ✅ Skill vector visualization
- ✅ Multiple viewing modes (List/Visual)
- ✅ Downloadable results
- ✅ Example goals in sidebar

### Backend (FastAPI)
- ✅ RESTful API with auto-generated docs
- ✅ Input validation (Pydantic)
- ✅ CORS support
- ✅ Error handling
- ✅ Health checks
- ✅ Multiple utility endpoints

### ML Engine
- ✅ Keyword-based goal parsing
- ✅ Vector normalization
- ✅ Cosine similarity ranking
- ✅ 18 pre-loaded content items
- ✅ Extensible architecture

## 🔮 How It Works

### 1. Goal → Vector Conversion
```python
"I want to become a CTO" 
→ Keywords: ['cto', 'become']
→ Maps to: Leadership (0.94), Communication (0.8), Coding (0.5)
→ Normalized Vector: [0.5, 0.2, 0.94, 0.8, 0.0, 0.2, 0.6]
```

### 2. Similarity Calculation
```python
cosine_similarity(goal_vector, content_vectors)
→ Scores: [0.89, 0.76, 0.68, ...]
```

### 3. Top-K Ranking
```python
top_5 = sorted_by_score[:5]
→ Returns: ["The Manager's Path", "Leadership Principles", ...]
```

## 📝 Customization

### Add More Content
Edit `backend/recommender.py` → `DataLoader._generate_content()`:

```python
{
    'Title': 'Your Content Title',
    'Type': 'Book',  # or 'Video', 'Course'
    'Description': 'Description here',
    'URL': 'https://example.com',
    'Coding': 0.8,
    'Data Science': 0.5,
    # ... add all 7 dimensions
}
```

### Add More Keywords
Edit `backend/recommender.py` → `FutureSelfEngine.keyword_mapping`:

```python
'newkeyword': 'Leadership',  # Map to dimension
```

### Change Skill Dimensions
Edit `backend/recommender.py` → `DataLoader.skill_dimensions`

## 🐛 Troubleshooting

### "Cannot connect to API"
- Ensure backend is running on port 8000
- Check firewall settings
- Verify API health: http://localhost:8000/health

### "Module not found"
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.10+)

### Port already in use
- Change port in `backend/app.py`: `uvicorn.run(..., port=8001)`
- Update API_URL in `frontend/streamlit_app.py`

## 📚 Dependencies

- fastapi==0.104.1 - Web framework
- uvicorn==0.24.0 - ASGI server
- pandas==2.1.3 - Data manipulation
- numpy==1.26.2 - Numerical computing
- scikit-learn==1.3.2 - ML algorithms
- streamlit==1.28.2 - UI framework
- requests==2.31.0 - HTTP client
- plotly==5.18.0 - Interactive charts
- pydantic==2.5.0 - Data validation

## 🚀 Future Enhancements

- [ ] User authentication and profiles
- [ ] Save/load user goals
- [ ] Real content database integration
- [ ] Collaborative filtering
- [ ] A/B testing framework
- [ ] Mobile app version
- [ ] Social sharing features

## 📄 License

MIT License - Feel free to use this project for learning and development.

## 👨‍💻 Author

Built as a demonstration of goal-driven recommendation systems using modern ML and web technologies.

---

**Ready to discover your future-self? Start the servers and begin your journey! 🚀**
