# 📱 AppVision Analytics - Complete Web Application

> **Predict mobile app performance with data-driven insights**

A beautiful, production-ready Streamlit web application for predicting app install success, classifying app performance tiers, and discovering similar successful competitors.

## 🎯 Features

### 1. **📊 Install Value Prediction (Regressor)**
- Predict the exact number of app installs
- 75.2% R² accuracy with Random Forest model
- Real-time input validation and feedback
- Personalized recommendations based on your app profile
- Feature importance visualization

### 2. **🎯 Install Tier Classification (Classifier)**
- Classify apps into 4 performance tiers:
  - 🔹 Low Performance (0-10K installs)
  - 🟡 Emerging (10K-100K installs)
  - 🟢 Popular (100K-1M installs)
  - 🔥 Viral (1M+ installs)
- 96.5% classification accuracy with XGBoost
- Tier-specific growth strategies
- Confidence visualization with probabilities
- Growth roadmap to next tier

### 3. **💡 Competitive App Recommender**
- Find similar successful apps
- Benchmark against competitors
- Learn from top performers
- Content-based similarity matching
- Actionable insights and strategies

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip or conda package manager

### Installation

1. **Clone or download the project**
```bash
cd appvision_predictor
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Add your models**
Place your trained models in the `models/` directory:
```
models/
├── regressor_model.pkl      # Random Forest regressor
├── classifier_model.pkl     # XGBoost classifier
└── recommender_model.pkl    # Recommendation system
```

5. **Run the app**
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📁 Project Structure

```
appvision_predictor/
│
├── app.py                          # Main home page
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── SETUP-GUIDE.md                  # Detailed setup instructions
│
├── pages/
│   ├── 1_📊_Regressor.py          # Install value prediction
│   ├── 2_🎯_Classifier.py         # Install tier classification
│   └── 3_💡_Recommender.py        # Recommendation system
│
├── models/
│   ├── regressor_model.pkl
│   ├── classifier_model.pkl
│   └── recommender_model.pkl
│
└── utils/
    ├── __init__.py
    ├── config.py                   # Configuration & constants
    ├── styling.py                  # CSS & UI design
    └── helpers.py                  # Helper functions
```

## 🎨 Design Features

### Dark Modern Theme
- Professional navy/blue color palette
- Smooth animations and transitions
- Responsive layout for all screen sizes
- Accessible typography with Inter font

### Interactive Components
- Real-time input validation
- Contextual feedback messages
- Interactive charts with Plotly
- Progress indicators
- Status badges

### Mobile Friendly
- Optimized for mobile and desktop
- Touch-friendly buttons and controls
- Responsive column layouts

## 📊 Input Features

### Core Features (Used by All Models)

| Feature | Type | Range | Importance |
|---------|------|-------|-----------|
| Rating Quality Score | Slider | 1.0 - 5.0 | 15.0% |
| Rating Count | Number | 0 - 10M | 38.3% |
| App Age Days | Number | 1 - 3650 | 5.4% |
| Size MB | Slider | 1.0 - 500.0 | 3.8% |
| Category | Dropdown | 48 options | 2.0% |
| Free | Radio | Yes/No | 1.5% |
| Ad Supported | Radio | Yes/No | 1.0% |
| In-App Purchases | Radio | Yes/No | 1.0% |
| Editors Choice | Radio | Yes/No | 0.5% |

**Calculated Features:**
- Rating Density = Rating Count / App Age Days (47.5% importance)

## 🔧 Customization

### Update Model Paths
Edit the model loading functions in each page:

```python
# In 1_📊_Regressor.py (line ~50)
model_path = "models/your_regressor_model.pkl"

# In 2_🎯_Classifier.py (line ~50)
model_path = "models/your_classifier_model.pkl"

# In 3_💡_Recommender.py (line ~50)
recommender_path = "models/your_recommender_model.pkl"
```

### Modify Color Scheme
Edit `utils/config.py`:

```python
COLORS = {
    "primary": "#1E3A8A",      # Your primary color
    "secondary": "#3B82F6",    # Your secondary color
    "accent": "#10B981",       # Your accent color
    # ... more colors
}
```

### Update Model Metrics
Edit `utils/config.py` in `MODEL_METRICS` dictionary:

```python
MODEL_METRICS = {
    "regressor": {
        "r2_score": 0.752,     # Your model's R² score
        "rmse": 0.234,         # Your RMSE
        "mae": 0.189,          # Your MAE
        "accuracy": "75.2%"
    },
    # ... more metrics
}
```

### Add/Remove Features
Edit `REGRESSION_FEATURES` in `utils/config.py` to customize which features are shown.

## 🤖 Model Requirements

Your models should accept pandas DataFrames with these columns:

### Input Format
```python
{
    'Rating_Count': int,
    'Size_MB': float,
    'Rating_Density': float,
    'Ad_Supported': int (0 or 1),
    'Price_USD': float,
    'Rating_Quality_Score': float (1-5),
    'In_App_Purchases': int (0 or 1),
    'Editors_Choice': int (0 or 1),
    'Category': str,
    'App_Age_Days': int,
    'Free': int (0 or 1)
}
```

### Output Format

**Regressor:**
```python
prediction: float  # Predicted install count
```

**Classifier:**
```python
prediction: int    # Predicted tier (0, 1, 2, or 3)
probabilities: array  # Optional - confidence for each class
```

## 📝 Usage Guide

### Regressor Page (📊)
1. Enter your app's rating quality score
2. Specify number of user ratings
3. Select app category and monetization strategy
4. Click "Predict App Installs"
5. Review predicted install count and recommendations

### Classifier Page (🎯)
1. Enter same app details as regressor
2. Click "Classify App Tier"
3. View tier classification and confidence scores
4. Review tier-specific growth strategies
5. Check progress roadmap to next tier

### Recommender Page (💡)
1. Describe your app's features
2. Adjust recommendation settings
3. Click "Find Similar Apps"
4. Compare with top performers
5. View action plan to improve your app

## 🐛 Troubleshooting

### Issue: "Module not found" error
**Solution:**
```bash
# Verify you're in the project root
cd appvision_predictor

# Clear cache and reinstall
pip install --force-reinstall -r requirements.txt
```

### Issue: Model file not found
**Solution:**
1. Verify model files exist in `models/` directory
2. Check file names match exactly in code
3. Ensure proper file permissions

### Issue: CSS not loading
**Solution:**
```bash
# Clear Streamlit cache
streamlit cache clear

# Restart app
streamlit run app.py

# Hard refresh browser (Ctrl+Shift+R or Cmd+Shift+R)
```

### Issue: Page navigation not working
**Solution:**
Verify folder structure:
```
pages/
├── 1_📊_Regressor.py
├── 2_🎯_Classifier.py
└── 3_💡_Recommender.py
```

The emoji prefix and underscore are important!

## 📊 Data Science Background

Models were trained on **2 million+ apps** from Google Play Store with:
- **Regression Model**: Random Forest
  - 75.2% R² Score
  - Predicts install count (0-10B range)
  
- **Classification Model**: XGBoost
  - 96.5% Accuracy
  - 4-class install tier prediction
  
- **Recommender System**: Content-Based
  - 85% Precision@10
  - Similar app discovery

## 🔐 Privacy & Data

- All predictions run locally on your machine
- No data sent to external servers
- Session-based data (cleared on browser close)
- No user tracking or analytics

## 🚀 Deployment

### Deploy to Streamlit Cloud
```bash
# Install Streamlit CLI
pip install streamlit

# Create account at https://streamlit.io
# Connect GitHub repo
# Select branch and main file (app.py)
```

### Deploy to Heroku
```bash
# Create Heroku app
heroku create your-app-name

# Deploy
git push heroku main
```

### Deploy Locally with Docker
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

## 📈 Performance Tips

1. **Cache Models**: Models are cached using `@st.cache_resource`
2. **Optimize Predictions**: Pre-process features for faster inference
3. **Limit History**: Clear old sessions to save memory
4. **Use CDN**: For production deployments

## 🛠️ Development

### Adding New Features
1. Update `utils/config.py` with new feature definitions
2. Add input widget in relevant page
3. Update helper functions if needed
4. Test with sample data

### Updating Styling
Edit CSS in `utils/styling.py`:
- Modify color variables in `:root`
- Update component styles
- Test across devices

## 📚 Dependencies

- **streamlit** (1.28.0+) - Web framework
- **pandas** (2.0.0+) - Data processing
- **numpy** (1.24.0+) - Numerical computing
- **scikit-learn** (1.3.0+) - ML algorithms
- **xgboost** (2.0.0+) - Gradient boosting
- **joblib** (1.3.0+) - Model serialization
- **plotly** (5.17.0+) - Interactive charts

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io)
- ML models trained on [Google Play Store Data](https://www.kaggle.com/datasets/lava18/google-play-store-apps)
- Inspired by mobile app development best practices

## 📞 Support & Resources

- **Streamlit Docs**: https://docs.streamlit.io
- **Pandas Docs**: https://pandas.pydata.org/docs/
- **Scikit-learn**: https://scikit-learn.org/stable/
- **XGBoost**: https://xgboost.readthedocs.io/

## 🎉 Ready to Launch?

```bash
# Start the application
streamlit run app.py

# Navigate to http://localhost:8501
# Enjoy! 🚀
```

---

**Made with ❤️ by AppVision Analytics Team**

© 2025 AppVision Analytics | All Rights Reserved
