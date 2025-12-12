"""
Installation and Setup Verification Script
Run this to test if all dependencies are installed correctly.
"""

import sys

def check_imports():
    """Check if all required packages are installed"""
    print("=" * 60)
    print("Future-Self Recommendation System - Setup Verification")
    print("=" * 60)
    print()
    
    required_packages = [
        ('fastapi', 'FastAPI'),
        ('uvicorn', 'Uvicorn'),
        ('pandas', 'Pandas'),
        ('numpy', 'NumPy'),
        ('sklearn', 'Scikit-Learn'),
        ('streamlit', 'Streamlit'),
        ('requests', 'Requests'),
        ('plotly', 'Plotly'),
        ('pydantic', 'Pydantic'),
    ]
    
    all_installed = True
    
    for package_name, display_name in required_packages:
        try:
            __import__(package_name)
            print(f"✅ {display_name:20} - Installed")
        except ImportError:
            print(f"❌ {display_name:20} - NOT INSTALLED")
            all_installed = False
    
    print()
    print("=" * 60)
    
    if all_installed:
        print("✅ All dependencies are installed correctly!")
        print()
        print("Next Steps:")
        print("1. Start the backend:  python backend/app.py")
        print("2. Start the frontend: streamlit run frontend/streamlit_app.py")
        print("3. Open browser at:    http://localhost:8501")
        print()
        return True
    else:
        print("❌ Some dependencies are missing!")
        print()
        print("Please run: pip install -r requirements.txt")
        print()
        return False


def test_recommender_engine():
    """Test the recommendation engine"""
    print("Testing Recommendation Engine...")
    print("-" * 60)
    
    try:
        sys.path.append('backend')
        from recommender import FutureSelfEngine
        
        engine = FutureSelfEngine()
        result = engine.recommend("I want to become a CTO", top_k=3)
        
        print(f"✅ Engine initialized successfully!")
        print(f"✅ Total content items: {len(engine.content_metadata)}")
        print(f"✅ Skill dimensions: {len(engine.skill_dimensions)}")
        print()
        print(f"Test Query: '{result['user_goal']}'")
        print(f"Goal Vector: {result['goal_vector']}")
        print()
        print(f"Top 3 Recommendations:")
        for i, rec in enumerate(result['recommendations'], 1):
            print(f"{i}. {rec['title']} (Match: {rec['match_score']:.1%})")
        
        print()
        print("=" * 60)
        print("✅ Recommendation engine is working perfectly!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"❌ Error testing engine: {str(e)}")
        return False


def main():
    """Main verification function"""
    print()
    
    # Check imports
    if not check_imports():
        sys.exit(1)
    
    print()
    
    # Test engine
    if not test_recommender_engine():
        sys.exit(1)
    
    print()
    print("🎉 Everything is ready! You can now run the application.")
    print()


if __name__ == "__main__":
    main()
