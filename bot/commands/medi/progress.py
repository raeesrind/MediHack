import discord
from discord.ext import commands
from discord import app_commands
from openai import OpenAI
import matplotlib.pyplot as plt
import io
import os
from bot.database import database

# 🔑 GitHub Models API
token = os.environ.get("GITHUB_TOKEN")
endpoint = "https://models.github.ai/inference"
model_name = "openai/gpt-4o"
client = OpenAI(base_url=endpoint, api_key=token)

class Progress(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="logweight", description="Log your current weight 📥")
    async def logweight(self, interaction: discord.Interaction, weight: float):
        await database.log_weight(interaction.user.id, weight)
        await interaction.response.send_message(
            f"✅ Logged {weight} kg for {interaction.user.mention}"
        )

    @app_commands.command(name="myprogress", description="View your weight progress 📊")
    async def myprogress(self, interaction: discord.Interaction):
        await interaction.response.defer()

        weights = await database.get_user_weights(interaction.user.id, limit=10)
        if not weights:
            return await interaction.followup.send("⚠️ No weight logs found. Use `/logweight` first!")

        values = [w[0] for w in weights]
        dates = [w[1] for w in weights]

        # 📊 Make chart
        plt.figure(figsize=(6, 4))
        plt.plot(dates, values, marker="o", linestyle="-")
        plt.title(f"{interaction.user.display_name}'s Weight Progress")
        plt.xlabel("Date")
        plt.ylabel("Weight (kg)")
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        file = discord.File(buf, filename="progress.png")
        plt.close()

        # 🤖 AI feedback
        prompt = f"User's weight logs: {values}. Provide motivational feedback and simple advice."
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a supportive health coach."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            max_tokens=250
        )
        advice = response.choices[0].message.content

        embed = discord.Embed(
            title="📊 Your Progress",
            description=advice,
            color=discord.Color.blue()
        )
        embed.set_footer(text="⚠️ General advice only. Always consult a doctor for medical guidance.")
        embed.set_image(url="attachment://progress.png")

        await interaction.followup.send(embed=embed, file=file)

async def setup(bot):
    await bot.add_cog(Progress(bot))
