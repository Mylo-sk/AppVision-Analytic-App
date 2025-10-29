# utils/config.py
"""
Configuration file for AppVision Analytics Predictor
Contains all constants, feature definitions, and app settings
"""

# ============================================================================
# APP CONFIGURATION
# ============================================================================

APP_TITLE = "AppVision Analytics"
APP_ICON = "📱"
PAGE_LAYOUT = "wide"
INITIAL_SIDEBAR_STATE = "expanded"

# ============================================================================
# COLOR PALETTE
# ============================================================================

COLORS = {
    "primary": "#1E3A8A",        # Deep Blue
    "secondary": "#3B82F6",      # Bright Blue
    "accent": "#10B981",         # Green
    "success": "#059669",        # Dark Green
    "warning": "#F59E0B",        # Orange
    "error": "#EF4444",          # Red
    "background": "#0F172A",     # Dark Navy
    "card_bg": "#1E293B",        # Slightly lighter navy
    "text_primary": "#F1F5F9",   # Off-white
    "text_secondary": "#94A3B8", # Light gray
    "border": "#334155"          # Medium gray
}

# ============================================================================
# MODEL PERFORMANCE METRICS
# ============================================================================

MODEL_METRICS = {
    "regressor": {
        "r2_score": 0.752,
        "rmse": 0.234,
        "mae": 0.189,
        "accuracy": "75.2%"
    },
    "classifier": {
        "accuracy": 0.965,
        "f1_macro": 0.96,
        "precision": 0.967,
        "recall": 0.964,
        "accuracy_display": "96.5%"
    },
    "recommender": {
        "precision_at_10": 0.85,
        "recall_at_10": 0.78,
        "ndcg": 0.82
    }
}

# ============================================================================
# REGRESSION MODEL FEATURES
# ============================================================================

REGRESSION_FEATURES = {
    "Rating_Count": {
        "display_name": "Total Number of Ratings",
        "icon": "📈",
        "type": "number",
        "min": 0,
        "max": 10000000,
        "default": 1000,
        "step": 100,
        "importance": 38.3,
        "description": "Total volume of user reviews. Higher counts indicate stronger market validation.",
        "help_text": "Apps with 10,000+ ratings typically perform better"
    },
    "Rating_Quality_Score": {
        "display_name": "Average User Rating",
        "icon": "⭐",
        "type": "slider",
        "min": 1.0,
        "max": 5.0,
        "default": 3.5,
        "step": 0.1,
        "importance": 15.0,
        "description": "Average rating on a 1-5 scale. Quality signal for user satisfaction.",
        "help_text": "Target 4.0+ for optimal performance",
        "feedback": {
            4.5: ("success", "🎉 Excellent rating!"),
            4.0: ("info", "👍 Good rating"),
            3.5: ("warning", "⚠️ Average rating"),
            0: ("error", "❌ Low rating - needs improvement")
        }
    },
    "App_Age_Days": {
        "display_name": "App Age (Days)",
        "icon": "📅",
        "type": "number",
        "min": 1,
        "max": 3650,
        "default": 365,
        "step": 30,
        "importance": 5.4,
        "description": "Time since initial launch. Older apps have more time to accumulate installs.",
        "help_text": "1 year = 365 days, 2 years = 730 days"
    },
    "Size_MB": {
        "display_name": "App Size (MB)",
        "icon": "💾",
        "type": "slider",
        "min": 1.0,
        "max": 500.0,
        "default": 25.0,
        "step": 5.0,
        "importance": 3.8,
        "description": "Application download size. Smaller apps have better conversion rates.",
        "help_text": "Keep under 100MB for optimal downloads",
        "feedback": {
            50: ("success", "✅ Optimal size"),
            100: ("info", "ℹ️ Acceptable size"),
            500: ("warning", "⚠️ Consider optimizing size")
        }
    },
    "Category": {
        "display_name": "App Category",
        "icon": "📂",
        "type": "selectbox",
        "importance": 2.0,
        "description": "Primary app category. Some categories perform better than others.",
        "help_text": "Photography, Business, and Education show highest growth",
        "options": [
            "Action", "Adventure", "Arcade", "Art & Design", "Auto & Vehicles",
            "Beauty", "Board", "Books & Reference", "Business", "Card", "Casino",
            "Casual", "Comics", "Communication", "Dating", "Education", "Educational",
            "Entertainment", "Events", "Finance", "Food & Drink", "Health & Fitness",
            "House & Home", "Libraries & Demo", "Lifestyle", "Maps & Navigation",
            "Medical", "Music", "Music & Audio", "News & Magazines", "Parenting",
            "Personalization", "Photography", "Productivity", "Puzzle", "Racing",
            "Role Playing", "Shopping", "Simulation", "Social", "Sports", "Strategy",
            "Tools", "Travel & Local", "Trivia", "Video Players & Editors", "Weather", "Word"
        ],
        "default": "Tools"
    },
    "Free": {
        "display_name": "Is the App Free?",
        "icon": "💰",
        "type": "radio",
        "importance": 1.5,
        "description": "Whether app is free to download. Free apps typically have higher install rates.",
        "help_text": "Free apps with IAP often outperform paid apps",
        "options": ["Yes", "No"],
        "default": "Yes"
    },
    "Ad_Supported": {
        "display_name": "Contains Ads?",
        "icon": "📺",
        "type": "radio",
        "importance": 1.0,
        "description": "Whether app displays advertisements for monetization.",
        "help_text": "Ad-supported apps can monetize free users",
        "options": ["Yes", "No"],
        "default": "No"
    },
    "In_App_Purchases": {
        "display_name": "Has In-App Purchases?",
        "icon": "🛒",
        "type": "radio",
        "importance": 1.0,
        "description": "Whether app offers in-app purchase options.",
        "help_text": "IAP provides flexible monetization opportunities",
        "options": ["Yes", "No"],
        "default": "No"
    },
    "Editors_Choice": {
        "display_name": "Editors' Choice?",
        "icon": "🏆",
        "type": "radio",
        "importance": 0.5,
        "description": "Google Play Editors' Choice recognition badge.",
        "help_text": "Editorial selection significantly boosts visibility",
        "options": ["Yes", "No"],
        "default": "No"
    }
}

# ============================================================================
# CLASSIFIER MODEL FEATURES (Same as regression + outputs)
# ============================================================================

CLASSIFIER_FEATURES = REGRESSION_FEATURES.copy()

INSTALL_TIERS = {
    0: {
        "name": "Low Performance",
        "icon": "🔹",
        "color": "#64748B",
        "description": "Low traction in installs and engagement. Focus on marketing and UX improvements.",
        "range": "0 - 10K installs",
        "recommendations": [
            "Increase user acquisition campaigns",
            "Optimize app store presence (ASO)",
            "Gather and respond to user feedback",
            "Improve app quality and reduce bugs"
        ]
    },
    1: {
        "name": "Emerging App",
        "icon": "🟡",
        "color": "#F59E0B",
        "description": "Growing momentum with building audience. Continue engagement strategies.",
        "range": "10K - 100K installs",
        "recommendations": [
            "Focus on user retention programs",
            "Implement referral mechanisms",
            "Enhance core features based on feedback",
            "Increase social media presence"
        ]
    },
    2: {
        "name": "Popular App",
        "icon": "🟢",
        "color": "#10B981",
        "description": "Strong performance with established user base. Scale and optimize.",
        "range": "100K - 1M installs",
        "recommendations": [
            "Scale marketing to new segments",
            "Launch premium features or tiers",
            "Build community engagement",
            "Explore partnership opportunities"
        ]
    },
    3: {
        "name": "Viral App",
        "icon": "🔥",
        "color": "#EF4444",
        "description": "Exceptional viral-level growth. Maintain momentum and expand.",
        "range": "1M+ installs",
        "recommendations": [
            "Expand to international markets",
            "Build robust infrastructure for scale",
            "Launch complementary products",
            "Consider strategic partnerships or funding"
        ]
    }
}

# ============================================================================
# TIPS AND GUIDANCE
# ============================================================================

QUICK_TIPS = [
    "🌟 Encourage ratings early - first 30 days are critical",
    "⚡ Keep app size under 100MB for better conversion",
    "💰 Free apps with IAP often outperform paid apps",
    "📱 Choose category wisely - impacts discoverability",
    "🎯 Track rating density (ratings per day) closely",
    "🚀 Editors' Choice badge can 10x your installs",
    "📊 Regular updates signal active development",
    "💬 Respond to reviews to boost engagement"
]

FEATURE_IMPORTANCE_ORDER = [
    "Rating_Count",
    "Rating_Quality_Score",
    "App_Age_Days",
    "Size_MB",
    "Category",
    "Free",
    "Ad_Supported",
    "In_App_Purchases",
    "Editors_Choice"
]
