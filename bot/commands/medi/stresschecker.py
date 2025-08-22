import discord
from discord.ext import commands
from discord import app_commands
from openai import OpenAI
import os

# 🔑 GitHub Models / OpenAI setup
token = os.environ.get("GITHUB_TOKEN")
endpoint = "https://models.github.ai/inference"
model_name = "openai/gpt-4o"

client = OpenAI(base_url=endpoint, api_key=token)


class StressCheckCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Store temporary answers per user
        self.user_sessions = {}

    @app_commands.command(
        name="stresscheck",
        description="🧘 Check your stress level and get relaxation advice"
    )
    async def stresscheck(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        # Define questions
        questions = [
            "😴 How well did you sleep last night? (good/average/poor)",
            "🙂 How is your mood today? (happy/neutral/sad/anxious)",
            "⚡ How is your energy level? (high/medium/low)",
            "🎯 Can you focus on tasks easily? (yes/no/sometimes)",
            "❤️ Do you feel supported by friends/family? (yes/no/unsure)"
        ]

        # Start asking
        self.user_sessions[interaction.user.id] = {"step": 0, "answers": []}
        await interaction.followup.send(questions[0], ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        user_id = message.author.id
        if user_id not in self.user_sessions:
            return

        session = self.user_sessions[user_id]
        step = session["step"]
        answers = session["answers"]

        # Save answer
        answers.append(message.content.strip())
        session["step"] += 1

        questions = [
            "😴 How well did you sleep last night? (good/average/poor)",
            "🙂 How is your mood today? (happy/neutral/sad/anxious)",
            "⚡ How is your energy level? (high/medium/low)",
            "🎯 Can you focus on tasks easily? (yes/no/sometimes)",
            "❤️ Do you feel supported by friends/family? (yes/no/unsure)"
        ]

        if session["step"] < len(questions):
            await message.channel.send(questions[session["step"]])
        else:
            # Done → analyze answers
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": (
                            "You are a stress management assistant. "
                            "The user answered some wellness questions. "
                            "Give a short professional summary of their stress level "
                            "and 3–4 practical tips for relaxation (e.g., breathing, breaks, talking to friends, exercise)."
                        )},
                        {"role": "user", "content": f"Answers: {answers}"}
                    ],
                    temperature=0.6,
                    max_tokens=300,
                )
                advice = response.choices[0].message.content
            except Exception as e:
                advice = f"⚠️ Error while fetching AI advice: {e}"

            embed = discord.Embed(
                title="🧘 Stress Check Results",
                description=advice,
                color=discord.Color.blue()
            )
            embed.set_footer(text="⚠️ This is not therapy. If stress is overwhelming, seek professional support.")
            await message.channel.send(embed=embed)

            # Clear session
            del self.user_sessions[user_id]


async def setup(bot):
    await bot.add_cog(StressCheckCommand(bot))
