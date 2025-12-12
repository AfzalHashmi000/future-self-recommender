# Deployment Guide for Streamlit Community Cloud

This guide will help you deploy the Future-Self Recommendation System to Streamlit Community Cloud.

## Prerequisites

1. A GitHub account
2. Git installed on your computer
3. The project code (already initialized with `git init`)

## Step-by-Step Deployment

### Step 1: Create a GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click the **+** button in the top right corner
3. Select **New repository**
4. Repository settings:
   - **Name:** `future-self-recommender` (or your preferred name)
   - **Description:** "Goal-driven content recommendation system using ML"
   - **Visibility:** Public (required for free Streamlit deployment)
   - **Do NOT** initialize with README, .gitignore, or license (we already have these)
5. Click **Create repository**

### Step 2: Connect Local Repository to GitHub

Open your terminal/PowerShell in the project directory and run:

```bash
# Add all files to git
git add .

# Commit the files
git commit -m "Initial commit: Future-Self Recommendation System"

# Add the remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/future-self-recommender.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Example with actual username:**
```bash
git remote add origin https://github.com/johndoe/future-self-recommender.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy to Streamlit Community Cloud

1. Go to [Streamlit Community Cloud](https://streamlit.io/cloud)
2. Sign in with your GitHub account
3. Click **New app**
4. Configure the deployment:
   - **Repository:** Select `YOUR_USERNAME/future-self-recommender`
   - **Branch:** `main`
   - **Main file path:** `streamlit_app.py`
5. Click **Deploy!**

### Step 4: Wait for Deployment

- Streamlit will install dependencies from `requirements.txt`
- This usually takes 2-5 minutes
- You'll see build logs in real-time
- Once complete, you'll get a public URL like: `https://your-app-name.streamlit.app`

## Project Structure for Deployment

```
future_self_project/
├── streamlit_app.py          # Main entry point (standalone version)
├── requirements.txt           # Python dependencies
├── .streamlit/
│   └── config.toml           # Streamlit configuration
├── backend/
│   ├── recommender.py        # ML recommendation engine
│   └── __init__.py
├── README.md                  # Documentation
└── .gitignore                # Git ignore rules
```

## Important Notes

### Main Entry Point
- The file `streamlit_app.py` in the **root directory** is the entry point
- This is a **standalone version** that doesn't require the FastAPI backend
- It imports the recommender engine directly from the `backend/` folder

### Dependencies
- Only essential packages are in `requirements.txt`
- Streamlit Cloud handles the installation automatically
- No FastAPI/Uvicorn needed for the cloud version

### Free Tier Limits
- **Resources:** 1 CPU, 800MB RAM
- **Apps:** Up to 3 public apps
- **Sleep:** Apps sleep after 7 days of inactivity
- **Perfect for:** Personal projects and demos

## Troubleshooting

### Build Fails
- Check `requirements.txt` for version conflicts
- Ensure all files are committed and pushed
- Check build logs in Streamlit Cloud dashboard

### Import Errors
- Make sure `backend/recommender.py` is in the repository
- Verify `backend/__init__.py` exists
- Check file paths are correct

### Memory Issues
- Streamlit Cloud has limited RAM (800MB)
- The current app should work fine within limits
- If issues occur, reduce the number of content items in `recommender.py`

## Updating Your Deployed App

After making changes locally:

```bash
# Stage changes
git add .

# Commit changes
git commit -m "Description of changes"

# Push to GitHub
git push origin main
```

Streamlit will automatically detect the changes and redeploy (usually within 1-2 minutes).

## Testing Locally Before Deployment

```bash
# Run the standalone version
streamlit run streamlit_app.py
```

This will run the same code that will be deployed to Streamlit Cloud.

## Environment Variables (Optional)

If you need environment variables (API keys, etc.):

1. In Streamlit Cloud dashboard, go to your app
2. Click **Settings** → **Secrets**
3. Add secrets in TOML format:
   ```toml
   API_KEY = "your-secret-key"
   ```
4. Access in code: `st.secrets["API_KEY"]`

## Custom Domain (Optional)

Free tier includes:
- Default URL: `https://your-app.streamlit.app`
- Custom domains available on paid plans

## Support

- [Streamlit Docs](https://docs.streamlit.io)
- [Community Forum](https://discuss.streamlit.io)
- [GitHub Issues](https://github.com/streamlit/streamlit/issues)

---

**Ready to deploy? Follow the steps above and share your app with the world! 🚀**
