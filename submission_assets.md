# Hackathon Submission Assets

## 1. Submission Description
**Project Name:** NutriNudge AI  
**Tagline:** Eat Better. Live Smarter.

**Describe the updates made in the deployed version:**  
"NutriNudge AI is a proactive health intelligence platform. We built a Context Engine using Python Flask and behavioral science logic to predict unhealthy eating moments based on mood, sleep, hydration, and time of day. Our deployed version features a premium, responsive frontend with a 24/7 AI conversational nutrition coach and a real-time Craving Risk Predictor. The application is fully optimized, container-ready, and deployed seamlessly on Google Cloud Run."

## 2. GitHub Push Commands
Run these commands to push the project to your repository:
```bash
git init
git add .
git commit -m "Initial commit: NutriNudge AI Hackathon Submission"
git branch -M main
git remote add origin <YOUR_GITHUB_REPO_URL>
git push -u origin main
```

## 3. Google Cloud Run Deploy Commands
Execute this from the project root using the Google Cloud CLI:
```bash
gcloud run deploy nutrinudge-ai \
  --source . \
  --port 8080 \
  --allow-unauthenticated \
  --region us-central1
```

## 4. 2-Minute Demo Script Flow
**[0:00 - 0:15] The Hook:**
"Most calorie trackers fail because they tell you what you ate *after* you made a bad decision. NutriNudge AI predicts your cravings *before* they happen. Let me show you."

**[0:15 - 0:45] The Context Engine:**
"Here on our dashboard, I'm going to input a high-risk scenario. Let's say I'm a stressed student, I only got 5 hours of sleep, it's late at night, and I'm hungry. Look at what happens."
*(Click "Generate Intelligence")*

**[0:45 - 1:15] The Results:**
"The system instantly identifies a **High Craving Risk**. But instead of generic advice, it gives me a scientific reason: lack of sleep spikes ghrelin. It then gives me a smart swap that fits my low budget, alongside a hydration protocol. Notice the habit streak adapting to keep me motivated."

**[1:15 - 1:45] AI Chat Coach:**
"If I need quick advice, our 24/7 NutriCoach AI is ready. I can ask, 'Why do I crave sugar right now?' and it immediately provides scientifically backed advice."

**[1:45 - 2:00] Deployment & Polish:**
"The entire platform is built with a lightweight Python Flask backend and a modern UI, fully deployed on Google Cloud Run for infinite scalability. Thank you!"

## 5. Last-Minute Polish Checklist
- [x] Ensure `requirements.txt` has `gunicorn`.
- [x] Confirm `app.py` uses `os.environ.get('PORT', 8080)` to bind the port.
- [x] Check mobile responsiveness of the UI.
- [x] Verify API endpoints return correctly formatted JSON.
- [x] Confirm `.gitignore` is present to keep the repo clean.
