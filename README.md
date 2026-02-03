# 🎬 Sentiment Analysis API

A Flask REST API that analyzes text sentiment using a custom-trained machine learning model. Built with Python, Flask, SQLite, and scikit-learn.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3-orange)

## 🌟 Features

- **Custom ML Model** — Trained on 50,000 IMDB movie reviews (85% accuracy)
- **REST API** — POST endpoint for sentiment analysis
- **Web Interface** — Clean UI to test predictions
- **SQLite Database** — Stores prediction history
- **Statistics Dashboard** — Track total predictions and sentiment breakdown

## 📸 Screenshots
<img width="1602" height="1113" alt="image" src="https://github.com/user-attachments/assets/b52a1919-833f-449e-a21f-05e477cf063d" />
<img width="981" height="682" alt="image" src="https://github.com/user-attachments/assets/4b429c75-3da0-4052-a138-e770604f83c8" />

### Home Page
- Analyze text form
- Live statistics (total, positive, negative, neutral)
- Recent predictions history

### Result Page
- Sentiment prediction with emoji
- Confidence score
- Back button to analyze more

## 🚀 Quick Start

### Option 1: Run on Replit
[![Run on Replit](https://replit.com/badge/github/Iliofotos/SentimentAnalysisAPI)](https://replit.com/@YOUR_USERNAME/SentimentAnalysisAPI)

### Option 2: Run Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/Iliofotos/SentimentAnalysisAPI.git
   cd SentimentAnalysisAPI
   ```

2. **Install dependencies**
   ```bash
   pip install flask scikit-learn
   ```

3. **Run the app**
   ```bash
   python main.py
   ```

4. **Open browser**
   ```
   http://localhost:5000
   ```

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web interface with form and stats |
| `/analyze` | POST | Analyze text sentiment |
| `/history` | GET | Get recent predictions (JSON) |
| `/stats` | GET | Get prediction statistics (JSON) |

### Example API Usage

```python
import requests

response = requests.post('http://localhost:5000/analyze', 
    data={'text': 'This movie was absolutely fantastic!'})

print(response.json())
# {'text': '...', 'sentiment': 'positive', 'confidence': 0.89}
```

## 🧠 Model Details

| Attribute | Value |
|-----------|-------|
| Algorithm | Multinomial Naive Bayes |
| Vectorizer | TF-IDF (10,000 features) |
| Training Data | IMDB Dataset (50,000 reviews) |
| Accuracy | 85.4% |
| AUC Score | 0.93 |

**Note:** The model performs best on longer text (similar to movie reviews). Short phrases may show ~50% confidence due to insufficient context.

## 📁 Project Structure

```
SentimentAnalysisAPI/
├── main.py                  # Flask application
├── sentiment_model.pkl      # Trained ML model
├── tfidf_vectorizer.pkl     # TF-IDF vectorizer
├── predictions.db           # SQLite database (auto-generated)
├── pyproject.toml           # Dependencies
└── README.md
```

## 🛠️ Technologies Used

- **Backend:** Python, Flask
- **ML:** scikit-learn, Multinomial Naive Bayes, TF-IDF
- **Database:** SQLite
- **Frontend:** HTML, CSS (inline)

## 📂 Related Projects

- [IMDB Sentiment Analysis](https://github.com/Iliofotos/IMDBSentimentAnalysis) — The notebook where this model was trained
- [Credit Card Default Prediction](https://github.com/Iliofotos/CreditCardDefaultPrediction) — ML classification project

## 👤 Author

**Iliofotos Iliofotou**

- GitHub: [@Iliofotos](https://github.com/Iliofotos)
- LinkedIn: [Iliofotos Iliofotou](https://linkedin.com/in/iliofotos-iliofotou-26244a155)

## 📄 License

This project is open source and available under the MIT License.
