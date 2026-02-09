# Setup and Deployment Guide

## Quick Start

This application can run in two ways: using Streamlit directly or using Docker (recommended for recipients).

---

## Prerequisites

**Option 1 - Streamlit:**
- Python 3.9+
- pip

**Option 2 - Docker (Recommended):**
- Docker Desktop only

---

## Running with Docker (Recommended)

### Install Docker Desktop

Download from: https://www.docker.com/products/docker-desktop

### Start Application

```bash
cd 1.DataNest_Assignment
docker-compose up
```

Open browser: `http://localhost:8501`

### Stop Application

```bash
docker-compose down
```

---

## Running with Streamlit

### Install Dependencies

```bash
cd 1.DataNest_Assignment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Start Application

```bash
streamlit run app.py
```

Open browser: `http://localhost:8501`

### Stop Application

Press `Ctrl+C` in terminal

---

## Project Structure

```
1.DataNest_Assignment/
├── app.py                    # Streamlit web application
├── result.csv                # Pre-computed predictions
├── requirements.txt          # Python dependencies
├── Dockerfile                # Container definition
├── docker-compose.yml        # Docker orchestration
├── data/                     # Input data
│   ├── items.csv
│   └── train.csv
│   └── test.csv
├── models/                   # Trained models (optional)
└── sales_forecast_pipeline.ipynb  # ML training notebook
```

---

## Using the Application

1. Open `http://localhost:8501` in browser
2. Select item ID from dropdown (or type to search)
3. Click "Predict Sales"
4. View results:
   - Total predicted sales across all shops
   - Number of shops
   - Top 5 shops breakdown
   - Visualization chart

---

## Dependencies

**requirements.txt:**
```
streamlit==1.30.0
pandas==2.0.3
numpy==1.24.3
```

---

## Troubleshooting

**Port already in use:**
```bash
# Docker: Edit docker-compose.yml, change "8501:8501" to "8502:8501"
# Streamlit: streamlit run app.py --server.port=8502
```

**Docker container won't start:**
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up
```

**Module not found (Streamlit):**
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Cloud Deployment

This Docker container can deploy to:
- **Streamlit Cloud:** Push to GitHub, connect at share.streamlit.io
- **Heroku:** Add Procfile, push to Heroku
- **AWS ECS:** Push image to ECR, create ECS service
- **Google Cloud Run:** Build and deploy container

---

**Last Updated:** February 2026
