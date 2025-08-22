import discord
from discord.ext import commands
from discord import app_commands
from openai import OpenAI
import os

token = os.environ.get("GITHUB_TOKEN")
endpoint = "https://models.github.ai/inference"
model_name = "openai/gpt-4o"

client = OpenAI(base_url=endpoint, api_key=token)

class DrugChecker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="drugcheck", description="Check possible risks when combining medicines 💊")
    async def drugcheck(self, interaction: discord.Interaction, drug1: str, drug2: str):
        await interaction.response.defer()
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": (
                        "You are a medical safety assistant. "
                        "Explain briefly if two drugs may interact, based on common knowledge. "
                        "Always remind the user to consult a doctor."
                    )},
                    {"role": "user", "content": f"Check interaction between {drug1} and {drug2}"}
                ],
                temperature=0.5,
                max_tokens=250,
            )
            advice = response.choices[0].message.content

            embed = discord.Embed(
                title=f"💊 Drug Interaction: {drug1} + {drug2}",
                description=advice,
                color=discord.Color.purple()
            )
            embed.set_footer(text="⚠️ Do not self-medicate. Consult a healthcare provider.")
            await interaction.followup.send(embed=embed)
        except Exception as e:
            await interaction.followup.send(f"⚠️ Error: `{e}`")

async def setup(bot):
    await bot.add_cog(DrugChecker(bot))
