import discord
from discord.ext import commands
from discord import app_commands
from openai import OpenAI
import os

from bot.database import database

# AI Config
token = os.environ.get("GITHUB_TOKEN")
endpoint = "https://models.github.ai/inference"
model_name = "openai/gpt-4o"

client = OpenAI(base_url=endpoint, api_key=token)


class BMICommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="bmi", description="📊 Calculate your BMI and get AI-based health advice.")
    async def bmi(self, interaction: discord.Interaction, weight: float, height: float):
        await interaction.response.defer()

        try:
            # ✅ Calculate BMI
            height_m = height / 100  # cm → meters
            bmi = round(weight / (height_m ** 2), 2)

            # ✅ Save to DB
            await database.log_bmi(interaction.user.id, weight, height, bmi)

            # ✅ Categorize
            if bmi < 18.5:
                category = "Underweight ❗"
            elif 18.5 <= bmi < 25:
                category = "Normal ✅"
            elif 25 <= bmi < 30:
                category = "Overweight ⚠️"
            else:
                category = "Obese 🚨"

            # ✅ Ask AI for professional advice
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": (
                        "You are a professional health advisor. "
                        "User gives BMI, weight, height. "
                        "Respond briefly with healthy lifestyle tips. "
                        "Be supportive, never judgmental. "
                        "Do NOT give exact medical prescriptions."
                    )},
                    {"role": "user", "content": f"My weight is {weight} kg, height {height} cm, BMI {bmi} ({category}). Give me advice."}
                ],
                temperature=0.6,
                max_tokens=250,
            )
            advice = response.choices[0].message.content

            # ✅ Embed Result
            embed = discord.Embed(
                title="📊 BMI Calculator",
                description=f"**Your BMI:** `{bmi}`\n**Category:** {category}",
                color=discord.Color.blue()
            )
            embed.add_field(name="💡 AI Health Advice", value=advice, inline=False)
            embed.set_footer(text="⚠️ This is general advice. Always consult a doctor for medical concerns.")

            await interaction.followup.send(embed=embed)

        except Exception as e:
            await interaction.followup.send(f"⚠️ Error while calculating BMI: `{e}`")


async def setup(bot):
    await bot.add_cog(BMICommand(bot))
