# 📑 Medi-Hack AI HealthBot

## 1. Project Title & Tagline
**Medi-Hack AI HealthBot**  
*Revolutionizing healthcare accessibility through AI on Discord.*

---

## 2. Hackathon Context
**Built for:** Medi-Hacks 2025  
**Theme:** AI for Medical Innovation  
**Track(s):** Telehealth & Remote Care / Mental Health & Wellness

---

## 3. Problem Statement
Millions struggle with accessing healthcare knowledge and preparing for telehealth visits. Users often lack guidance on symptoms, hydration, nutrition, and mental wellness. We need AI-driven tools that make basic healthcare advice more accessible and personalized.

---

## 4. Solution: The Bot
Our Discord bot provides AI-powered health assistance in a simple and interactive way.  
It helps users:

- Track BMI, weight, hydration, and stress
- Check symptoms and get nutrition advice
- Prepare for telehealth consultations
- Receive mental health support  

By combining AI with Discord accessibility, it delivers personalized guidance anytime.

---

## 5. Features (Detailed)
- 🤖 **Symptom Checker** – AI-powered health insights.  
- 🧾 **Telehealth Checklist** – Prepares patients before virtual appointments.  
- 💧 **Hydration Advisor** – Calculates daily water intake based on weight, climate, and activity.  
- ⚖️ **BMI / Weight Tracker** – Monitor trends and progress over time.  
- 😌 **Stress Logging** – Track mental wellness and receive relaxation tips.  
- 🩺 **Health Interview** – Quick AI-guided questionnaire to summarize symptoms.  
- 💊 **Medicine Checker** – Provides info and precautions for medications.  
- 🥦 **Nutrition Advisor** – Suggests diet adjustments for common diseases or general health.  
- 💙 **Mental Health Support** – Encouragement and advice for mood or stress.

---

## 6. Tech Stack
- **Python 3.11+**  
- **discord.py 2.5.2**  
- **SQLite + aiosqlite**  
- **OpenAI API (GitHub Models)**  
- **dotenv, matplotlib**

---

## 7. Installation & Setup

Copy and run all the following commands in your terminal:


### Clone the repository
git clone <repo-url>
cd MediHack-AI-HealthBot

### Install dependencies
`pip install -r requirements.txt`

### Create .env file
echo "DISCORD_TOKEN=your_discord_bot_token" >> config/.env
echo "GITHUB_TOKEN=your_github_models_token" >> config/.env
echo "DATABASE=bot/database/healthbot.db" >> config/.env


---

## 8. Usage Examples
**/symptoms fever cough**
**/telehealth**
**/logweight 72
/myprogress
/hydration 70 hot medium
?prefix !**

---

## 10. Future Scope

Integrate additional AI models for more accurate health advice

Connect with hospital / EMR systems

Develop dashboards or mobile apps for better tracking and analytics

Add multi-language support for wider accessibility

---

## 11. Disclaimer

⚠️ This bot does not provide medical diagnoses. Always consult a licensed healthcare professional.

---

## 12. Contributing / Author Info

Built for Medi-Hacks 2025 by [RAEES RIND].

## 13. Project Structure

```
MediHack-AI-HealthBot/
│
├─ bot/
│   ├─ commands/            # All bot command cogs (hydration, BMI, symptoms, etc.)
│   ├─ core/                # Loader, bot setup
│   ├─ database/            # SQLite DB & helper functions
│   └─ main.py              # Bot entry point
│
├─ config/
│   └─ .env                 # Environment variables
├─ requirements.txt         # Python dependencies
└─ README.md                # Read abt Bot


# Run the bot
python -m bot.main
