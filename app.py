from flask import Flask, request, jsonify, render_template
import re
import random

app = Flask(__name__)

# --- Behavior Intelligence Engine Logic ---

def calculate_score(context):
    """Calculates health readiness score (0-100)."""
    score = 80
    
    sleep = float(context.get("sleep", 7))
    if sleep < 6:
        score -= 15
    elif sleep >= 7:
        score += 10
        
    mood = context.get("mood", "neutral").lower()
    if mood in ["stressed", "sad", "anxious"]:
        score -= 10
    elif mood in ["happy", "energetic"]:
        score += 10
        
    hydration = context.get("hydration", "moderate").lower()
    if hydration == "low":
        score -= 10
    elif hydration == "high":
        score += 5
        
    activity = context.get("activity", "sedentary").lower()
    if activity in ["active", "intense"]:
        score += 10
        
    return max(0, min(100, score))

def predict_craving_risk(context):
    """Outputs percentage risk of junk-food relapse."""
    risk = 20  # Base risk
    
    sleep = float(context.get("sleep", 7))
    if sleep < 6:
        risk += 25
        
    mood = context.get("mood", "neutral").lower()
    if mood == "stressed":
        risk += 30
        
    time_of_day = context.get("timeOfDay", "afternoon").lower()
    if time_of_day == "late night":
        risk += 20
        
    hydration = context.get("hydration", "moderate").lower()
    if hydration == "low":
        risk += 15
        
    return max(0, min(100, int(risk)))

def recommend_meal(context):
    """Chooses best action/meal for current user state."""
    goal = context.get("goal", "maintain").lower()
    budget = context.get("budget", "medium").lower()
    activity = context.get("activity", "sedentary").lower()
    time_of_day = context.get("timeOfDay", "afternoon").lower()
    
    if activity == "intense":
        return "Lean Chicken & Quinoa Protein Bowl"
    elif budget == "low" and goal == "fat loss":
        return "Spiced Lentil Soup with a side of Greens"
    elif goal == "fat loss":
        return "Grilled Salmon with Asparagus"
    elif time_of_day == "late night":
        return "Greek Yogurt with Berries (Calming & Satiating)"
    elif time_of_day == "morning":
        return "Oatmeal with Chia Seeds and Almonds"
    
    return "Balanced Turkey Wrap with Mixed Greens"

def recommend_swap(context):
    """Provides a healthier alternative."""
    time_of_day = context.get("timeOfDay", "afternoon").lower()
    mood = context.get("mood", "neutral").lower()
    
    if time_of_day == "late night":
        return "Instead of Ice Cream ➔ Try Frozen Grapes or Dark Chocolate"
    if mood == "stressed":
        return "Instead of Chips ➔ Try Air-popped Popcorn with Nutritional Yeast"
        
    return "Instead of Sugary Soda ➔ Try Sparkling Water with Fresh Lime"

def generate_reason(context):
    """Short scientific explanation for the recommendation."""
    sleep = float(context.get("sleep", 7))
    mood = context.get("mood", "neutral").lower()
    
    if sleep < 6:
        return "Lack of sleep spikes ghrelin (hunger hormone). High-protein, fiber-rich meals prevent sugar crashes today."
    if mood == "stressed":
        return "Stress increases cortisol, driving sugar cravings. Opting for complex carbs keeps blood sugar stable."
        
    return "This balanced choice provides sustained energy without causing a mid-day insulin spike."

def generate_streak_message(score):
    """Motivational habit streak."""
    if score >= 85:
        return "🔥 3-Day Optimal Streak! Your metabolism is primed."
    elif score >= 60:
        return "💪 Solid day. Keep hydrating to hit peak performance."
    return "⚠️ Body needs recovery. Prioritize sleep and water today."

def chat_reply(message):
    """Conversational Nutrition Coach logic."""
    msg = message.lower()
    if re.search(r'\b(protein)\b', msg):
        return "For optimal protein synthesis, aim for 1.6-2.2g per kg of body weight daily. Good sources: eggs, chicken, lentils, Greek yogurt."
    elif re.search(r'\b(water|hydrate)\b', msg):
        return "Hydration is key! Drink a glass of water first thing in the morning. It boosts metabolism and reduces false hunger signals."
    elif re.search(r'\b(sugar|sweet)\b', msg):
        return "Sugar cravings often mean you need more protein or are dehydrated. Try having a glass of water and a handful of almonds first."
    elif re.search(r'\b(sleep)\b', msg):
        return "Poor sleep drastically reduces your ability to make healthy choices. Try to stop eating 3 hours before bed."
    else:
        return "I'm your NutriNudge AI coach. I analyze your current state to give precise behavioral advice. How are you feeling right now?"

# --- Routes ---

@app.route('/')
def home():
    """Serves the main application UI."""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Core intelligence endpoint."""
    context = request.json or {}
    
    score = calculate_score(context)
    risk = predict_craving_risk(context)
    meal = recommend_meal(context)
    swap = recommend_swap(context)
    reason = generate_reason(context)
    streak = generate_streak_message(score)
    
    hydration_action = "Drink 500ml of water right now." if context.get("hydration") == "low" else "Keep sipping water steadily."
    
    return jsonify({
        "score": score,
        "craving_risk": risk,
        "meal": meal,
        "swap": swap,
        "hydration": hydration_action,
        "reason": reason,
        "streak_message": streak
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Conversational endpoint."""
    data = request.json or {}
    message = data.get("message", "")
    reply = chat_reply(message)
    
    return jsonify({"reply": reply})

@app.route('/health', methods=['GET'])
def health():
    """Healthcheck for Cloud Run."""
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    # Use PORT environment variable provided by Cloud Run
    import os
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
