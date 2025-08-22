import discord
from discord.ext import commands
from discord import app_commands
from openai import OpenAI
import os
import datetime

token = os.environ.get("GITHUB_TOKEN")
endpoint = "https://models.github.ai/inference"
model_name = "openai/gpt-4o"

client = OpenAI(base_url=endpoint, api_key=token)

# Cache daily tip to avoid generating new one multiple times a day
last_tip = {"date": None, "text": None}

class DailyTip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="dailytip", description="Get a fresh daily health tip 🌿")
    async def dailytip(self, interaction: discord.Interaction):
        await interaction.response.defer()

        global last_tip
        today = datetime.date.today()

        try:
            # ✅ Use cached tip if already generated today
            if last_tip["date"] == today:
                tip = last_tip["text"]
            else:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a motivational health coach. "
                                "Generate ONE short, unique, practical tip for daily wellness. "
                                "It can be about nutrition, fitness, skin care, stress relief, hydration, or mental clarity. "
                                "Keep it under 2–3 sentences."
                            ),
                        },
                        {"role": "user", "content": "Give me today's daily health tip."}
                    ],
                    temperature=0.8,
                    max_tokens=150,
                )
                tip = response.choices[0].message.content
                last_tip = {"date": today, "text": tip}

            # ✅ Send tip
            embed = discord.Embed(
                title=f"🌞 Daily Health Tip ({today.strftime('%B %d, %Y')})",
                description=tip,
                color=discord.Color.teal()
            )
            embed.set_footer(text="Stay consistent. Small habits build big results 💪")
            await interaction.followup.send(embed=embed)

        except Exception as e:
            await interaction.followup.send(f"⚠️ Error while fetching tip: `{e}`")

async def setup(bot):
    await bot.add_cog(DailyTip(bot))
