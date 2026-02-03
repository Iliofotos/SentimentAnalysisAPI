import pickle
import sqlite3

from flask import Flask, jsonify, request

app = Flask(__name__)

with open('sentiment_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('tfidf_vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)


@app.route('/')
def index():
    conn = sqlite3.connect('predictions.db')
    c = conn.cursor()

    c.execute('SELECT COUNT(*) FROM predictions')
    total = c.fetchone()[0]

    c.execute('SELECT sentiment, COUNT(*) FROM predictions GROUP BY sentiment')
    breakdown = dict(c.fetchall())

    c.execute('SELECT * FROM predictions ORDER BY created_at DESC LIMIT 5')
    recent = c.fetchall()

    conn.close()

    positive = breakdown.get('positive', 0)
    negative = breakdown.get('negative', 0)
    neutral = breakdown.get('neutral', 0)

    if recent:
        history_html = "".join(
            f'<div class="history-item">'
            f'<span>{row[1][:50]}...</span>'
            f'<span class="{row[2]}">{row[2]} ({row[3]:.1%})</span>'
            f'</div>' for row in recent)
    else:
        history_html = '<p>No predictions yet</p>'

    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sentiment Analysis API</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background: #f5f5f5;
            }}
            h1 {{
                color: #333;
                text-align: center;
            }}
            .container {{
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }}
            textarea {{
                width: 100%;
                padding: 15px;
                font-size: 16px;
                border: 2px solid #ddd;
                border-radius: 5px;
                resize: vertical;
            }}
            button {{
                background: #4CAF50;
                color: white;
                padding: 15px 30px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
                margin-top: 10px;
            }}
            button:hover {{
                background: #45a049;
            }}
            .stats {{
                display: flex;
                justify-content: space-around;
                text-align: center;
                margin: 20px 0;
            }}
            .stat-box {{
                padding: 20px;
                border-radius: 10px;
                min-width: 100px;
            }}
            .stat-box.total {{ background: #e3f2fd; }}
            .stat-box.positive {{ background: #e8f5e9; }}
            .stat-box.negative {{ background: #ffebee; }}
            .stat-box.neutral {{ background: #fff3e0; }}
            .stat-number {{
                font-size: 32px;
                font-weight: bold;
            }}
            .history {{
                margin-top: 20px;
            }}
            .history-item {{
                padding: 10px;
                border-bottom: 1px solid #eee;
                display: flex;
                justify-content: space-between;
            }}
            .positive {{ color: #4CAF50; }}
            .negative {{ color: #f44336; }}
            .neutral {{ color: #ff9800; }}
        </style>
    </head>
    <body>
        <h1>🎬 Sentiment Analysis API</h1>

        <div class="container">
            <h3>Analyze Text</h3>
            <form action="/analyze" method="POST">
                <textarea name="text" rows="4" placeholder="Enter text to analyze..."></textarea>
                <button type="submit">Analyze Sentiment</button>
            </form>
        </div>

        <div class="container">
            <h3>📊 Statistics</h3>
            <div class="stats">
                <div class="stat-box total">
                    <div class="stat-number">{total}</div>
                    <div>Total</div>
                </div>
                <div class="stat-box positive">
                    <div class="stat-number">{positive}</div>
                    <div>Positive</div>
                </div>
                <div class="stat-box negative">
                    <div class="stat-number">{negative}</div>
                    <div>Negative</div>
                </div>
                <div class="stat-box neutral">
                    <div class="stat-number">{neutral}</div>
                    <div>Neutral</div>
                </div>
            </div>
        </div>

        <div class="container">
            <h3>🕐 Recent Predictions</h3>
            <div class="history">
                {history_html}
            </div>
        </div>
    </body>
    </html>
    '''


def init_db():
    conn = sqlite3.connect('predictions.db')

    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS predictions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT, sentiment TEXT,
                 confidence REAL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'''
              )
    conn.commit()
    conn.close()


@app.route('/stats')
def stats():
    conn = sqlite3.connect('predictions.db')
    c = conn.cursor()

    c.execute('SELECT COUNT(*) FROM predictions')
    total = c.fetchone()[0]

    c.execute('SELECT sentiment, COUNT(*) FROM predictions GROUP BY sentiment')
    breakdown = c.fetchall()

    conn.close()

    return jsonify({'total': total, 'breakdown': breakdown})


@app.route('/analyze', methods=['POST'])
def analyze():

    text = request.form.get('text', '')
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    text_vectorized = vectorizer.transform([text])
    prediction = model.predict(text_vectorized)[0]
    confidence = max(model.predict_proba(text_vectorized)[0])

    sentiment = prediction

    # Save to database
    conn = sqlite3.connect('predictions.db')
    c = conn.cursor()
    c.execute(
        'INSERT INTO predictions (text, sentiment, confidence) VALUES (?, ?, ?)',
        (text, sentiment, confidence))
    conn.commit()
    conn.close()

    # Set color based on sentiment
    if sentiment == 'positive':
        color = '#4CAF50'
        emoji = '😊'
    elif sentiment == 'negative':
        color = '#f44336'
        emoji = '😞'
    else:
        color = '#ff9800'
        emoji = '😐'

    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Result - Sentiment Analysis</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 600px;
                margin: 50px auto;
                padding: 20px;
                background: #f5f5f5;
                text-align: center;
            }}
            .result-box {{
                background: white;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            .emoji {{
                font-size: 64px;
            }}
            .sentiment {{
                font-size: 32px;
                font-weight: bold;
                color: {color};
                margin: 20px 0;
            }}
            .confidence {{
                font-size: 18px;
                color: #666;
            }}
            .text {{
                background: #f5f5f5;
                padding: 15px;
                border-radius: 5px;
                margin: 20px 0;
                font-style: italic;
            }}
            .back-btn {{
                background: #2196F3;
                color: white;
                padding: 15px 30px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
                text-decoration: none;
                display: inline-block;
                margin-top: 20px;
            }}
            .back-btn:hover {{
                background: #1976D2;
            }}
        </style>
    </head>
    <body>
        <div class="result-box">
            <div class="emoji">{emoji}</div>
            <div class="sentiment">{sentiment.upper()}</div>
            <div class="confidence">Confidence: {confidence:.1%}</div>
            <div class="text">"{text[:100]}{"..." if len(text) > 100 else ""}"</div>
            <a href="/" class="back-btn">← Analyze Another</a>
        </div>
    </body>
    </html>
    '''


@app.route('/history')
def history():
    conn = sqlite3.connect('predictions.db')
    c = conn.cursor()
    c.execute('SELECT * FROM predictions ORDER BY created_at DESC LIMIT 20')
    rows = c.fetchall()
    conn.close()

    return jsonify({'predictions': rows})


init_db()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
