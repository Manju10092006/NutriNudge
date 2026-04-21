document.addEventListener('DOMContentLoaded', () => {
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    const contextForm = document.getElementById('contextForm');
    const resultsPanel = document.getElementById('resultsPanel');
    const loadingState = document.getElementById('loadingState');
    
    // Analyzer Form Submit
    contextForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Show loading state
        const analyzerContainer = document.querySelector('.analyzer-container');
        loadingState.style.display = 'flex';
        resultsPanel.style.display = 'none';
        
        // Gather data
        const data = {
            mood: document.getElementById('mood').value,
            sleep: document.getElementById('sleep').value,
            hunger: document.getElementById('hunger').value,
            goal: document.getElementById('goal').value,
            timeOfDay: document.getElementById('timeOfDay').value,
            hydration: document.getElementById('hydration').value,
            activity: document.getElementById('activity').value,
            budget: document.getElementById('budget').value
        };

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            // Artificial delay for "AI processing" effect
            setTimeout(() => {
                loadingState.style.display = 'none';
                updateResultsUI(result);
                resultsPanel.style.display = 'block';
                
                // Scroll to results on mobile
                if (window.innerWidth < 900) {
                    resultsPanel.scrollIntoView({ behavior: 'smooth' });
                }
            }, 1200);
            
        } catch (error) {
            console.error('Error analyzing context:', error);
            loadingState.style.display = 'none';
            alert("Error connecting to intelligence engine. Please try again.");
        }
    });

    function updateResultsUI(data) {
        // Animate circular score
        const scoreCircle = document.getElementById('scoreCircle');
        const scoreText = document.getElementById('scoreText');
        
        // Stroke dasharray format: "value, 100"
        setTimeout(() => {
            scoreCircle.setAttribute('stroke-dasharray', `${data.score}, 100`);
            // Color based on score
            if(data.score >= 80) scoreCircle.style.stroke = 'var(--risk-low)';
            else if(data.score >= 50) scoreCircle.style.stroke = 'var(--risk-med)';
            else scoreCircle.style.stroke = 'var(--risk-high)';
        }, 100);
        
        // Animate number count up
        animateValue(scoreText, 0, data.score, 1000);

        // Update Risk Meter
        const riskFill = document.getElementById('riskFill');
        const riskText = document.getElementById('riskText');
        
        setTimeout(() => {
            riskFill.style.width = `${data.craving_risk}%`;
            if(data.craving_risk >= 70) riskFill.style.background = 'var(--risk-high)';
            else if(data.craving_risk >= 40) riskFill.style.background = 'var(--risk-med)';
            else riskFill.style.background = 'var(--risk-low)';
        }, 100);
        
        riskText.textContent = `${data.craving_risk}%`;

        // Update Recommendations
        document.getElementById('recMeal').textContent = data.meal;
        document.getElementById('recSwap').textContent = data.swap;
        document.getElementById('recHydration').textContent = data.hydration;
        document.getElementById('recReason').textContent = data.reason;
        
        // Update Streak
        const streakBadge = document.getElementById('streakBadge');
        streakBadge.textContent = data.streak_message;
        
        if (data.score >= 85) {
            streakBadge.style.background = 'rgba(16, 185, 129, 0.1)';
            streakBadge.style.color = 'var(--accent)';
            streakBadge.style.borderColor = 'rgba(16, 185, 129, 0.2)';
        } else if (data.score >= 60) {
            streakBadge.style.background = 'rgba(59, 130, 246, 0.1)';
            streakBadge.style.color = '#3b82f6';
            streakBadge.style.borderColor = 'rgba(59, 130, 246, 0.2)';
        } else {
            streakBadge.style.background = 'rgba(239, 68, 68, 0.1)';
            streakBadge.style.color = '#ef4444';
            streakBadge.style.borderColor = 'rgba(239, 68, 68, 0.2)';
        }
    }

    function animateValue(obj, start, end, duration) {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            obj.innerHTML = Math.floor(progress * (end - start) + start);
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    }

    // Chatbot Logic
    const chatInput = document.getElementById('chatInput');
    const sendChatBtn = document.getElementById('sendChatBtn');
    const chatWindow = document.getElementById('chatWindow');

    async function sendChatMessage() {
        const message = chatInput.value.trim();
        if (!message) return;

        // Add user message to UI
        addMessageToChat(message, 'user-msg');
        chatInput.value = '';

        // Add loading indicator
        const loadingId = 'loading-' + Date.now();
        addMessageToChat('...', 'ai-msg', loadingId);

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message })
            });
            const data = await response.json();
            
            // Remove loading indicator and add real response
            document.getElementById(loadingId).remove();
            addMessageToChat(data.reply, 'ai-msg');
            
        } catch (error) {
            console.error('Chat error:', error);
            document.getElementById(loadingId).remove();
            addMessageToChat('Sorry, I am having trouble connecting to my neural network.', 'ai-msg');
        }
    }

    function addMessageToChat(text, className, id = null) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `chat-msg ${className}`;
        if (id) msgDiv.id = id;
        
        const p = document.createElement('p');
        p.textContent = text;
        msgDiv.appendChild(p);
        
        chatWindow.appendChild(msgDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    sendChatBtn.addEventListener('click', sendChatMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendChatMessage();
    });
});
