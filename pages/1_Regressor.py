# pages/1_📊_Regressor.py
"""
Regressor Page - Predict Numerical App Installs
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import joblib

# Add parent directory to path
parent_dir = str(Path(__file__).parent.parent)
sys.path.append(parent_dir)

from utils.styling import load_css, create_header, create_section_header
from utils.config import (
    APP_TITLE, APP_ICON, REGRESSION_FEATURES, 
    FEATURE_IMPORTANCE_ORDER, PAGE_LAYOUT
)
from utils.helpers import (
    initialize_session_state, format_number, convert_days_to_readable,
    calculate_rating_density, get_feedback_for_value, validate_inputs,
    prepare_model_input, generate_recommendations, create_summary_dict,
    show_model_performance
)

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title=f"📊 Regressor | {APP_TITLE}",
    page_icon="📊",
    layout=PAGE_LAYOUT,
    initial_sidebar_state="expanded"
)

initialize_session_state()
load_css()

# ============================================================================
# MODEL LOADING
# ============================================================================

@st.cache_resource
def load_regressor_model():
    """
    Load the pre-trained regressor model
    Replace with your actual model path
    """
    try:
        # IMPORTANT: Update this path to your actual model file
        model_path = "models/gstore_rfr_model.pkl"
        model = joblib.load(model_path)
        return model
    except Exception as e:
        st.error(f"⚠️ Error loading model: {e}")
        st.info("Please ensure your model file is in the 'models' directory")
        return None

# ============================================================================
# HEADER
# ============================================================================

create_header(
    "📊 Install Prediction - Regressor",
    "Predict the exact number of app installs based on your features"
)

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("## 📊 Regressor Info")
    
    show_model_performance('regressor')
    
    st.markdown("---")
    
    st.markdown("### 📈 Top Features")
    st.markdown("""
    The most important factors:
    
    1. **Rating Density** (47.5%)
    2. **Rating Count** (38.3%)
    3. **Rating Quality** (15%)
    4. **App Age** (5.4%)
    5. **App Size** (3.8%)
    """)
    
    st.markdown("---")
    
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("app.py")

# ============================================================================
# INPUT FORM
# ============================================================================

st.markdown("## 📝 Enter Your App Details")

# Form container
with st.container():
    col1, col2 = st.columns(2, gap="large")
    
    form_data = {}
    
    # LEFT COLUMN - Primary Metrics
    with col1:
        create_section_header("📊 App Performance Metrics", "")
        
        # Rating Quality Score
        config = REGRESSION_FEATURES['Rating_Quality_Score']
        rating = st.slider(
            f"{config['icon']} {config['display_name']}",
            min_value=config['min'],
            max_value=config['max'],
            value=config['default'],
            step=config['step'],
            help=config['help_text'],
            key='rating_quality'
        )
        form_data['Rating_Quality_Score'] = rating
        
        # Real-time feedback for rating
        feedback_type, feedback_msg = get_feedback_for_value('Rating_Quality_Score', rating)
        if feedback_msg:
            if feedback_type == 'success':
                st.success(feedback_msg)
            elif feedback_type == 'info':
                st.info(feedback_msg)
            elif feedback_type == 'warning':
                st.warning(feedback_msg)
            elif feedback_type == 'error':
                st.error(feedback_msg)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Rating Count
        config = REGRESSION_FEATURES['Rating_Count']
        rating_count = st.number_input(
            f"{config['icon']} {config['display_name']}",
            min_value=config['min'],
            max_value=config['max'],
            value=config['default'],
            step=config['step'],
            help=config['help_text'],
            key='rating_count'
        )
        form_data['Rating_Count'] = rating_count
        
        # Show rating count feedback
        if rating_count < 100:
            st.warning("⚠️ Low rating count. Target 100+ for credibility.")
        elif rating_count >= 10000:
            st.success("🎉 Excellent rating count!")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # App Age
        config = REGRESSION_FEATURES['App_Age_Days']
        app_age = st.number_input(
            f"{config['icon']} {config['display_name']}",
            min_value=config['min'],
            max_value=config['max'],
            value=config['default'],
            step=config['step'],
            help=config['help_text'],
            key='app_age'
        )
        form_data['App_Age_Days'] = app_age
        
        # Show readable age
        readable_age = convert_days_to_readable(app_age)
        st.caption(f"📊 Age: **{readable_age}**")
        
        # Calculate and show rating density
        rating_density = calculate_rating_density(rating_count, app_age)
        st.caption(f"📈 Rating Density: **{rating_density:.2f} ratings/day**")
        
        if rating_density < 1.0:
            st.warning("⚠️ Low rating density. Encourage more user reviews.")
        elif rating_density >= 5.0:
            st.success("🚀 Excellent rating density!")
    
    # RIGHT COLUMN - App Details
    with col2:
        create_section_header("🔧 App Configuration", "")
        
        # App Size
        config = REGRESSION_FEATURES['Size_MB']
        size = st.number_input(
            f"{config['icon']} {config['display_name']}",
            min_value=config['min'],
            max_value=config['max'],
            value=config['default'],
            step=config['step'],
            help=config['help_text'],
            key='app_size'
        )
        form_data['Size_MB'] = size
        
        # Size feedback
        feedback_type, feedback_msg = get_feedback_for_value('Size_MB', size)
        if feedback_msg:
            if feedback_type == 'success':
                st.success(feedback_msg)
            elif feedback_type == 'info':
                st.info(feedback_msg)
            elif feedback_type == 'warning':
                st.warning(feedback_msg)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Category
        config = REGRESSION_FEATURES['Category']
        category = st.selectbox(
            f"{config['icon']} {config['display_name']}",
            options=config['options'],
            index=config['options'].index(config['default']),
            help=config['help_text'],
            key='category'
        )
        form_data['Category'] = category
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Monetization Strategy Section
        st.markdown("#### 💰 Monetization Strategy")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            config = REGRESSION_FEATURES['Free']
            free = st.radio(
                f"{config['icon']} {config['display_name']}",
                options=config['options'],
                index=0 if config['default'] == 'Yes' else 1,
                help=config['help_text'],
                key='free',
                horizontal=True
            )
            form_data['Free'] = free
        
        with col_b:
            config = REGRESSION_FEATURES['Ad_Supported']
            ads = st.radio(
                f"{config['icon']} {config['display_name']}",
                options=config['options'],
                index=0 if config['default'] == 'Yes' else 1,
                help=config['help_text'],
                key='ads',
                horizontal=True
            )
            form_data['Ad_Supported'] = ads
        
        col_c, col_d = st.columns(2)
        
        with col_c:
            config = REGRESSION_FEATURES['In_App_Purchases']
            iap = st.radio(
                f"{config['icon']} {config['display_name']}",
                options=config['options'],
                index=0 if config['default'] == 'Yes' else 1,
                help=config['help_text'],
                key='iap',
                horizontal=True
            )
            form_data['In_App_Purchases'] = iap
        
        with col_d:
            config = REGRESSION_FEATURES['Editors_Choice']
            editors = st.radio(
                f"{config['icon']} {config['display_name']}",
                options=config['options'],
                index=0 if config['default'] == 'Yes' else 1,
                help=config['help_text'],
                key='editors',
                horizontal=True
            )
            form_data['Editors_Choice'] = editors

# ============================================================================
# PREDICTION SECTION
# ============================================================================

st.markdown("---")
st.markdown("## 🚀 Generate Prediction")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    predict_button = st.button(
        "🔮 Predict App Installs",
        use_container_width=True,
        type="primary"
    )

if predict_button:
    # Validate inputs
    errors, warnings = validate_inputs(form_data)
    
    # Show validation messages
    if errors:
        for error in errors:
            st.error(error)
        st.stop()
    
    if warnings:
        with st.expander("⚠️ Warnings - Click to view", expanded=True):
            for warning in warnings:
                st.warning(warning)
    
    # Load model
    model = load_regressor_model()
    
    if model is None:
        st.error("❌ Model could not be loaded. Please check model file.")
        st.stop()
    
    # Prepare input
    with st.spinner("🔄 Analyzing your app data..."):
        model_input = prepare_model_input(form_data)
        
        try:
            # Make prediction
            prediction = model.predict(model_input)[0]
            
            # Store in session state
            st.session_state.prediction_made = True
            st.session_state.prediction_result = prediction
            st.session_state.form_data = form_data
            
        except Exception as e:
            st.error(f"❌ Prediction error: {e}")
            st.stop()

# ============================================================================
# RESULTS DISPLAY
# ============================================================================

if st.session_state.prediction_made and st.session_state.prediction_result is not None:
    
    prediction = st.session_state.prediction_result
    form_data = st.session_state.form_data
    
    st.markdown("---")
    st.markdown("## 🎯 Prediction Results")
    
    # Main result card
    st.markdown(f"""
    <div class="result-card">
        <div class="result-title">📊 Predicted App Installs</div>
        <div class="result-value">{format_number(prediction)}</div>
        <div class="result-description">
            Based on your app's features, we predict approximately <strong>{format_number(prediction)}</strong> installs.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Summary and Recommendations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 Input Summary")
        summary = create_summary_dict(form_data)
        
        for key, value in summary.items():
            st.markdown(f"**{key}:** {value}")
    
    with col2:
        st.markdown("### 💡 Recommendations")
        recommendations = generate_recommendations(form_data, prediction, 'regressor')
        
        for rec in recommendations[:5]:  # Show top 5
            priority_color = {
                'high': '#EF4444',
                'medium': '#F59E0B',
                'low': '#10B981'
            }
            color = priority_color.get(rec['priority'], '#3B82F6')
            
            st.markdown(f"""
            <div style="
                background: rgba(30, 41, 59, 0.5);
                padding: 1rem;
                border-radius: 8px;
                border-left: 4px solid {color};
                margin-bottom: 0.75rem;
            ">
                <strong style="color: {color};">{rec['icon']} {rec['title']}</strong><br>
                <span style="color: #94A3B8; font-size: 0.9rem;">{rec['description']}</span>
            </div>
            """, unsafe_allow_html=True)
    
    # Additional Insights
    st.markdown("---")
    st.markdown("### 📊 Key Insights")
    
    col1, col2, col3 = st.columns(3)
    
    rating_density = calculate_rating_density(
        form_data['Rating_Count'],
        form_data['App_Age_Days']
    )
    
    with col1:
        st.metric(
            "Rating Density",
            f"{rating_density:.2f}/day",
            help="Number of ratings received per day (47.5% importance)"
        )
    
    with col2:
        st.metric(
            "User Engagement",
            "High" if form_data['Rating_Count'] > 1000 else "Medium" if form_data['Rating_Count'] > 100 else "Low",
            help="Based on total rating count (38.3% importance)"
        )
    
    with col3:
        st.metric(
            "Quality Score",
            f"{form_data['Rating_Quality_Score']:.1f} ⭐",
            help="Average user rating (15% importance)"
        )
    
    # Reset button
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🔄 Make Another Prediction", use_container_width=True):
            st.session_state.prediction_made = False
            st.session_state.prediction_result = None
            st.session_state.form_data = None
            st.rerun()

# ============================================================================
# FOOTER INFO
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748B; font-size: 0.9rem;'>
    <p><strong>Note:</strong> Predictions are based on machine learning models trained on 2M+ apps.</p>
    <p>Actual results may vary based on marketing efforts, market timing, and app quality.</p>
</div>
""", unsafe_allow_html=True)
