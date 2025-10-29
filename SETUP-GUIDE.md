# 📱 AppVision Analytics - Setup Guide

## 🚀 Complete Installation & Running Instructions

### **Step 1: Project Structure**

Create the following folder structure:

```
AppVision Analytics App/
│
├── app.py                    # Main home page
├── requirements.txt          # Python dependencies
├── README.md                 # This file
│
├── pages/                    # Streamlit pages
│   ├── 1_📊_Regressor.py    # Install value prediction
│   ├── 2_🎯_Classifier.py   # Install tier classification
│   └── 3_💡_Recommender.py  # Recommendation system
│
├── models/                   # Machine learning models
│   ├── regressor_model.pkl
│   ├── classifier_model.pkl
│   └── recommender_model.pkl
│
└── utils/                    # Utility modules
    ├── __init__.py
    ├── config.py             # Configuration constants
    ├── styling.py            # CSS and design
    └── helpers.py            # Helper functions
```

---

### **Step 2: Environment Setup**

#### **Option A: Using Virtual Environment (Recommended)**

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### **Option B: Using Conda**

```bash
# Create conda environment
conda create -n appvision python=3.10

# Activate environment
conda activate appvision

# Install dependencies
pip install -r requirements.txt
```

---

### **Step 3: Create `utils/__init__.py`**

Create an empty file to make utils a Python package:

**File: `utils/__init__.py`**
```python
# Empty file - marks utils as a Python package
```

---

### **Step 4: Add Your Model Files**

Place your trained model files in the `models/` directory:

- `regressor_model.pkl` - Your Random Forest regressor
- `classifier_model.pkl` - Your XGBoost classifier  
- `recommender_model.pkl` - Your recommendation system

**Important:** Update the model paths in the page files if your models are named differently.

---

### **Step 5: Running the Application**

```bash
# Make sure you're in the project root directory
cd AppVision Analytics App

# Run the Streamlit app
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

---

## 📋 File-by-File Setup Checklist

### ✅ **1. config.py** (Already created)
Contains all feature definitions, color schemes, and app constants.

### ✅ **2. styling.py** (Already created)
Professional dark-themed CSS with animations and modern UI components.

### ✅ **3. helpers.py** (Already created)
Utility functions for data processing, validation, and recommendations.

### ✅ **4. app.py** (Already created)
Main home page with navigation to all three predictors.

### ✅ **5. 1_📊_Regressor.py** (Already created)
Regressor prediction page - predicts exact number of installs.

### ⏳ **6. 2_🎯_Classifier.py** (To be created)
Classifier prediction page - predicts install tier (Low/Emerging/Popular/Viral).

### ⏳ **7. 3_💡_Recommender.py** (To be created)
Recommendation page - finds similar successful apps.

---

## 🎨 Key Features

### **1. Regressor Page (Install Value Prediction)**
- Predicts exact number of installs
- Real-time input validation and feedback
- Feature importance display
- Personalized recommendations
- 75.2% R² accuracy

### **2. Classifier Page (Install Tier Prediction)** - Coming Next
- 4-tier classification system
- Tier-specific strategies
- Growth roadmap insights
- 96.5% accuracy

### **3. Recommender Page** - Coming Next
- Content-based recommendations
- Similar app discovery
- Competitive analysis
- Strategic benchmarking

---

## 🔧 Customization Guide

### **Update Model Paths**

In `pages/1_📊_Regressor.py`, update line 50:

```python
model_path = "models/regressor_model.pkl"  # Change to your path
```

### **Modify Feature List**

Edit `utils/config.py` to add/remove features from `REGRESSION_FEATURES` dictionary.

### **Change Color Scheme**

Edit the `COLORS` dictionary in `utils/config.py`:

```python
COLORS = {
    "primary": "#1E3A8A",      # Your primary color
    "secondary": "#3B82F6",    # Your secondary color
    "accent": "#10B981",       # Your accent color
    # ... etc
}
```

### **Update Model Metrics**

Edit `MODEL_METRICS` in `utils/config.py` with your actual model performance:

```python
MODEL_METRICS = {
    "regressor": {
        "r2_score": 0.752,     # Your R² score
        "rmse": 0.234,         # Your RMSE
        "mae": 0.189,          # Your MAE
        "accuracy": "75.2%"
    },
    # ... etc
}
```

---

## 🐛 Troubleshooting

### **Problem: "Module not found" error**

**Solution:**
```bash
# Ensure you're in the project root
cd appvision_predictor

# Reinstall dependencies
pip install -r requirements.txt
```

### **Problem: Model file not found**

**Solution:**
1. Check that your model files are in the `models/` directory
2. Verify the file names match in the code
3. Check file permissions

### **Problem: CSS not loading properly**

**Solution:**
1. Clear Streamlit cache: `streamlit cache clear`
2. Restart the app
3. Hard refresh browser (Ctrl+Shift+R or Cmd+Shift+R)

### **Problem: Page navigation not working**

**Solution:**
Ensure your folder structure matches exactly:
```
pages/
  ├── 1_📊_Regressor.py
  ├── 2_🎯_Classifier.py
  └── 3_💡_Recommender.py
```

---

## 📊 Model Input Format

Your models should expect a pandas DataFrame with these columns:

**Regressor & Classifier Input:**
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

---

## 🎯 Next Steps

Now that you have the Regressor page working:

1. ✅ **Test the Regressor page** thoroughly
2. ⏳ **Create the Classifier page** (Step 2)
3. ⏳ **Create the Recommender page** (Step 3)
4. 🎨 **Customize styling** to your brand
5. 📊 **Add data visualizations** (optional)

---

## 💡 Tips for Success

1. **Start Simple**: Test the regressor page first before moving to classifier/recommender
2. **Use Real Models**: Replace placeholder model paths with your actual trained models
3. **Test Thoroughly**: Try various input combinations to ensure validation works
4. **Customize**: Adapt the styling and features to match your specific needs
5. **Monitor Performance**: Check model loading times and optimize if needed

---

## 📞 Support & Resources

- **Streamlit Docs**: https://docs.streamlit.io
- **Pandas Docs**: https://pandas.pydata.org/docs/
- **Scikit-learn**: https://scikit-learn.org/stable/

---

## 🎉 You're Ready!

Your Step 1 (Regressor) is complete! Run the app:

```bash
streamlit run app.py
```

Then navigate to the **📊 Regressor** page and start making predictions!

**Next:** Would you like me to create the **Classifier page (Step 2)** or the **Recommender page (Step 3)**?

---

© 2025 AppVision Analytics | Built with ❤️ and Streamlit
