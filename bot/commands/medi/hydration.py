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


class HydrationCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="hydration",
        description="💧 Calculate how much water you should drink daily based on weight, climate, and activity."
    )
    @app_commands.describe(
        weight="Your weight in kilograms",
        climate="Your climate (hot, moderate, cold)",
        activity="Your activity level (low, medium, high)"
    )
    async def hydration(self, interaction: discord.Interaction, weight: float, climate: str, activity: str):
        await interaction.response.defer()

        try:
            # ✅ Base calculation: 35ml water per kg body weight
            base_water_ml = weight * 35

            # ✅ Adjust for climate
            climate_factor = {"hot": 1.3, "moderate": 1.0, "cold": 0.9}
            base_water_ml *= climate_factor.get(climate.lower(), 1.0)

            # ✅ Adjust for activity
            activity_factor = {"low": 1.0, "medium": 1.2, "high": 1.4}
            base_water_ml *= activity_factor.get(activity.lower(), 1.0)

            # ✅ Convert to liters
            water_liters = round(base_water_ml / 1000, 2)

            # ✅ Save to DB
            await database.log_hydration(interaction.user.id, weight, climate, activity, water_liters)

            # ✅ Ask AI for hydration advice
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": (
                        "You are a professional health & hydration advisor. "
                        "User gives weight, climate, activity, and water needs. "
                        "Give short professional advice on hydration habits and tips. "
                        "Be supportive, never judgmental."
                    )},
                    {"role": "user", "content": f"My weight is {weight}kg, climate is {climate}, activity level is {activity}. My recommended intake is {water_liters}L/day. Give me hydration advice."}
                ],
                temperature=0.6,
                max_tokens=250,
            )
            advice = response.choices[0].message.content

            # ✅ Embed Result
            embed = discord.Embed(
                title="💧 Daily Hydration Needs",
                description=f"**Recommended Water Intake:** `{water_liters} L/day`",
                color=discord.Color.teal()
            )
            embed.add_field(name="💡 AI Hydration Advice", value=advice, inline=False)
            embed.set_footer(text="⚠️ This is general advice. Always adjust if you have medical conditions.")

            await interaction.followup.send(embed=embed)

        except Exception as e:
            await interaction.followup.send(f"⚠️ Error while calculating hydration: `{e}`")


async def setup(bot):
    await bot.add_cog(HydrationCommand(bot))
