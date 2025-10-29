# utils/helpers.py
"""
Helper functions for AppVision Analytics
Includes data processing, validation, and utility functions
"""

import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from .config import REGRESSION_FEATURES, INSTALL_TIERS, MODEL_METRICS


def calculate_rating_density(rating_count, app_age_days):
    """
    Calculate rating density (ratings per day)
    """
    if app_age_days <= 0:
        return 0
    return rating_count / app_age_days


def convert_days_to_readable(days):
    """
    Convert days to human-readable format
    """
    years = days // 365
    remaining_days = days % 365
    months = remaining_days // 30
    
    parts = []
    if years > 0:
        parts.append(f"{years} year{'s' if years > 1 else ''}")
    if months > 0:
        parts.append(f"{months} month{'s' if months > 1 else ''}")
    
    return ", ".join(parts) if parts else f"{days} days"


def format_number(num):
    """
    Format large numbers with K, M, B suffixes
    """
    if num >= 1_000_000_000:
        return f"{num/1_000_000_000:.2f}B"
    elif num >= 1_000_000:
        return f"{num/1_000_000:.2f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    else:
        return f"{num:,.0f}"


def get_feedback_for_value(feature_name, value):
    """
    Get contextual feedback for feature values
    """
    feature_config = REGRESSION_FEATURES.get(feature_name, {})
    feedback_rules = feature_config.get('feedback', {})
    
    if not feedback_rules:
        return None, None
    
    # Sort thresholds in descending order
    thresholds = sorted(feedback_rules.keys(), reverse=True)
    
    for threshold in thresholds:
        if value >= threshold:
            msg_type, message = feedback_rules[threshold]
            return msg_type, message
    
    return None, None


def validate_inputs(input_data):
    """
    Validate user inputs against feature constraints
    """
    errors = []
    warnings = []
    
    # Rating Count validation
    if input_data.get('Rating_Count', 0) < 10:
        warnings.append("⚠️ Very low rating count. Apps typically need 100+ ratings for credibility.")
    
    # Rating Quality Score validation
    rating = input_data.get('Rating_Quality_Score', 0)
    if rating < 3.0:
        errors.append("❌ Rating below 3.0 is critically low. Focus on quality improvements.")
    elif rating < 3.5:
        warnings.append("⚠️ Rating below 3.5 may hurt discoverability.")
    
    # App Age validation
    age = input_data.get('App_Age_Days', 0)
    if age < 7:
        warnings.append("⚠️ Very new app. Consider allowing more time for organic growth.")
    
    # Size validation
    size = input_data.get('Size_MB', 0)
    if size > 150:
        warnings.append("⚠️ Large app size may reduce download conversion rate.")
    elif size > 200:
        errors.append("❌ App size over 200MB significantly impacts downloads.")
    
    return errors, warnings


def prepare_model_input(form_data):
    """
    Prepare user input data for model prediction
    Ensures all features are in the correct format
    """
    # Calculate rating density
    rating_density = calculate_rating_density(
        form_data['Rating_Count'],
        form_data['App_Age_Days']
    )
    
    # Prepare the input dictionary with all required features
    model_input = {
        'Rating_Count': form_data['Rating_Count'],
        'Size_MB': form_data['Size_MB'],
        'Rating_Density': rating_density,
        'Ad_Supported': 1 if form_data['Ad_Supported'] == 'Yes' else 0,
        'Price_USD': 0.0 if form_data['Free'] == 'Yes' else 2.99,  # Default paid price
        'Rating_Quality_Score': form_data['Rating_Quality_Score'],
        'In_App_Purchases': 1 if form_data['In_App_Purchases'] == 'Yes' else 0,
        'Editors_Choice': 1 if form_data['Editors_Choice'] == 'Yes' else 0,
        'Category': form_data['Category'],
        'App_Age_Days': form_data['App_Age_Days'],
        'Free': 1 if form_data['Free'] == 'Yes' else 0,
    }
    
    return pd.DataFrame([model_input])


def get_install_tier_info(tier_number):
    """
    Get tier information for classification results
    """
    return INSTALL_TIERS.get(tier_number, INSTALL_TIERS[0])


def generate_recommendations(form_data, prediction_result=None, model_type='regressor'):
    """
    Generate personalized recommendations based on input data and predictions
    """
    recommendations = []
    
    # Rating-based recommendations
    rating = form_data.get('Rating_Quality_Score', 0)
    if rating < 4.0:
        recommendations.append({
            'icon': '⭐',
            'title': 'Improve User Rating',
            'description': 'Focus on app quality and user experience. Target 4.0+ rating.',
            'priority': 'high'
        })
    
    # Rating count recommendations
    rating_count = form_data.get('Rating_Count', 0)
    rating_density = calculate_rating_density(rating_count, form_data.get('App_Age_Days', 1))
    
    if rating_density < 1.0:
        recommendations.append({
            'icon': '📈',
            'title': 'Boost User Engagement',
            'description': 'Encourage users to leave ratings. Aim for 1+ rating per day.',
            'priority': 'high'
        })
    elif rating_count < 1000:
        recommendations.append({
            'icon': '💬',
            'title': 'Scale User Feedback',
            'description': 'Implement in-app prompts to gather more ratings.',
            'priority': 'medium'
        })
    
    # Size optimization
    size = form_data.get('Size_MB', 0)
    if size > 100:
        recommendations.append({
            'icon': '💾',
            'title': 'Optimize App Size',
            'description': f'Current size: {size}MB. Reduce to under 100MB for better conversion.',
            'priority': 'medium'
        })
    
    # Monetization recommendations
    is_free = form_data.get('Free') == 'Yes'
    has_ads = form_data.get('Ad_Supported') == 'Yes'
    has_iap = form_data.get('In_App_Purchases') == 'Yes'
    
    if is_free and not has_ads and not has_iap:
        recommendations.append({
            'icon': '💰',
            'title': 'Implement Monetization',
            'description': 'Consider adding ads or in-app purchases for revenue.',
            'priority': 'low'
        })
    
    # Age-based recommendations
    age = form_data.get('App_Age_Days', 0)
    if age < 90:
        recommendations.append({
            'icon': '🚀',
            'title': 'Launch Marketing Push',
            'description': 'First 90 days are critical. Invest in user acquisition.',
            'priority': 'high'
        })
    
    # Category-specific recommendations
    category = form_data.get('Category', '')
    high_growth_categories = ['Photography', 'Business', 'Education', 'Productivity']
    if category in high_growth_categories:
        recommendations.append({
            'icon': '📊',
            'title': 'Leverage Category Strength',
            'description': f'{category} shows high growth potential. Focus on category-specific features.',
            'priority': 'medium'
        })
    
    return recommendations


def create_summary_dict(form_data):
    """
    Create a clean summary dictionary for display
    """
    age_readable = convert_days_to_readable(form_data['App_Age_Days'])
    rating_density = calculate_rating_density(
        form_data['Rating_Count'],
        form_data['App_Age_Days']
    )
    
    return {
        'Category': form_data['Category'],
        'User Rating': f"{form_data['Rating_Quality_Score']:.1f} ⭐",
        'Total Ratings': format_number(form_data['Rating_Count']),
        'Rating Density': f"{rating_density:.2f} ratings/day",
        'App Age': age_readable,
        'Size': f"{form_data['Size_MB']:.1f} MB",
        'Free': 'Yes' if form_data['Free'] == 'Yes' else 'No',
        'Monetization': get_monetization_summary(form_data),
        'Editors Choice': '🏆 Yes' if form_data['Editors_Choice'] == 'Yes' else 'No'
    }


def get_monetization_summary(form_data):
    """
    Get monetization strategy summary
    """
    strategies = []
    
    if form_data.get('Ad_Supported') == 'Yes':
        strategies.append('Ads')
    if form_data.get('In_App_Purchases') == 'Yes':
        strategies.append('IAP')
    if form_data.get('Free') == 'No':
        strategies.append('Paid')
    
    return ', '.join(strategies) if strategies else 'None'


def display_feature_importance():
    """
    Display feature importance information
    """
    st.markdown("### 📊 Feature Importance")
    
    # Create importance data
    importance_data = []
    for feature, config in REGRESSION_FEATURES.items():
        if 'importance' in config:
            importance_data.append({
                'Feature': config['display_name'],
                'Importance': config['importance']
            })
    
    # Sort by importance
    importance_df = pd.DataFrame(importance_data)
    importance_df = importance_df.sort_values('Importance', ascending=False)
    
    # Display as horizontal bar chart or table
    st.dataframe(
        importance_df,
        use_container_width=True,
        hide_index=True
    )


def show_model_performance(model_type='regressor'):
    """
    Display model performance metrics in sidebar
    """
    metrics = MODEL_METRICS.get(model_type, {})
    
    st.sidebar.markdown(f"### 🎯 {model_type.title()} Performance")
    
    if model_type == 'regressor':
        st.sidebar.metric("R² Score", f"{metrics.get('r2_score', 0):.1%}")
        st.sidebar.metric("RMSE", f"{metrics.get('rmse', 0):.3f}")
        st.sidebar.metric("MAE", f"{metrics.get('mae', 0):.3f}")
    elif model_type == 'classifier':
        st.sidebar.metric("Accuracy", f"{metrics.get('accuracy', 0):.1%}")
        st.sidebar.metric("F1 Score", f"{metrics.get('f1_macro', 0):.3f}")
        st.sidebar.metric("Precision", f"{metrics.get('precision', 0):.1%}")
    
    # Progress bars
    if model_type == 'regressor':
        st.sidebar.progress(metrics.get('r2_score', 0), text="Model Accuracy")
    else:
        st.sidebar.progress(metrics.get('accuracy', 0), text="Model Accuracy")


def initialize_session_state():
    """
    Initialize Streamlit session state variables
    """
    if 'prediction_made' not in st.session_state:
        st.session_state.prediction_made = False
    
    if 'prediction_result' not in st.session_state:
        st.session_state.prediction_result = None
    
    if 'form_data' not in st.session_state:
        st.session_state.form_data = None
    
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
