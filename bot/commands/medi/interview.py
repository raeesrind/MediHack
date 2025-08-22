import discord
from discord.ext import commands
from discord import app_commands
from openai import OpenAI
import os

token = os.environ.get("GITHUB_TOKEN")
endpoint = "https://models.github.ai/inference"
model_name = "openai/gpt-4o"

client = OpenAI(base_url=endpoint, api_key=token)

class InterviewCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_sessions = {}  # user_id -> session state

    @app_commands.command(name="interview", description="Start a quick health interview 🩺")
    async def interview(self, interaction: discord.Interaction):
        user_id = interaction.user.id

        if user_id in self.active_sessions:
            await interaction.response.send_message("⚠️ You already have an active interview. Finish it first.", ephemeral=True)
            return

        # Questions for the interview
        questions = [
            "For how many days have you had this issue?",
            "Where exactly is the pain or main symptom located?",
            "On a scale of 1–10, how severe is it?",
            "Do you have fever, nausea, vomiting, or other symptoms?",
            "Do you have any chronic conditions (diabetes, kidney disease, etc.)?",
            "Are you currently taking any medicines?",
            "Have you experienced this before?",
            "Does anything make it better or worse?",
        ]

        self.active_sessions[user_id] = {
            "step": 0,
            "answers": [],
            "questions": questions
        }

        await interaction.response.send_message(f"🩺 Let's begin your health interview!\n\n**Q1:** {questions[0]}", ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        user_id = message.author.id
        if user_id not in self.active_sessions:
            return

        session = self.active_sessions[user_id]
        session["answers"].append(message.content)
        session["step"] += 1

        if session["step"] < len(session["questions"]):
            # Ask next question
            next_q = session["questions"][session["step"]]
            await message.channel.send(f"**Q{session['step']+1}:** {next_q}")
        else:
            # All questions answered → summarize with AI
            answers_text = "\n".join(
                [f"Q{i+1}: {q}\nA: {a}" for i, (q, a) in enumerate(zip(session["questions"], session["answers"]))]
            )

            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": (
                            "You are a quick medical interviewer. The user has answered some health-related questions. "
                            "Summarize possible conditions (not diagnosis), give simple advice, and recommend when to see a doctor."
                        )},
                        {"role": "user", "content": answers_text}
                    ],
                    temperature=0.5,
                    max_tokens=400,
                )

                summary = response.choices[0].message.content
                embed = discord.Embed(
                    title="🩺 Interview Summary",
                    description=summary,
                    color=discord.Color.teal()
                )
                embed.set_footer(text="⚠️ This is not a medical diagnosis. Always consult a doctor.")
                await message.channel.send(embed=embed)

            except Exception as e:
                await message.channel.send(f"⚠️ Error while generating summary: `{e}`")

            # End session
            del self.active_sessions[user_id]

async def setup(bot):
    await bot.add_cog(InterviewCommand(bot))
