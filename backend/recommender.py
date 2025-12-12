"""
Future-Self Recommendation Engine
Generates dummy content data and performs cosine similarity-based recommendations.
"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple


class DataLoader:
    """
    Auto-generates a dummy dataset of content (Books, Videos, Courses)
    with 7-dimensional skill vectors.
    """
    
    def __init__(self):
        self.skill_dimensions = [
            'Coding', 
            'Data Science', 
            'Leadership', 
            'Communication', 
            'Fitness', 
            'Mindfulness', 
            'Entrepreneurship'
        ]
        self.content_data = self._generate_content()
    
    def _generate_content(self) -> pd.DataFrame:
        """
        Generates at least 15 content items with skill vectors.
        
        Returns:
            DataFrame with columns: Title, Type, Description, URL, and skill dimensions
        """
        content_items = [
            {
                'Title': 'The Lean Startup',
                'Type': 'Book',
                'Description': 'Build a successful startup using validated learning and rapid experimentation.',
                'URL': 'https://example.com/lean-startup',
                'Coding': 0.2,
                'Data Science': 0.3,
                'Leadership': 0.7,
                'Communication': 0.6,
                'Fitness': 0.0,
                'Mindfulness': 0.2,
                'Entrepreneurship': 0.95
            },
            {
                'Title': 'Clean Code: A Handbook of Agile Software Craftsmanship',
                'Type': 'Book',
                'Description': 'Learn how to write clean, maintainable code that stands the test of time.',
                'URL': 'https://example.com/clean-code',
                'Coding': 0.95,
                'Data Science': 0.3,
                'Leadership': 0.4,
                'Communication': 0.5,
                'Fitness': 0.0,
                'Mindfulness': 0.1,
                'Entrepreneurship': 0.2
            },
            {
                'Title': 'Deep Learning Specialization',
                'Type': 'Course',
                'Description': 'Master deep learning fundamentals and build neural networks from scratch.',
                'URL': 'https://example.com/deep-learning',
                'Coding': 0.8,
                'Data Science': 0.98,
                'Leadership': 0.2,
                'Communication': 0.3,
                'Fitness': 0.0,
                'Mindfulness': 0.1,
                'Entrepreneurship': 0.2
            },
            {
                'Title': 'How to Win Friends and Influence People',
                'Type': 'Book',
                'Description': 'Classic guide to improving interpersonal skills and building relationships.',
                'URL': 'https://example.com/win-friends',
                'Coding': 0.0,
                'Data Science': 0.0,
                'Leadership': 0.8,
                'Communication': 0.95,
                'Fitness': 0.0,
                'Mindfulness': 0.3,
                'Entrepreneurship': 0.5
            },
            {
                'Title': 'Python for Data Analysis',
                'Type': 'Book',
                'Description': 'Comprehensive guide to data manipulation and analysis with pandas.',
                'URL': 'https://example.com/python-data',
                'Coding': 0.85,
                'Data Science': 0.9,
                'Leadership': 0.1,
                'Communication': 0.2,
                'Fitness': 0.0,
                'Mindfulness': 0.0,
                'Entrepreneurship': 0.1
            },
            {
                'Title': 'Atomic Habits',
                'Type': 'Book',
                'Description': 'Build good habits and break bad ones using tiny changes.',
                'URL': 'https://example.com/atomic-habits',
                'Coding': 0.0,
                'Data Science': 0.1,
                'Leadership': 0.5,
                'Communication': 0.4,
                'Fitness': 0.6,
                'Mindfulness': 0.85,
                'Entrepreneurship': 0.4
            },
            {
                'Title': 'Full-Stack Web Development Bootcamp',
                'Type': 'Course',
                'Description': 'Learn React, Node.js, and MongoDB to build complete web applications.',
                'URL': 'https://example.com/fullstack',
                'Coding': 0.92,
                'Data Science': 0.2,
                'Leadership': 0.3,
                'Communication': 0.4,
                'Fitness': 0.0,
                'Mindfulness': 0.1,
                'Entrepreneurship': 0.3
            },
            {
                'Title': 'The 4-Hour Work Week',
                'Type': 'Book',
                'Description': 'Escape the 9-5, live anywhere, and join the new rich.',
                'URL': 'https://example.com/4-hour',
                'Coding': 0.1,
                'Data Science': 0.0,
                'Leadership': 0.6,
                'Communication': 0.5,
                'Fitness': 0.3,
                'Mindfulness': 0.4,
                'Entrepreneurship': 0.88
            },
            {
                'Title': 'Mindfulness Meditation for Beginners',
                'Type': 'Video',
                'Description': 'Introduction to mindfulness practice for stress reduction and focus.',
                'URL': 'https://example.com/mindfulness-video',
                'Coding': 0.0,
                'Data Science': 0.0,
                'Leadership': 0.2,
                'Communication': 0.3,
                'Fitness': 0.4,
                'Mindfulness': 0.95,
                'Entrepreneurship': 0.1
            },
            {
                'Title': 'High-Intensity Interval Training (HIIT) Masterclass',
                'Type': 'Course',
                'Description': 'Transform your body with science-backed HIIT workouts.',
                'URL': 'https://example.com/hiit',
                'Coding': 0.0,
                'Data Science': 0.0,
                'Leadership': 0.3,
                'Communication': 0.2,
                'Fitness': 0.97,
                'Mindfulness': 0.4,
                'Entrepreneurship': 0.1
            },
            {
                'Title': 'Leadership Principles from Naval Ravikant',
                'Type': 'Video',
                'Description': 'Timeless wisdom on wealth creation and personal freedom.',
                'URL': 'https://example.com/naval',
                'Coding': 0.2,
                'Data Science': 0.1,
                'Leadership': 0.92,
                'Communication': 0.7,
                'Fitness': 0.2,
                'Mindfulness': 0.6,
                'Entrepreneurship': 0.85
            },
            {
                'Title': 'Machine Learning Engineering',
                'Type': 'Book',
                'Description': 'Deploy ML models to production with best practices and real-world examples.',
                'URL': 'https://example.com/ml-engineering',
                'Coding': 0.88,
                'Data Science': 0.95,
                'Leadership': 0.4,
                'Communication': 0.5,
                'Fitness': 0.0,
                'Mindfulness': 0.1,
                'Entrepreneurship': 0.3
            },
            {
                'Title': 'Public Speaking Mastery',
                'Type': 'Course',
                'Description': 'Overcome stage fright and deliver compelling presentations.',
                'URL': 'https://example.com/public-speaking',
                'Coding': 0.0,
                'Data Science': 0.0,
                'Leadership': 0.7,
                'Communication': 0.96,
                'Fitness': 0.1,
                'Mindfulness': 0.3,
                'Entrepreneurship': 0.5
            },
            {
                'Title': 'Zero to One: Notes on Startups',
                'Type': 'Book',
                'Description': 'Build the future by creating innovative companies that matter.',
                'URL': 'https://example.com/zero-to-one',
                'Coding': 0.2,
                'Data Science': 0.1,
                'Leadership': 0.85,
                'Communication': 0.6,
                'Fitness': 0.0,
                'Mindfulness': 0.2,
                'Entrepreneurship': 0.93
            },
            {
                'Title': 'System Design Interview Prep',
                'Type': 'Course',
                'Description': 'Ace technical interviews at FAANG companies with scalable architectures.',
                'URL': 'https://example.com/system-design',
                'Coding': 0.9,
                'Data Science': 0.4,
                'Leadership': 0.5,
                'Communication': 0.7,
                'Fitness': 0.0,
                'Mindfulness': 0.1,
                'Entrepreneurship': 0.2
            },
            {
                'Title': 'The Yoga Sutras of Patanjali',
                'Type': 'Book',
                'Description': 'Ancient wisdom on meditation, consciousness, and self-realization.',
                'URL': 'https://example.com/yoga-sutras',
                'Coding': 0.0,
                'Data Science': 0.0,
                'Leadership': 0.3,
                'Communication': 0.2,
                'Fitness': 0.7,
                'Mindfulness': 0.98,
                'Entrepreneurship': 0.0
            },
            {
                'Title': 'Building a Second Brain',
                'Type': 'Course',
                'Description': 'Organize your digital life and amplify your creative productivity.',
                'URL': 'https://example.com/second-brain',
                'Coding': 0.3,
                'Data Science': 0.2,
                'Leadership': 0.6,
                'Communication': 0.5,
                'Fitness': 0.1,
                'Mindfulness': 0.4,
                'Entrepreneurship': 0.7
            },
            {
                'Title': 'The Manager\'s Path',
                'Type': 'Book',
                'Description': 'Navigate your career from tech lead to CTO with practical advice.',
                'URL': 'https://example.com/managers-path',
                'Coding': 0.5,
                'Data Science': 0.2,
                'Leadership': 0.94,
                'Communication': 0.8,
                'Fitness': 0.0,
                'Mindfulness': 0.2,
                'Entrepreneurship': 0.6
            }
        ]
        
        return pd.DataFrame(content_items)
    
    def get_content_vectors(self) -> np.ndarray:
        """
        Extracts the skill vectors from the content data.
        
        Returns:
            Numpy array of shape (n_items, 7) with skill vectors
        """
        return self.content_data[self.skill_dimensions].values
    
    def get_content_metadata(self) -> pd.DataFrame:
        """
        Returns the metadata columns (Title, Type, Description, URL).
        
        Returns:
            DataFrame with metadata columns
        """
        return self.content_data[['Title', 'Type', 'Description', 'URL']]


class FutureSelfEngine:
    """
    Core recommendation engine that converts user goals into vectors
    and finds similar content using cosine similarity.
    """
    
    def __init__(self):
        self.data_loader = DataLoader()
        self.skill_dimensions = self.data_loader.skill_dimensions
        self.content_vectors = self.data_loader.get_content_vectors()
        self.content_metadata = self.data_loader.get_content_metadata()
        
        # Keyword mapping for goal-to-vector conversion
        self.keyword_mapping = {
            # Coding keywords
            'code': 'Coding',
            'coding': 'Coding',
            'programmer': 'Coding',
            'developer': 'Coding',
            'software': 'Coding',
            'engineer': 'Coding',
            'python': 'Coding',
            'java': 'Coding',
            'javascript': 'Coding',
            'fullstack': 'Coding',
            'backend': 'Coding',
            'frontend': 'Coding',
            
            # Data Science keywords
            'data': 'Data Science',
            'science': 'Data Science',
            'ml': 'Data Science',
            'ai': 'Data Science',
            'machine learning': 'Data Science',
            'artificial intelligence': 'Data Science',
            'analytics': 'Data Science',
            'analyst': 'Data Science',
            'deep learning': 'Data Science',
            
            # Leadership keywords
            'lead': 'Leadership',
            'leader': 'Leadership',
            'leadership': 'Leadership',
            'manager': 'Leadership',
            'management': 'Leadership',
            'cto': 'Leadership',
            'ceo': 'Leadership',
            'director': 'Leadership',
            'executive': 'Leadership',
            'vp': 'Leadership',
            
            # Communication keywords
            'communication': 'Communication',
            'speak': 'Communication',
            'speaking': 'Communication',
            'presentation': 'Communication',
            'writing': 'Communication',
            'influence': 'Communication',
            'persuasion': 'Communication',
            'networking': 'Communication',
            
            # Fitness keywords
            'fit': 'Fitness',
            'fitness': 'Fitness',
            'health': 'Fitness',
            'workout': 'Fitness',
            'exercise': 'Fitness',
            'gym': 'Fitness',
            'athlete': 'Fitness',
            'physical': 'Fitness',
            
            # Mindfulness keywords
            'mindful': 'Mindfulness',
            'mindfulness': 'Mindfulness',
            'meditation': 'Mindfulness',
            'zen': 'Mindfulness',
            'peace': 'Mindfulness',
            'calm': 'Mindfulness',
            'spiritual': 'Mindfulness',
            'awareness': 'Mindfulness',
            
            # Entrepreneurship keywords
            'entrepreneur': 'Entrepreneurship',
            'entrepreneurship': 'Entrepreneurship',
            'startup': 'Entrepreneurship',
            'business': 'Entrepreneurship',
            'founder': 'Entrepreneurship',
            'venture': 'Entrepreneurship',
            'company': 'Entrepreneurship',
            'innovation': 'Entrepreneurship',
        }
    
    def text_to_vector(self, user_goal: str) -> np.ndarray:
        """
        Converts user goal text into a 7-dimensional skill vector.
        
        Args:
            user_goal: User's goal statement (e.g., "I want to become a CTO")
        
        Returns:
            Numpy array of shape (7,) representing the goal vector
        """
        # Initialize vector with zeros
        goal_vector = {dim: 0.0 for dim in self.skill_dimensions}
        
        # Convert to lowercase for matching
        goal_lower = user_goal.lower()
        
        # Count matches for each skill dimension
        for keyword, dimension in self.keyword_mapping.items():
            if keyword in goal_lower:
                goal_vector[dimension] += 1.0
        
        # Convert to numpy array
        vector_array = np.array([goal_vector[dim] for dim in self.skill_dimensions])
        
        # Normalize the vector (L2 normalization)
        vector_norm = np.linalg.norm(vector_array)
        if vector_norm > 0:
            vector_array = vector_array / vector_norm
        else:
            # If no keywords matched, return a uniform vector
            vector_array = np.ones(len(self.skill_dimensions)) / np.sqrt(len(self.skill_dimensions))
        
        return vector_array
    
    def recommend(self, user_goal: str, top_k: int = 5) -> List[Dict]:
        """
        Generates content recommendations based on user's goal.
        
        Args:
            user_goal: User's goal statement
            top_k: Number of recommendations to return (default: 5)
        
        Returns:
            List of dictionaries containing recommended content with match scores
        """
        # Convert goal to vector
        goal_vector = self.text_to_vector(user_goal)
        
        # Calculate cosine similarity
        similarities = cosine_similarity(
            goal_vector.reshape(1, -1), 
            self.content_vectors
        )[0]
        
        # Get top K indices
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        # Build recommendations
        recommendations = []
        for idx in top_indices:
            recommendation = {
                'title': self.content_metadata.iloc[idx]['Title'],
                'type': self.content_metadata.iloc[idx]['Type'],
                'description': self.content_metadata.iloc[idx]['Description'],
                'url': self.content_metadata.iloc[idx]['URL'],
                'match_score': float(similarities[idx]),
                'content_vector': self.content_vectors[idx].tolist()
            }
            recommendations.append(recommendation)
        
        return {
            'user_goal': user_goal,
            'goal_vector': goal_vector.tolist(),
            'skill_dimensions': self.skill_dimensions,
            'recommendations': recommendations
        }


# Example usage
if __name__ == "__main__":
    engine = FutureSelfEngine()
    
    # Test recommendation
    result = engine.recommend("I want to become a CTO")
    
    print(f"Goal: {result['user_goal']}")
    print(f"Goal Vector: {result['goal_vector']}")
    print(f"\nTop Recommendations:")
    for i, rec in enumerate(result['recommendations'], 1):
        print(f"\n{i}. {rec['title']} ({rec['type']})")
        print(f"   Match Score: {rec['match_score']:.3f}")
        print(f"   Description: {rec['description']}")
