import pytest
import sys
import os

# Ensure the app module can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, calculate_score, predict_craving_risk

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test that the home page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"NutriNudge AI" in response.data

def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}

def test_analyze_endpoint(client):
    """Test the core analyze API with sample context."""
    data = {
        "mood": "stressed",
        "sleep": "5",
        "hunger": "high",
        "goal": "fat loss",
        "timeOfDay": "late night",
        "hydration": "low",
        "activity": "sedentary",
        "budget": "low"
    }
    response = client.post('/analyze', json=data)
    assert response.status_code == 200
    
    json_data = response.json
    assert "score" in json_data
    assert "craving_risk" in json_data
    assert "meal" in json_data
    
    # Low sleep, stressed, low hydration should result in a lower score and high risk
    assert json_data["score"] < 80
    assert json_data["craving_risk"] > 50

def test_chat_endpoint(client):
    """Test the chat API."""
    response = client.post('/chat', json={"message": "I need some protein advice."})
    assert response.status_code == 200
    assert "protein" in response.json["reply"].lower()

def test_score_calculation_bounds():
    """Ensure the score stays between 0 and 100."""
    terrible_context = {
        "mood": "stressed", "sleep": "2", "hydration": "low", "activity": "sedentary"
    }
    great_context = {
        "mood": "happy", "sleep": "9", "hydration": "high", "activity": "intense"
    }
    
    assert 0 <= calculate_score(terrible_context) <= 100
    assert 0 <= calculate_score(great_context) <= 100

def test_risk_calculation_bounds():
    """Ensure craving risk stays between 0 and 100."""
    terrible_context = {
        "mood": "stressed", "sleep": "2", "hydration": "low", "timeOfDay": "late night"
    }
    great_context = {
        "mood": "happy", "sleep": "9", "hydration": "high", "timeOfDay": "morning"
    }
    
    assert 0 <= predict_craving_risk(terrible_context) <= 100
    assert 0 <= predict_craving_risk(great_context) <= 100
