# pages/3_Recommender.py
"""
Recommender Page - Content-Based App Recommendation System (FAISS)
Uses Facebook AI Similarity Search for fast, accurate app recommendations
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import joblib
import faiss
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from scipy.sparse import hstack

# Add parent directory to path
parent_dir = str(Path(__file__).parent.parent)
sys.path.append(parent_dir)

from utils.styling import load_css, create_header, create_section_header
from utils.config import (
    APP_TITLE, APP_ICON, PAGE_LAYOUT, 
    CLASSIFIER_FEATURES, MODEL_METRICS, COLORS
)
from utils.helpers import (
    initialize_session_state, format_number, convert_days_to_readable,
    calculate_rating_density
)

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title=f"💡 Recommender | {APP_TITLE}",
    page_icon="💡",
    layout=PAGE_LAYOUT,
    initial_sidebar_state="expanded"
)

initialize_session_state()
load_css()

# ============================================================================
# MODEL & DATA LOADING
# ============================================================================

@st.cache_resource
def load_recommender_system():
    """
    Load the FAISS-based recommender system components:
    - Dataset with app features
    - FAISS index for similarity search
    - Preprocessors (encoders, scalers)
    """
    try:
        # Load the processed dataset
        gsdf = pd.read_csv("data/gsdf_clean.csv")
        
        # Load FAISS index
        index = faiss.read_index("models/faiss_recommender.index")
        
        # Load preprocessors
        cat_encoder = joblib.load("models/cat_encoder.pkl")
        scaler = joblib.load("models/scaler.pkl")
        
        return {
            'dataset': gsdf,
            'index': index,
            'cat_encoder': cat_encoder,
            'scaler': scaler,
            'feature_matrix': None  # Will be loaded separately if needed
        }
    except Exception as e:
        st.error(f"⚠️ Error loading recommender system: {e}")
        st.info("""
        Please ensure the following files exist:
        - `data/gsdf_clean.csv` - Processed dataset
        - `models/faiss_recommender.index` - FAISS index
        - `models/cat_encoder.pkl` - Category encoder
        - `models/scaler.pkl` - Feature scaler
        """)
        return None

@st.cache_data
def load_feature_matrix():
    """Load or recreate the feature matrix for recommendations"""
    try:
        # Try to load pre-computed matrix
        import scipy.sparse as sp
        X = sp.load_npz("models/feature_matrix.npz")
        return X.toarray().astype('float32')
    except:
        # If not available, will need to recreate from dataset
        st.warning("Feature matrix not found. Using FAISS index only.")
        return None

# ============================================================================
# RECOMMENDATION FUNCTIONS
# ============================================================================

def prepare_input_features(form_data, cat_encoder, scaler):
    """
    Prepare input features for similarity search
    
    Args:
        form_data: Dictionary with user input
        cat_encoder: Fitted OneHotEncoder for categories
        scaler: Fitted MinMaxScaler for numerical features
        
    Returns:
        Normalized feature vector ready for FAISS search
    """
    # Extract features
    category = form_data['Category']
    rating_quality = form_data['Rating_Quality_Score']
    rating_count = form_data['Rating_Count']
    app_age = form_data['App_Age_Days']
    size_mb = form_data['Size_MB']
    
    # Calculate rating density
    rating_density = rating_count / (app_age + 1)
    
    # Encode category
    cat_features = cat_encoder.transform([[category]])
    
    # Scale numerical features
    num_features = np.array([[
        rating_quality,
        rating_count,
        app_age,
        size_mb,
        rating_density
    ]])
    num_features_scaled = scaler.transform(num_features)
    
    # Combine features
    X = hstack([cat_features, num_features_scaled])
    X_dense = X.toarray().astype('float32')
    
    # Normalize for cosine similarity
    faiss.normalize_L2(X_dense)
    
    return X_dense

def recommend_apps_faiss(form_data, recommender_system, n=5, min_rating=3.5):
    """
    Recommend similar apps using FAISS similarity search
    
    Args:
        form_data: User input dictionary
        recommender_system: Loaded recommender components
        n: Number of recommendations
        min_rating: Minimum rating threshold
        
    Returns:
        DataFrame with recommended apps
    """
    try:
        # Prepare input vector
        input_vector = prepare_input_features(
            form_data,
            recommender_system['cat_encoder'],
            recommender_system['scaler']
        )
        
        # Search for similar apps (get more than needed to filter)
        D, I = recommender_system['index'].search(input_vector, n * 3)
        
        # Get recommended apps
        dataset = recommender_system['dataset']
        similar_indices = I[0]
        
        # Filter by minimum rating and return top n
        recommendations = dataset.iloc[similar_indices].copy()
        recommendations = recommendations[recommendations['Rating'] >= min_rating]
        recommendations = recommendations.head(n)
        
        # Add similarity scores
        recommendations['Similarity'] = D[0][:len(recommendations)]
        
        return recommendations[['App_Name', 'Category', 'Rating', 'Rating_Count', 
                               'Installs_Central', 'Size_MB', 'Free', 'Ad_Supported', 
                               'In_App_Purchases', 'Editors_Choice', 'Similarity']]
        
    except Exception as e:
        st.error(f"Error generating recommendations: {e}")
        return pd.DataFrame()

def search_similar_apps(app_name, recommender_system, n=5):
    """
    Find apps similar to a specific app by name
    
    Args:
        app_name: Name of the app to find similar ones
        recommender_system: Loaded recommender components
        n: Number of recommendations
        
    Returns:
        DataFrame with similar apps
    """
    dataset = recommender_system['dataset']
    
    # Find matching apps (case-insensitive, partial match)
    matches = dataset[dataset['App_Name'].str.contains(app_name, case=False, na=False)]
    
    if matches.empty:
        return None, f"No apps found matching '{app_name}'. Try another search term."
    
    # Get the first match
    idx = matches.index[0]
    matched_app = dataset.iloc[idx]
    
    # Reload feature matrix for this specific search
    try:
        X_dense = load_feature_matrix()
        if X_dense is None:
            return None, "Feature matrix not available for app-based search."
        
        # Get app vector and normalize
        app_vector = X_dense[idx].reshape(1, -1)
        faiss.normalize_L2(app_vector)
        
        # Search for similar apps
        D, I = recommender_system['index'].search(app_vector, n + 1)
        
        # Exclude the app itself (first result)
        similar_indices = I[0][1:]
        
        # Get recommendations
        recommendations = dataset.iloc[similar_indices].copy()
        recommendations['Similarity'] = D[0][1:len(recommendations)+1]
        
        return recommendations[['App_Name', 'Category', 'Rating', 'Rating_Count', 
                               'Installs_Central', 'Size_MB', 'Similarity']], None
        
    except Exception as e:
        return None, f"Error finding similar apps: {e}"

# ============================================================================
# HEADER
# ============================================================================

create_header(
    "💡 Smart App Recommender",
    "Discover similar successful apps using AI-powered content-based filtering"
)

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("## 💡 Recommender Info")
    
    st.markdown("### 🎯 System Performance")
    
    rec_metrics = MODEL_METRICS.get('recommender', {})
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Precision@10", f"{rec_metrics.get('precision_at_10', 0.85):.1%}")
    with col2:
        st.metric("Recall@10", f"{rec_metrics.get('recall_at_10', 0.72):.1%}")
    
    st.metric("NDCG Score", f"{rec_metrics.get('ndcg', 0.89):.3f}", 
             help="Normalized Discounted Cumulative Gain")
    
    st.markdown("---")
    
    st.markdown("### 📋 How It Works")
    st.markdown("""
    **FAISS-Based Similarity Search:**
    
    1. **Describe Your App** - Enter key features
    2. **AI Analysis** - FAISS finds similar apps
    3. **Smart Ranking** - Apps ranked by similarity
    4. **Learn Strategies** - Discover success patterns
    5. **Competitive Edge** - Apply insights
    
    **Technology:**
    - Facebook AI Similarity Search (FAISS)
    - Content-based filtering
    - Cosine similarity matching
    - Real-time recommendations
    """)
    
    st.markdown("---")
    
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("app.py")

# ============================================================================
# LOAD RECOMMENDER SYSTEM
# ============================================================================

recommender_system = load_recommender_system()

if recommender_system is None:
    st.error("❌ Could not load recommender system. Please check model files.")
    st.stop()

# ============================================================================
# TWO MODES: APP-BASED SEARCH OR FEATURE-BASED RECOMMENDATION
# ============================================================================

st.markdown("## 🔍 Choose Recommendation Mode")

mode = st.radio(
    "",
    options=["🎯 Feature-Based Recommendations", "🔍 Find Apps Similar to..."],
    help="Choose how you want to discover new apps"
)

st.markdown("---")

# ============================================================================
# MODE 1: APP-BASED SEARCH
# ============================================================================

if mode == "🔍 Find Apps Similar to...":
    st.markdown("### 🔎 Search for an App")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input(
            "Enter app name:",
            placeholder="e.g., WhatsApp, Instagram, Candy Crush...",
            help="Type any part of the app name"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        n_results = st.number_input(
            "Results:",
            min_value=3,
            max_value=20,
            value=8,
            step=1
        )
    
    if st.button("🔍 Find Similar Apps", use_container_width=True, type="primary"):
        if not search_query:
            st.warning("⚠️ Please enter an app name to search.")
        else:
            with st.spinner(f"🔄 Searching for apps similar to '{search_query}'..."):
                recommendations, error = search_similar_apps(
                    search_query,
                    recommender_system,
                    n=n_results
                )
                
                if error:
                    st.error(error)
                elif recommendations is not None and not recommendations.empty:
                    # Store in session state
                    st.session_state.recommendations = recommendations
                    st.session_state.search_query = search_query
                    st.session_state.recommendations_made = True

# ============================================================================
# MODE 2: FEATURE-BASED RECOMMENDATIONS
# ============================================================================

else:  # Feature-Based Mode
    st.markdown("## 📝 Describe Your App")
    
    with st.container():
        col1, col2 = st.columns(2, gap="large")
        
        form_data = {}
        
        # LEFT COLUMN
        with col1:
            create_section_header("📊 App Performance", "")
            
            # Rating Quality
            config = CLASSIFIER_FEATURES['Rating_Quality_Score']
            rating = st.slider(
                f"{config['icon']} {config['display_name']}",
                min_value=config['min'],
                max_value=config['max'],
                value=config['default'],
                step=config['step'],
                help=config['help_text'],
                key='rec_rating'
            )
            form_data['Rating_Quality_Score'] = rating
            
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
                key='rec_rating_count'
            )
            form_data['Rating_Count'] = rating_count
            
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
                key='rec_app_age'
            )
            form_data['App_Age_Days'] = app_age
            
            readable_age = convert_days_to_readable(app_age)
            st.caption(f"📊 Age: **{readable_age}**")
            
            rating_density = calculate_rating_density(rating_count, app_age)
            st.caption(f"📈 Rating Density: **{rating_density:.2f} ratings/day**")
        
        # RIGHT COLUMN
        with col2:
            create_section_header("🔧 App Details", "")
            
            # Size
            config = CLASSIFIER_FEATURES['Size_MB']
            size = st.slider(
                f"{config['icon']} {config['display_name']}",
                min_value=config['min'],
                max_value=config['max'],
                value=config['default'],
                step=config['step'],
                help=config['help_text'],
                key='rec_size'
            )
            form_data['Size_MB'] = size
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Category
            config = CLASSIFIER_FEATURES['Category']
            category = st.selectbox(
                f"{config['icon']} {config['display_name']}",
                options=config['options'],
                index=config['options'].index(config['default']),
                help=config['help_text'],
                key='rec_category'
            )
            form_data['Category'] = category
    
    # Settings
    st.markdown("---")
    st.markdown("## ⚙️ Recommendation Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        n_recommendations = st.slider(
            "Number of Recommendations",
            min_value=3,
            max_value=15,
            value=8,
            step=1,
            help="How many similar apps to recommend"
        )
    
    with col2:
        min_rating = st.slider(
            "Minimum Rating Filter",
            min_value=1.0,
            max_value=5.0,
            value=3.5,
            step=0.5,
            help="Only show apps with this rating or higher"
        )
    
    # Generate Button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🔍 Find Similar Apps", use_container_width=True, type="primary"):
            with st.spinner("🔄 Analyzing and finding similar apps..."):
                recommendations = recommend_apps_faiss(
                    form_data,
                    recommender_system,
                    n=n_recommendations,
                    min_rating=min_rating
                )
                
                if not recommendations.empty:
                    st.session_state.recommendations = recommendations
                    st.session_state.form_data = form_data
                    st.session_state.recommendations_made = True
                else:
                    st.warning("No apps found matching your criteria. Try adjusting the filters.")

# ============================================================================
# DISPLAY RECOMMENDATIONS
# ============================================================================

if st.session_state.get('recommendations_made', False):
    recommendations = st.session_state.get('recommendations')
    
    if recommendations is None or recommendations.empty:
        st.info("No recommendations to display.")
    else:
        st.markdown("---")
        st.markdown("## 📱 Recommended Apps")
        
        if 'search_query' in st.session_state:
            st.markdown(f"**Apps similar to:** *{st.session_state.search_query}*")
        
        st.markdown(f"Found **{len(recommendations)}** similar apps")
        
        # Tabs for different views
        tab1, tab2, tab3 = st.tabs(["📋 Detailed List", "📊 Comparison Table", "🎯 Key Insights"])
        
        # ========== TAB 1: DETAILED LIST ==========
        
        with tab1:
            for idx, row in recommendations.iterrows():
                similarity_pct = row.get('Similarity', 0) * 100
                
                # Color based on similarity
                if similarity_pct >= 90:
                    color = COLORS['success']
                elif similarity_pct >= 75:
                    color = COLORS['accent']
                elif similarity_pct >= 60:
                    color = COLORS['warning']
                else:
                    color = COLORS['secondary']
                
                col1, col2 = st.columns([1, 4])
                
                with col1:
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, {color}, {COLORS['primary']});
                        padding: 1.5rem;
                        border-radius: 12px;
                        text-align: center;
                        color: white;
                    ">
                        <div style="font-size: 2rem; font-weight: bold;">{similarity_pct:.0f}%</div>
                        <div style="font-size: 0.9rem; margin-top: 0.5rem;">Match</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Build badge list
                    badges = []
                    if row.get('Free', False):
                        badges.append("🆓 Free")
                    if row.get('Ad_Supported', False):
                        badges.append("📢 Ads")
                    if row.get('In_App_Purchases', False):
                        badges.append("💰 IAP")
                    if row.get('Editors_Choice', False):
                        badges.append("🏆 Editor's Choice")
                    
                    badges_html = ' '.join([f'<span style="background: rgba(59, 130, 246, 0.2); padding: 0.3rem 0.6rem; border-radius: 4px; color: #93C5FD; font-size: 0.8rem; margin-right: 0.3rem;">{badge}</span>' for badge in badges])
                    
                    html_block = f"""<div style="background: rgba(30, 41, 59, 0.5);
                        padding: 1.5rem;
                        border-radius: 10px;
                        border-left: 4px solid {color};">
                        <h3 style="margin: 0 0 0.5rem 0; color: #F1F5F9;">{row['App_Name']}</h3>
                        <p style="margin: 0 0 1rem 0; color: #94A3B8; font-size: 0.9rem;">📂 {row['Category']}</p>
                        <div style="margin-bottom: 0.5rem;">{badges_html}</div>
                        <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                            <span style="color: #F1F5F9;">⭐ {row['Rating']:.1f}</span>
                            <span style="color: #94A3B8;">💬 {format_number(row['Rating_Count'])} reviews</span>
                            <span style="color: #94A3B8;">📊 {format_number(row['Installs_Central'])} installs</span>
                            <span style="color: #94A3B8;">💾 {row['Size_MB']:.0f}MB</span>
                        </div>
                    </div>"""

                    st.markdown(html_block, unsafe_allow_html=True)
        
        # ========== TAB 2: COMPARISON TABLE ==========
        with tab2:
            st.markdown("### 📊 Quick Comparison")
            
            # Prepare display dataframe
            display_df = recommendations[['App_Name', 'Category', 'Rating', 
                                         'Rating_Count', 'Installs_Central', 
                                         'Size_MB', 'Similarity']].copy()
            
            # Format numbers
            display_df['Rating_Count'] = display_df['Rating_Count'].apply(format_number)
            display_df['Installs_Central'] = display_df['Installs_Central'].apply(format_number)
            display_df['Size_MB'] = display_df['Size_MB'].apply(lambda x: f"{x:.0f}MB")
            display_df['Similarity'] = display_df['Similarity'].apply(lambda x: f"{x*100:.1f}%")
            
            # Rename columns
            display_df.columns = ['App Name', 'Category', 'Rating', 'Reviews', 
                                 'Installs', 'Size', 'Similarity']
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # ========== TAB 3: KEY INSIGHTS ==========
        with tab3:
            st.markdown("### 🎯 Key Success Patterns")
            
            # Analyze top recommendations
            top_3 = recommendations.head(3)
            
            # Average metrics
            avg_rating = top_3['Rating'].mean()
            avg_reviews = top_3['Rating_Count'].mean()
            avg_installs = top_3['Installs_Central'].mean()
            avg_size = top_3['Size_MB'].mean()
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Avg Rating", f"{avg_rating:.2f} ⭐")
            with col2:
                st.metric("Avg Reviews", format_number(avg_reviews))
            with col3:
                st.metric("Avg Installs", format_number(avg_installs))
            with col4:
                st.metric("Avg Size", f"{avg_size:.0f}MB")
            
            st.markdown("---")
            
            # Monetization insights
            st.markdown("### 💰 Monetization Strategies")
            
            if all(col in recommendations.columns for col in ['Free', 'Ad_Supported', 'In_App_Purchases']):
                free_pct = (recommendations['Free'].sum() / len(recommendations)) * 100
                ads_pct = (recommendations['Ad_Supported'].sum() / len(recommendations)) * 100
                iap_pct = (recommendations['In_App_Purchases'].sum() / len(recommendations)) * 100
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Free Apps", f"{free_pct:.0f}%")
                with col2:
                    st.metric("Ad-Supported", f"{ads_pct:.0f}%")
                with col3:
                    st.metric("In-App Purchases", f"{iap_pct:.0f}%")
            
            st.markdown("---")
            
            # Top performer highlight
            st.markdown("### 🌟 Top Recommendation")
            
            top_app = recommendations.iloc[0]
            
            st.markdown(f"""
            <div style="
                background: linear-gradient(145deg, {COLORS['accent']}, {COLORS['success']});
                padding: 2rem;
                border-radius: 12px;
                color: white;
                margin-bottom: 1rem;
            ">
                <h3 style="margin: 0 0 1rem 0;">{top_app['App_Name']}</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem;">
                    <div>
                        <div style="font-size: 0.9rem; opacity: 0.8;">Similarity</div>
                        <div style="font-size: 2rem; font-weight: bold;">{top_app.get('Similarity', 0)*100:.0f}%</div>
                    </div>
                    <div>
                        <div style="font-size: 0.9rem; opacity: 0.8;">Rating</div>
                        <div style="font-size: 2rem; font-weight: bold;">{top_app['Rating']:.1f} ⭐</div>
                    </div>
                    <div>
                        <div style="font-size: 0.9rem; opacity: 0.8;">Installs</div>
                        <div style="font-size: 2rem; font-weight: bold;">{format_number(top_app['Installs_Central'])}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Reset button
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("🔄 New Search", use_container_width=True):
                st.session_state.recommendations_made = False
                st.session_state.recommendations = None
                if 'search_query' in st.session_state:
                    del st.session_state.search_query
                if 'form_data' in st.session_state:
                    del st.session_state.form_data
                st.rerun()

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748B; font-size: 0.9rem;'>
    <p><strong>Powered by Facebook AI Similarity Search (FAISS)</strong></p>
    <p>Content-based recommendations using cosine similarity and normalized features</p>
    <p>Results based on app features: category, ratings, engagement, and performance metrics</p>
</div>
""", unsafe_allow_html=True)
