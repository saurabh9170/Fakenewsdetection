Fake News Detection System
📌 Project Overview

The Fake News Detection System is a machine learning based web application that predicts whether a given news article is Real or Fake.
The system uses Natural Language Processing (NLP) and Machine Learning algorithms to analyze the text of a news article and classify it accordingly.

With the rapid spread of misinformation on the internet and social media platforms, this system helps users verify the authenticity of news content quickly.

🚀 Features

Detects whether a news article is Fake or Real

Machine Learning based prediction model

User-friendly web interface

Stores prediction history in MySQL database

Login and Register system for users

Fast and accurate prediction

🛠️ Technologies Used
Backend

Python

Flask

Machine Learning

Scikit-learn

Logistic Regression

TF-IDF Vectorizer

Pandas

NumPy

Frontend

HTML

CSS

JavaScript

Database

MySQL

📂 Project Structure
FakeNewsDetection
│
├── app.py                # Flask main application
├── model_training.py     # ML model training script
├── model.pkl             # Trained machine learning model
├── vectorizer.pkl        # TF-IDF vectorizer
│
├── templates
│   ├── login.html
│   ├── register.html
│   ├── home.html
│
├── static
│   ├── style.css
│
└── README.md
⚙️ Installation
1️⃣ Clone the repository
git clone https://github.com/saurabh9170/Fakenewsdetection.git
2️⃣ Go to project directory
cd Fakenewsdetection
3️⃣ Install required libraries
pip install -r requirements.txt
4️⃣ Run the application
python app.py
💻 Usage

Open the web application in browser.

Register a new user account.

Login to the system.

Enter the news text.

Click Predict.

The system will display whether the news is Real or Fake.

📊 Machine Learning Workflow

Data Collection

Data Preprocessing

Text Cleaning

Feature Extraction using TF-IDF

Model Training using Logistic Regression

Model Evaluation

Deployment using Flask

📸 Screenshots

(Add screenshots of your project here)

Example:

Login Page

Register Page

Prediction Page

Result Page

📈 Future Improvements

Improve model accuracy using Deep Learning

Add News URL detection

Deploy on cloud platform

Add API support

👨‍💻 Author

Saurabh Singh

GitHub:
https://github.com/saurabh9170
