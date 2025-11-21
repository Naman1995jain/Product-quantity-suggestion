# 👕 Clothing Production AI Forecaster

## 📌 Overview

This project is an AI-powered application designed to optimize clothing manufacturing schedules. It predicts the suggested production quantity for various clothing items based on the selected month.

The system uses a **Random Forest Regressor** machine learning model trained on historical sales and production data (`data.csv`). It provides a user-friendly web interface built with **Streamlit** to compare AI predictions against historical averages.

---

## 🚀 Features

- **AI Forecasting**: Predicts production quantities for specific months based on learned seasonal patterns
- **Historical Comparison**: Automatically compares AI suggestions with the actual historical average for that month to highlight deviations
- **Interactive Dashboard**: Visualize trends using dynamic charts (Altair) and detailed data tables
- **Robust Handling**: Automatically trains and saves the model if the pre-trained file is missing

---

## 🛠️ Tech Stack

- **Language**: Python 3.x
- **Frontend**: Streamlit
- **Machine Learning**: Scikit-learn (Random Forest)
- **Data Manipulation**: Pandas
- **Visualization**: Altair

---

## 📂 Project Structure

```
clothing-production-forecaster/
├── app.py                          # Main Streamlit application
├── data.csv                        # Historical dataset (Required for training & comparison)
├── clothing_production_model.joblib # Saved AI Model (Generated automatically)
└── README.md                       # Project documentation
```

---

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Step 1: Clone or Download

Clone or download this repository to your local machine:

```bash
git clone https://github.com/yourusername/clothing-production-forecaster.git
cd clothing-production-forecaster
```

### Step 2: Install Required Libraries

Open your terminal or command prompt and run:

```bash
pip install streamlit pandas scikit-learn joblib altair
```

Or use a requirements file:

```bash
pip install -r requirements.txt
```

### Step 3: Prepare Data

Ensure your `data.csv` file is placed in the same directory as `app.py`.

---

## 🏃‍♂️ How to Run

### Start the Application

Run the following command in your terminal:

```bash
streamlit run app.py
```

### Use the Interface

1. A browser window will open automatically (usually at `http://localhost:8501`)
2. Select a **Month** from the sidebar dropdown (e.g., November)
3. Click **"Analyze [Month]"**
4. View the:
   - AI Suggestions
   - Comparison Charts (AI vs History)
   - Detailed Comparison Table

---

## 🧠 How the Model Works

### Algorithm

**Random Forest Regressor** with `n_estimators=100`

### Input Features

- **Month**: Encoded as 1-12
- **Product Name**: Label Encoded

### Target Variable

- **Production Quantity**: Numeric value representing units to produce

### Logic

The model learns the relationship between the time of year and the volume of production required for specific items. For example:
- "Winter Scarves" typically have high production in December
- "Summer T-Shirts" peak in May-June
- Seasonal patterns are automatically detected and used for predictions

---

## 📊 Data Format

The system expects a `data.csv` file with at least the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| `Date` | Date in dd-mm-yyyy format | 15-01-2023 |
| `Month` | Full month name | January, February |
| `Product Name` | Name of clothing item | Formal Shirt, Winter Jacket |
| `Production Quantity` | Number of units produced | 500, 1200 |

### Sample Data Structure

```csv
Date,Month,Product Name,Production Quantity
01-01-2023,January,Winter Jacket,1200
15-01-2023,January,Formal Shirt,800
01-02-2023,February,Casual Pants,950
```

---

## 📈 Model Performance

- The model automatically evaluates itself during training
- Performance metrics are displayed in the console
- Predictions improve with more historical data

---

## 🔧 Troubleshooting

### Common Issues

**Issue**: Model file not found
- **Solution**: The app will automatically train a new model on first run

**Issue**: Data file missing
- **Solution**: Ensure `data.csv` is in the same directory as `app.py`

**Issue**: Import errors
- **Solution**: Verify all dependencies are installed using `pip install -r requirements.txt`

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- Your Name - Initial work

---

## 🙏 Acknowledgments

- Built with Streamlit
- Machine Learning powered by Scikit-learn
- Data visualization using Altair

---

## 📧 Contact

For questions or support, please open an issue in the GitHub repository or contact [namanjain34710@gmail.com]

---