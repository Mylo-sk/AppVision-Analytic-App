# app.py
"""
AppVision Analytics - Main Application
Predictive analytics for mobile app performance
"""

import streamlit as st
import sys
from pathlib import Path

# Add utils to path
sys.path.append(str(Path(__file__).parent))

from utils.styling import load_css, create_header, create_metric_card
from utils.config import (
    APP_TITLE, APP_ICON, PAGE_LAYOUT, INITIAL_SIDEBAR_STATE,
    MODEL_METRICS, QUICK_TIPS
)
from utils.helpers import initialize_session_state

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title=f"{APP_ICON} {APP_TITLE}",
    page_icon=APP_ICON,
    layout=PAGE_LAYOUT,
    initial_sidebar_state=INITIAL_SIDEBAR_STATE,
    menu_items={
        'Get Help': 'https://github.com/yourusername/appvision',
        'Report a bug': 'https://github.com/yourusername/appvision/issues',
        'About': f"""
        # {APP_ICON} {APP_TITLE}
        
        **Predict app performance with data-driven insights**
        
        Built with ❤️ using Streamlit and Machine Learning
        
        - 🎯 96.5% Classification Accuracy
        - 📊 75.2% Regression R² Score
        - 📱 2M+ Apps Analyzed
        - 🚀 Real-time Predictions
        
        © 2025 AppVision Analytics
        """
    }
)

# ============================================================================
# INITIALIZATION
# ============================================================================

initialize_session_state()
load_css()

# ============================================================================
# SIDEBAR
# ============================================================================

def render_sidebar():
    """Render the sidebar with model info and tips"""
    
    with st.sidebar:
        st.markdown("## 🎯 Model Performance")
        
        # Regressor metrics
        reg_metrics = MODEL_METRICS['regressor']
        st.metric(
            "📊 Regression Accuracy",
            reg_metrics['accuracy'],
            help="R² Score: Explains 75.2% of install variance"
        )
        st.progress(reg_metrics['r2_score'])
        
        st.markdown("---")
        
        # Classifier metrics
        clf_metrics = MODEL_METRICS['classifier']
        st.metric(
            "🎯 Classification Accuracy",
            clf_metrics['accuracy_display'],
            help="96.5% accuracy in predicting install tiers"
        )
        st.progress(clf_metrics['accuracy'])
        
        st.markdown("---")
        
        # Quick Tips
        st.markdown("## 💡 Quick Tips")
        
        with st.expander("📚 View Success Strategies", expanded=False):
            for tip in QUICK_TIPS:
                st.markdown(f"- {tip}")
        
        st.markdown("---")
        
        # Footer
        st.markdown("""
        <div style='text-align: center; color: #94A3B8; font-size: 0.85rem;'>
            <p>Made with ❤️ by AppVision</p>
            <p>© 2025 All Rights Reserved</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# HOME PAGE
# ============================================================================

def render_home_page():
    """Render the main home page"""
    
    # Header
    create_header(
        f"{APP_ICON} {APP_TITLE}",
        "Predict App Success with Data-Driven Insights"
    )
    
    # Metrics Row
    st.markdown("### 📊 Platform Insights")
    
    cols = st.columns(4)
    metrics = [
        ("📱", "2M+", "Apps Analyzed"),
        ("🎯", "96.5%", "Prediction Accuracy"),
        ("🚀", "1.2K+", "Success Stories"),
        ("📂", "48", "Categories"),
    ]
    
    for col, (icon, value, label) in zip(cols, metrics):
        col.markdown(
            create_metric_card(icon, value, label),
            unsafe_allow_html=True
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Feature Cards
    st.markdown("### 🎯 Prediction Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="form-container">
            <h3 style="color: #3B82F6; text-align: center;">📊 Regressor</h3>
            <p style="text-align: center; color: #94A3B8;">
                Predict the exact number of app installs based on your app's features.
            </p>
            <ul style="color: #F1F5F9; line-height: 1.8;">
                <li>Numerical install prediction</li>
                <li>75.2% R² accuracy</li>
                <li>Feature importance analysis</li>
                <li>Actionable recommendations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="form-container">
            <h3 style="color: #10B981; text-align: center;">🎯 Classifier</h3>
            <p style="text-align: center; color: #94A3B8;">
                Classify your app into performance tiers: Low, Emerging, Popular, or Viral.
            </p>
            <ul style="color: #F1F5F9; line-height: 1.8;">
                <li>4-tier classification system</li>
                <li>96.5% accuracy</li>
                <li>Tier-specific strategies</li>
                <li>Growth roadmap insights</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="form-container">
            <h3 style="color: #F59E0B; text-align: center;">💡 Recommender</h3>
            <p style="text-align: center; color: #94A3B8;">
                Find similar successful apps and learn from their strategies.
            </p>
            <ul style="color: #F1F5F9; line-height: 1.8;">
                <li>Content-based recommendations</li>
                <li>Similar app discovery</li>
                <li>Competitive analysis</li>
                <li>Strategic benchmarking</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Call to Action
    st.markdown("### 🚀 Get Started")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Launch Regressor", use_container_width=True, type="primary"):
            st.switch_page("pages/1_Regressor.py")
    
    with col2:
        if st.button("🎯 Launch Classifier", use_container_width=True, type="primary"):
            st.switch_page("pages/2_Classifier.py")
    
    with col3:
        if st.button("💡 Launch Recommender", use_container_width=True, type="primary"):
            st.switch_page("pages/3_Recommender.py")
    
    # Additional Information
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📚 How It Works
        
        Our platform uses **machine learning models** trained on over **2 million apps** 
        from the Google Play Store. We analyze:
        
        - **Rating Engagement**: User ratings and review patterns
        - **App Characteristics**: Size, category, age, and features
        - **Monetization Strategy**: Free, paid, ads, and in-app purchases
        - **Market Position**: Editors' Choice and category performance
        
        The models identify patterns that predict app success with industry-leading accuracy.
        """)
    
    with col2:
        st.markdown("""
        ### 🎯 Why AppVision?
        
        - **🚀 Fast Predictions**: Get results in seconds
        - **📊 Data-Driven**: Based on real app store data
        - **💡 Actionable Insights**: Receive personalized recommendations
        - **🎯 High Accuracy**: 96.5% classification accuracy
        - **📱 User-Friendly**: Intuitive interface, no technical knowledge needed
        - **🔒 Privacy First**: Your data never leaves the session
        """)
    
    # Key Features Highlight
    st.markdown("---")
    st.markdown("### ⭐ Key Success Factors")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 2rem;">📈</div>
            <h4 style="color: #10B981;">Rating Density</h4>
            <p style="color: #94A3B8; font-size: 0.9rem;">
                47.5% importance<br>
                Most critical factor
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 2rem;">💬</div>
            <h4 style="color: #3B82F6;">Rating Count</h4>
            <p style="color: #94A3B8; font-size: 0.9rem;">
                38.3% importance<br>
                User engagement signal
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 2rem;">⭐</div>
            <h4 style="color: #F59E0B;">Rating Quality</h4>
            <p style="color: #94A3B8; font-size: 0.9rem;">
                15% importance<br>
                Quality indicator
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 2rem;">📅</div>
            <h4 style="color: #EF4444;">App Age</h4>
            <p style="color: #94A3B8; font-size: 0.9rem;">
                5.4% importance<br>
                Time on market
            </p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main application entry point"""
    
    # Render sidebar
    render_sidebar()
    
    # Render home page
    render_home_page()

if __name__ == "__main__":
    main()
