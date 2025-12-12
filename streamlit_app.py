"""
Streamlit Frontend for Future-Self Recommendation System (Standalone Version)
Provides interactive UI for goal input, visualization, and recommendations.
Works without external API - includes recommender engine directly.
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, List
import sys
from pathlib import Path

# Add backend directory to path to import recommender
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from recommender import FutureSelfEngine

# Page configuration
st.set_page_config(
    page_title="Future-Self Recommender",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling with improved contrast
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1E88E5;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #333333;
        margin-bottom: 2rem;
    }
    .recommendation-card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #ffffff;
        margin-bottom: 1rem;
        border-left: 4px solid #1E88E5;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .recommendation-card h3 {
        color: #1E88E5;
        margin-bottom: 0.5rem;
    }
    .recommendation-card p {
        color: #333333;
        line-height: 1.6;
    }
    .recommendation-card strong {
        color: #000000;
    }
    .recommendation-card a {
        color: #1E88E5;
        text-decoration: none;
        font-weight: 600;
    }
    .recommendation-card a:hover {
        color: #0D47A1;
        text-decoration: underline;
    }
    .match-score {
        font-size: 1.5rem;
        font-weight: bold;
        color: #4CAF50;
    }
    }
    </style>
""", unsafe_allow_html=True)


# Initialize recommendation engine (cached for performance)
@st.cache_resource
def load_engine():
    """Load and cache the recommendation engine"""
    return FutureSelfEngine()


def create_radar_chart(goal_vector: List[float], content_vector: List[float], 
                       skill_dimensions: List[str], content_title: str) -> go.Figure:
    """
    Creates a radar chart comparing user's goal vector with recommended content vector.
    
    Args:
        goal_vector: User's future-self goal vector
        content_vector: Recommended content's skill vector
        skill_dimensions: List of skill dimension names
        content_title: Title of the recommended content
    
    Returns:
        Plotly figure object
    """
    fig = go.Figure()
    
    # Add goal vector trace
    fig.add_trace(go.Scatterpolar(
        r=goal_vector,
        theta=skill_dimensions,
        fill='toself',
        name='Your Goal',
        line=dict(color='#1E88E5', width=2),
        fillcolor='rgba(30, 136, 229, 0.3)'
    ))
    
    # Add content vector trace
    fig.add_trace(go.Scatterpolar(
        r=content_vector,
        theta=skill_dimensions,
        fill='toself',
        name=f'Content: {content_title}',
        line=dict(color='#4CAF50', width=2),
        fillcolor='rgba(76, 175, 80, 0.3)'
    ))
    
    # Update layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                showticklabels=True,
                ticks='outside'
            )
        ),
        showlegend=True,
        title={
            'text': f"Skill Match Analysis",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': '#333'}
        },
        height=500,
        margin=dict(l=80, r=80, t=100, b=80)
    )
    
    return fig


def display_recommendation_card(rec: Dict, index: int):
    """
    Displays a single recommendation as a styled card.
    
    Args:
        rec: Recommendation dictionary
        index: Index number of the recommendation
    """
    st.markdown(f"""
        <div class="recommendation-card">
            <h3>#{index}. {rec['title']}</h3>
            <p><strong>Type:</strong> {rec['type']} | <strong>Match Score:</strong> 
            <span class="match-score">{rec['match_score']:.1%}</span></p>
            <p>{rec['description']}</p>
            <p><a href="{rec['url']}" target="_blank">🔗 View Content</a></p>
        </div>
    """, unsafe_allow_html=True)


def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown('<div class="main-header">🎯 Future-Self Recommendation System</div>', 
                unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Discover content aligned with who you want to become, not who you were.</div>', 
                unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("About")
        st.info("""
        This system recommends content based on your **Future Identity**, not your past behavior.
        
        **How it works:**
        1. Enter your future-self goal
        2. System converts it to a skill vector
        3. Find content matching your aspirations
        
        **Skill Dimensions:**
        - Coding
        - Data Science
        - Leadership
        - Communication
        - Fitness
        - Mindfulness
        - Entrepreneurship
        """)
        
        st.header("Examples")
        st.code("I want to become a CTO")
        st.code("I want to be a data scientist and entrepreneur")
        st.code("I want to be fit and mindful")
        
        st.divider()
        st.success("✅ Engine Ready")
    
    # Load recommendation engine
    try:
        engine = load_engine()
    except Exception as e:
        st.error(f"❌ Failed to load recommendation engine: {str(e)}")
        st.stop()
    
    # Main content area
    st.divider()
    
    # Input section
    st.subheader("🌟 Who Do You Want to Become?")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_goal = st.text_input(
            label="Enter your future-self goal:",
            placeholder="e.g., I want to become a CTO, startup founder, or ML engineer...",
            label_visibility="collapsed"
        )
    
    with col2:
        top_k = st.number_input(
            "Top K",
            min_value=1,
            max_value=10,
            value=5,
            help="Number of recommendations to show"
        )
    
    generate_button = st.button("🚀 Generate Recommendations", type="primary", use_container_width=True)
    
    # Process recommendations
    if generate_button:
        if not user_goal or user_goal.strip() == "":
            st.warning("⚠️ Please enter a goal to get recommendations.")
        else:
            with st.spinner("🔍 Analyzing your future-self and finding perfect matches..."):
                try:
                    # Generate recommendations using local engine
                    result = engine.recommend(user_goal, top_k=top_k)
                    
                    # Store in session state
                    st.session_state['result'] = result
                    st.success("✅ Recommendations generated successfully!")
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # Display results
    if 'result' in st.session_state:
        result = st.session_state['result']
        
        st.divider()
        st.header("📊 Your Future-Self Profile")
        
        # Display goal vector
        goal_vector = result['goal_vector']
        skill_dimensions = result['skill_dimensions']
        
        # Create a bar chart for goal vector
        goal_df = pd.DataFrame({
            'Skill': skill_dimensions,
            'Strength': goal_vector
        })
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Goal Vector Breakdown")
            st.bar_chart(goal_df.set_index('Skill'), height=300)
        
        with col2:
            st.subheader("Vector Values")
            for skill, value in zip(skill_dimensions, goal_vector):
                st.metric(label=skill, value=f"{value:.3f}")
        
        # Recommendations section
        st.divider()
        st.header("🎓 Recommended Content for You")
        
        recommendations = result['recommendations']
        
        if not recommendations:
            st.warning("No recommendations found. Try a different goal.")
        else:
            # Create tabs for different views
            tab1, tab2 = st.tabs(["📋 List View", "📈 Visual Analysis"])
            
            with tab1:
                # Display all recommendations as cards
                for i, rec in enumerate(recommendations, 1):
                    display_recommendation_card(rec, i)
            
            with tab2:
                # Radar chart comparison
                st.subheader("Compare Your Goal with Top Recommendations")
                
                # Select which recommendation to compare
                rec_titles = [f"{i+1}. {rec['title']}" for i, rec in enumerate(recommendations)]
                selected_rec_index = st.selectbox(
                    "Select content to compare:",
                    range(len(rec_titles)),
                    format_func=lambda x: rec_titles[x]
                )
                
                selected_rec = recommendations[selected_rec_index]
                
                # Create and display radar chart
                radar_fig = create_radar_chart(
                    goal_vector=goal_vector,
                    content_vector=selected_rec['content_vector'],
                    skill_dimensions=skill_dimensions,
                    content_title=selected_rec['title']
                )
                
                st.plotly_chart(radar_fig, use_container_width=True)
                
                # Display match details
                st.info(f"""
                **Match Score:** {selected_rec['match_score']:.1%}
                
                **{selected_rec['title']}** ({selected_rec['type']})
                
                {selected_rec['description']}
                
                [🔗 View Content]({selected_rec['url']})
                """)
                
                # Show all radar charts in a grid
                st.divider()
                st.subheader("All Recommendations - Skill Match")
                
                cols = st.columns(2)
                for i, rec in enumerate(recommendations[:6]):  # Show max 6
                    with cols[i % 2]:
                        mini_radar = create_radar_chart(
                            goal_vector=goal_vector,
                            content_vector=rec['content_vector'],
                            skill_dimensions=skill_dimensions,
                            content_title=rec['title'][:30] + "..." if len(rec['title']) > 30 else rec['title']
                        )
                        mini_radar.update_layout(height=350)
                        st.plotly_chart(mini_radar, use_container_width=True)
        
        # Download results
        st.divider()
        if st.button("📥 Download Recommendations as JSON"):
            st.download_button(
                label="Download JSON",
                data=str(result),
                file_name="future_self_recommendations.json",
                mime="application/json"
            )


if __name__ == "__main__":
    main()
