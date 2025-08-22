import discord
from discord.ext import commands
from discord import app_commands
from openai import OpenAI
import os

# 🔑 GitHub Models API
token = os.environ.get("GITHUB_TOKEN")
endpoint = "https://models.github.ai/inference"
model_name = "openai/gpt-4o"

client = OpenAI(base_url=endpoint, api_key=token)

class FoodScan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="foodscan",
        description="Scan a food item and check if it’s healthy or not 🍎🍔"
    )
    async def foodscan(self, interaction: discord.Interaction, *, item: str):
        await interaction.response.defer()

        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a professional nutrition advisor. "
                            "The user will give you a food item. "
                            "Explain briefly if it is healthy/unhealthy, "
                            "highlight key nutrients, and provide a short tip."
                        )
                    },
                    {"role": "user", "content": f"Food item: {item}"}
                ],
                temperature=0.6,
                max_tokens=300
            )

            advice = response.choices[0].message.content

            embed = discord.Embed(
                title=f"🥗 Food Scan: {item.capitalize()}",
                description=advice,
                color=discord.Color.teal()
            )
            embed.set_footer(text="⚠️ General nutrition info only. Always consult a professional for diet plans.")
            await interaction.followup.send(embed=embed)

        except Exception as e:
            await interaction.followup.send(f"⚠️ Error: `{e}`")

async def setup(bot):
    await bot.add_cog(FoodScan(bot))
