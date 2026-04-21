# 🍃 NutriNudge AI
**Eat Better. Live Smarter.**

NutriNudge AI is a next-generation health intelligence platform that predicts unhealthy eating moments and provides personalized, behavior-based nutrition guidance. 

## 🏆 The Challenge
Most health apps only tell you what you ate *after* you ate it. They are reactive and lack context. NutriNudge AI flips this model by being **proactive**. It uses behavioral science and context (mood, sleep, time of day) to give you smart swaps and guidance *before* a craving takes over.

## ✨ Key Features
- **🧠 Behavior Intelligence Engine**: Uses contextual signals to detect relapse moments.
- **⚡ Craving Risk Predictor**: Outputs a percentage risk of a junk-food relapse.
- **🥗 Smart Meal Recommendations**: Suggests optimal meals or swaps based on your goals and budget.
- **💬 Conversational Nutrition Coach**: An AI assistant ready to answer your nutrition questions 24/7.
- **🔥 Adaptive Habit Streaks**: Encourages consistency with a dynamic scoring system.

## 🏗️ Architecture
- **Frontend**: High-performance Vanilla HTML/CSS/JS with a premium glassmorphism UI.
- **Backend**: Python Flask RESTful API.
- **Deployment**: Configured for seamless scaling on Google Cloud Run.

## 🚀 Local Setup
1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd NutriNudgeAI
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Open `http://localhost:8080` in your browser.

## ☁️ Deploy to Google Cloud Run
1. Ensure you have the [Google Cloud CLI](https://cloud.google.com/sdk/docs/install) installed and authenticated.
2. Run the deployment command:
   ```bash
   gcloud run deploy nutrinudge-ai --source . --port 8080 --allow-unauthenticated
   ```

## 📸 Screenshots
*(Insert placeholders for screenshots of the UI)*
- `[Screenshot: Hero Section]`
- `[Screenshot: Analyzer Dashboard]`
- `[Screenshot: AI Chat Coach]`

## 🗺️ Future Roadmap
- Integration with wearables (Apple Health, Fitbit) for automatic context gathering.
- Personalized recipe generation based on pantry ingredients.
- Social accountability features.
