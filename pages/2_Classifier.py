# pages/2_🎯_Classifier.py
"""
Classifier Page - Predict App Install Tier (Classification)
Classifies apps into 4 tiers: Low Performance, Emerging, Popular, or Viral
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Add parent directory to path
parent_dir = str(Path(__file__).parent.parent)
sys.path.append(parent_dir)

from utils.styling import load_css, create_header, create_section_header
from utils.config import (
    APP_TITLE, APP_ICON, REGRESSION_FEATURES, 
    INSTALL_TIERS, PAGE_LAYOUT, CLASSIFIER_FEATURES
)
from utils.helpers import (
    initialize_session_state, format_number, convert_days_to_readable,
    calculate_rating_density, get_feedback_for_value, validate_inputs,
    prepare_model_input, generate_recommendations, create_summary_dict,
    show_model_performance, get_install_tier_info
)

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title=f"🎯 Classifier | {APP_TITLE}",
    page_icon="🎯",
    layout=PAGE_LAYOUT,
    initial_sidebar_state="expanded"
)

initialize_session_state()
load_css()

# ============================================================================
# MODEL LOADING
# ============================================================================

@st.cache_resource
def load_classifier_model():
    """
    Load the pre-trained classifier model (XGBoost)
    Replace with your actual model path
    """
    try:
        # IMPORTANT: Update this path to your actual model file
        model_path = "models//xgboost_model.pkl"
        model = joblib.load(model_path)
        return model
    except Exception as e:
        st.error(f"⚠️ Error loading model: {e}")
        st.info("Please ensure your classifier model file is in the 'models' directory")
        return None

# ============================================================================
# HEADER
# ============================================================================

create_header(
    "🎯 Install Classification - Predictor",
    "Classify your app into a performance tier and receive tier-specific strategies"
)

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("## 🎯 Classifier Info")
    
    show_model_performance('classifier')
    
    st.markdown("---")
    
    st.markdown("### 📊 Classification Tiers")
    
    for tier_num, tier_info in INSTALL_TIERS.items():
        st.markdown(f"""
        **{tier_info['icon']} {tier_info['name']}** ({tier_info['range']})
        
        {tier_info['description']}
        """)
    
    st.markdown("---")
    
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("app.py")

# ============================================================================
# INPUT FORM
# ============================================================================

st.markdown("## 📝 Enter Your App Details")

with st.container():
    col1, col2 = st.columns(2, gap="large")
    
    form_data = {}
    
    # LEFT COLUMN - Primary Metrics
    with col1:
        create_section_header("📊 App Performance Metrics", "")
        
        # Rating Quality Score
        config = CLASSIFIER_FEATURES['Rating_Quality_Score']
        rating = st.slider(
            f"{config['icon']} {config['display_name']}",
            min_value=config['min'],
            max_value=config['max'],
            value=config['default'],
            step=config['step'],
            help=config['help_text'],
            key='clf_rating_quality'
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
        config = CLASSIFIER_FEATURES['Rating_Count']
        rating_count = st.number_input(
            f"{config['icon']} {config['display_name']}",
            min_value=config['min'],
            max_value=config['max'],
            value=config['default'],
            step=config['step'],
            help=config['help_text'],
            key='clf_rating_count'
        )
        form_data['Rating_Count'] = rating_count
        
        # Show rating count feedback
        if rating_count < 100:
            st.warning("⚠️ Low rating count. Target 100+ for better tier prediction.")
        elif rating_count >= 10000:
            st.success("🎉 Excellent rating count!")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # App Age
        config = CLASSIFIER_FEATURES['App_Age_Days']
        app_age = st.number_input(
            f"{config['icon']} {config['display_name']}",
            min_value=config['min'],
            max_value=config['max'],
            value=config['default'],
            step=config['step'],
            help=config['help_text'],
            key='clf_app_age'
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
        config = CLASSIFIER_FEATURES['Size_MB']
        size = st.slider(
            f"{config['icon']} {config['display_name']}",
            min_value=config['min'],
            max_value=config['max'],
            value=config['default'],
            step=config['step'],
            help=config['help_text'],
            key='clf_app_size'
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
        config = CLASSIFIER_FEATURES['Category']
        category = st.selectbox(
            f"{config['icon']} {config['display_name']}",
            options=config['options'],
            index=config['options'].index(config['default']),
            help=config['help_text'],
            key='clf_category'
        )
        form_data['Category'] = category
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Monetization Strategy Section
        st.markdown("#### 💰 Monetization Strategy")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            config = CLASSIFIER_FEATURES['Free']
            free = st.radio(
                f"{config['icon']} {config['display_name']}",
                options=config['options'],
                index=0 if config['default'] == 'Yes' else 1,
                help=config['help_text'],
                key='clf_free',
                horizontal=True
            )
            form_data['Free'] = free
        
        with col_b:
            config = CLASSIFIER_FEATURES['Ad_Supported']
            ads = st.radio(
                f"{config['icon']} {config['display_name']}",
                options=config['options'],
                index=0 if config['default'] == 'Yes' else 1,
                help=config['help_text'],
                key='clf_ads',
                horizontal=True
            )
            form_data['Ad_Supported'] = ads
        
        col_c, col_d = st.columns(2)
        
        with col_c:
            config = CLASSIFIER_FEATURES['In_App_Purchases']
            iap = st.radio(
                f"{config['icon']} {config['display_name']}",
                options=config['options'],
                index=0 if config['default'] == 'Yes' else 1,
                help=config['help_text'],
                key='clf_iap',
                horizontal=True
            )
            form_data['In_App_Purchases'] = iap
        
        with col_d:
            config = CLASSIFIER_FEATURES['Editors_Choice']
            editors = st.radio(
                f"{config['icon']} {config['display_name']}",
                options=config['options'],
                index=0 if config['default'] == 'Yes' else 1,
                help=config['help_text'],
                key='clf_editors',
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
        "🎯 Classify App Tier",
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
    model = load_classifier_model()
    
    if model is None:
        st.error("❌ Model could not be loaded. Please check model file.")
        st.stop()
    
    # Prepare input
    with st.spinner("🔄 Classifying your app..."):
        model_input = prepare_model_input(form_data)
        
        try:
            # Make prediction
            tier_prediction = model.predict(model_input)[0]
            
            # Get probabilities for confidence visualization
            try:
                probabilities = model.predict_proba(model_input)[0]
            except:
                probabilities = None
            
            # Store in session state
            st.session_state.prediction_made = True
            st.session_state.prediction_result = tier_prediction
            st.session_state.probabilities = probabilities
            st.session_state.form_data = form_data
            
        except Exception as e:
            st.error(f"❌ Classification error: {e}")
            st.stop()

# ============================================================================
# RESULTS DISPLAY
# ============================================================================

if st.session_state.prediction_made and st.session_state.prediction_result is not None:
    
    tier = st.session_state.prediction_result
    form_data = st.session_state.form_data
    probabilities = st.session_state.get('probabilities', None)
    
    tier_info = get_install_tier_info(int(tier))
    
    st.markdown("---")
    st.markdown("## 🎯 Classification Results")
    
    # Main result card with tier color
    tier_color = tier_info['color']
    st.markdown(f"""
    <div class="result-card" style="border-color: {tier_color}; border-width: 3px;">
        <div class="result-title">{tier_info['icon']} {tier_info['name']}</div>
        <div class="result-value" style="color: {tier_color};">{tier_info['range']}</div>
        <div class="result-description">
            {tier_info['description']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Confidence visualization (if probabilities available)
    if probabilities is not None:
        st.markdown("### 📊 Confidence Scores")
        
        # Create confidence bar chart
        tier_names = [INSTALL_TIERS[i]['name'] for i in range(len(probabilities))]
        
        fig = go.Figure()
        
        colors = [INSTALL_TIERS[i]['color'] for i in range(len(probabilities))]
        
        fig.add_trace(go.Bar(
            y=tier_names,
            x=probabilities,
            orientation='h',
            marker=dict(color=colors),
            text=[f"{p*100:.1f}%" for p in probabilities],
            textposition='outside',
            hovertemplate="<b>%{y}</b><br>Confidence: %{x:.1%}<extra></extra>"
        ))
        
        fig.update_layout(
            title="Model Confidence by Tier",
            xaxis_title="Confidence Score",
            yaxis_title="Install Tier",
            showlegend=False,
            height=300,
            template="plotly_dark",
            font=dict(family="Inter, sans-serif"),
            plot_bgcolor="rgba(30,41,59,0.5)",
            paper_bgcolor="rgba(15,23,42,0)",
            xaxis=dict(range=[0, 1], gridcolor="rgba(52,64,84,0.5)"),
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Summary and Strategies
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 Input Summary")
        summary = create_summary_dict(form_data)
        
        for key, value in summary.items():
            st.markdown(f"**{key}:** {value}")
    
    with col2:
        st.markdown("### 🎯 Tier-Specific Strategies")
        
        for rec in tier_info['recommendations']:
            st.markdown(f"""
            <div style="
                background: rgba(30, 41, 59, 0.5);
                padding: 0.75rem;
                border-radius: 8px;
                border-left: 4px solid {tier_color};
                margin-bottom: 0.5rem;
            ">
                <strong style="color: {tier_color};">✓ {rec}</strong>
            </div>
            """, unsafe_allow_html=True)
    
    # Additional Insights and Recommendations
    st.markdown("---")
    st.markdown("### 💡 Recommendations to Next Tier")
    
    recommendations = generate_recommendations(form_data, tier, 'classifier')
    
    if recommendations:
        for rec in recommendations[:5]:
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
    
    # Growth Roadmap
    st.markdown("---")
    st.markdown("### 🚀 Your Growth Roadmap")
    
    # Create tier progression visualization
    tier_progression = []
    current_tier = int(tier)
    
    tier_icons = {
        0: "🔹",
        1: "🟡",
        2: "🟢",
        3: "🔥"
    }
    
    tier_names_short = {
        0: "Low",
        1: "Emerging",
        2: "Popular",
        3: "Viral"
    }
    
    col1, col2, col3, col4 = st.columns(4)
    cols = [col1, col2, col3, col4]
    
    for i in range(4):
        with cols[i]:
            if i < current_tier:
                # Past tier
                st.markdown(f"""
                <div style="
                    background: rgba(16, 185, 129, 0.2);
                    padding: 1rem;
                    border-radius: 8px;
                    text-align: center;
                    border: 2px solid #10B981;
                ">
                    <div style="font-size: 2rem;">{tier_icons[i]}</div>
                    <div style="color: #10B981; font-weight: bold;">{tier_names_short[i]}</div>
                    <div style="color: #94A3B8; font-size: 0.8rem;">✓ Achieved</div>
                </div>
                """, unsafe_allow_html=True)
            elif i == current_tier:
                # Current tier
                st.markdown(f"""
                <div style="
                    background: rgba(59, 130, 246, 0.2);
                    padding: 1rem;
                    border-radius: 8px;
                    text-align: center;
                    border: 3px solid #3B82F6;
                ">
                    <div style="font-size: 2rem;">{tier_icons[i]}</div>
                    <div style="color: #3B82F6; font-weight: bold;">{tier_names_short[i]}</div>
                    <div style="color: #93C5FD; font-size: 0.8rem;">📍 You are here</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Future tier
                st.markdown(f"""
                <div style="
                    background: rgba(107, 114, 128, 0.1);
                    padding: 1rem;
                    border-radius: 8px;
                    text-align: center;
                    border: 2px dashed #334155;
                ">
                    <div style="font-size: 2rem; opacity: 0.5;">{tier_icons[i]}</div>
                    <div style="color: #94A3B8; font-weight: bold;">{tier_names_short[i]}</div>
                    <div style="color: #64748B; font-size: 0.8rem;">🎯 Next Goal</div>
                </div>
                """, unsafe_allow_html=True)
    
    # Key Insights
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
            help="Number of ratings received per day"
        )
    
    with col2:
        st.metric(
            "User Engagement",
            "High" if form_data['Rating_Count'] > 1000 else "Medium" if form_data['Rating_Count'] > 100 else "Low",
            help="Based on total rating count"
        )
    
    with col3:
        st.metric(
            "Quality Score",
            f"{form_data['Rating_Quality_Score']:.1f} ⭐",
            help="Average user rating"
        )
    
    # Compare with tier benchmarks
    st.markdown("---")
    st.markdown("### 📈 Tier Benchmarks")
    
    benchmark_data = {
        "🔹 Low (0-10K)": {"Rating Quality": 2.5, "Rating Density": 0.5, "App Age Days": 90},
        "🟡 Emerging (10K-100K)": {"Rating Quality": 3.5, "Rating Density": 2.0, "App Age Days": 180},
        "🟢 Popular (100K-1M)": {"Rating Quality": 4.0, "Rating Density": 4.0, "App Age Days": 365},
        "🔥 Viral (1M+)": {"Rating Quality": 4.5, "Rating Density": 8.0, "App Age Days": 730},
    }
    
    st.info("💡 **Tip**: To move to the next tier, focus on increasing your app's rating density and quality score.")
    
    # Reset button
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🔄 Make Another Prediction", use_container_width=True):
            st.session_state.prediction_made = False
            st.session_state.prediction_result = None
            st.session_state.probabilities = None
            st.session_state.form_data = None
            st.rerun()

# ============================================================================
# FOOTER INFO
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748B; font-size: 0.9rem;'>
    <p><strong>Note:</strong> Classifications are based on machine learning models trained on 2M+ apps.</p>
    <p>Tiers represent estimated install ranges. Actual results may vary based on market dynamics.</p>
</div>
""", unsafe_allow_html=True)
