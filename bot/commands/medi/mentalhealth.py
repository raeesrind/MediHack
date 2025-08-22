import discord
from discord.ext import commands
from discord import app_commands
from openai import OpenAI
import os

token = os.environ.get("GITHUB_TOKEN")
endpoint = "https://models.github.ai/inference"
model_name = "openai/gpt-4o"

client = OpenAI(base_url=endpoint, api_key=token)

class MentalHealthCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mentalhealth", description="Share how you feel and get supportive advice 💙")
    async def mentalhealth(self, interaction: discord.Interaction, *, mood: str):
        await interaction.response.defer()
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": (
                        "You are a caring mental health assistant. "
                        "Respond briefly, kindly, and encourage self-care. "
                        "If signs of crisis appear (suicidal/self-harm), suggest contacting professionals immediately."
                    )},
                    {"role": "user", "content": mood}
                ],
                temperature=0.7,
                max_tokens=250,
            )
            advice = response.choices[0].message.content

            embed = discord.Embed(
                title="💙 Mental Health Support",
                description=advice,
                color=discord.Color.blue()
            )
            embed.set_footer(text="⚠️ This is not therapy. If you’re struggling, please reach out to a professional.")
            await interaction.followup.send(embed=embed)
        except Exception as e:
            await interaction.followup.send(f"⚠️ Error: `{e}`")

async def setup(bot):
    await bot.add_cog(MentalHealthCommand(bot))
