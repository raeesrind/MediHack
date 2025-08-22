import os
import discord
from discord.ext import commands
from discord import app_commands
from openai import OpenAI

# Load GitHub Models API client
token = os.environ.get("GITHUB_TOKEN")
endpoint = "https://models.github.ai/inference"
model_name = "openai/gpt-4o"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

class SymptomsCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="symptoms", 
        description="Describe your symptoms (e.g., cough, fever, back pain)."
    )
    async def symptoms(self, interaction: discord.Interaction, *, description: str):
        await interaction.response.defer()

        try:
            # Custom fast rules for common cases
            quick_checks = {
                ("cough", "fever"): "This may be related to flu, infection, or COVID-like illness. Stay hydrated and rest. Seek medical help if it worsens.",
                ("vomiting", "back pain", "fever"): "These could suggest kidney-related issues or infection. Please consult a doctor promptly.",
                ("headache", "dizziness"): "Might be due to dehydration, migraine, or stress. Rest and drink fluids, but check with a doctor if severe.",
            }

            # Normalize input
            desc_lower = description.lower()
            found_condition = None
            for symptoms, advice in quick_checks.items():
                if all(s in desc_lower for s in symptoms):
                    found_condition = advice
                    break

            if found_condition:
                answer = found_condition
            else:
                # Ask AI for general analysis
                response = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a quick medical assistant. "
                                "The user will describe symptoms. "
                                "Give a **short, clear response** with possible conditions (not diagnosis) "
                                "and a simple piece of advice."
                            ),
                        },
                        {
                            "role": "user",
                            "content": description,
                        }
                    ],
                    model=model_name,
                    temperature=0.5,
                    max_tokens=300,
                )
                answer = response.choices[0].message.content

            # Send AI/quick response back to Discord
            embed = discord.Embed(
                title="🩺 Symptom Checker",
                description=answer,
                color=discord.Color.green()
            )
            embed.set_footer(text="⚠️ This is not a medical diagnosis. Always consult a doctor.")
            await interaction.followup.send(embed=embed)

        except Exception as e:
            await interaction.followup.send(
                f"⚠️ Error while fetching AI response: `{e}`"
            )

async def setup(bot):
    await bot.add_cog(SymptomsCommand(bot))
