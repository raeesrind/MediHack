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

class MedicineCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="checkmedicine", 
        description="Check details about a medicine (uses AI if unknown)."
    )
    @app_commands.describe(
        medicine="Name of the medicine (e.g., Paracetamol, Ibuprofen)."
    )
    async def checkmedicine(self, interaction: discord.Interaction, medicine: str):
        await interaction.response.defer()

        try:
            med_lower = medicine.lower().strip()

            # Quick facts for common meds
            quick_facts = {
                "paracetamol": "💊 Paracetamol (Acetaminophen): Used for fever and mild to moderate pain. Do not exceed 4g/day. Avoid alcohol to reduce liver risk.",
                "ibuprofen": "💊 Ibuprofen: NSAID for pain, inflammation, fever. Take after food to avoid stomach irritation. Avoid if ulcers, kidney issues, or pregnancy (3rd trimester).",
                "amoxicillin": "💊 Amoxicillin: Antibiotic for bacterial infections. Take full course even if you feel better. Not effective for viral infections like colds.",
                "aspirin": "💊 Aspirin: Used for pain, fever, and heart health (low dose). Avoid in children (risk of Reye’s syndrome). Can irritate stomach lining.",
                "metformin": "💊 Metformin: Commonly for type 2 diabetes. Helps lower blood sugar. Take with meals. Watch for rare but serious side effect: lactic acidosis.",
            }

            if med_lower in quick_facts:
                answer = quick_facts[med_lower]
            else:
                # AI fallback for any medicine
                response = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a medical assistant. The user gives the name of a medicine. "
                                "Explain its general use, common side effects, and important warnings. "
                                "Keep response short, clear, and under 6 sentences. "
                                "Add ⚠️ disclaimer about consulting a doctor."
                            ),
                        },
                        {
                            "role": "user",
                            "content": medicine,
                        }
                    ],
                    model=model_name,
                    temperature=0.5,
                    max_tokens=350,
                )
                answer = response.choices[0].message.content

            embed = discord.Embed(
                title=f"💊 Medicine Check: {medicine.title()}",
                description=answer,
                color=discord.Color.purple()
            )
            embed.set_footer(text="⚠️ This is general info. Always consult a doctor or pharmacist before use.")
            await interaction.followup.send(embed=embed)

        except Exception as e:
            await interaction.followup.send(
                f"⚠️ Error while fetching AI response: `{e}`"
            )


async def setup(bot):
    await bot.add_cog(MedicineCommand(bot))
