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

class NutritionCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="advicefornutrient", 
        description="Get nutrition advice for a disease (or general advice)."
    )
    @app_commands.describe(
        disease="Name of the disease, or 'no' for general nutrition advice."
    )
    async def advicefornutrient(self, interaction: discord.Interaction, disease: str):
        await interaction.response.defer()

        try:
            disease_lower = disease.lower().strip()

            # Quick rules for some common conditions
            quick_advice = {
                "no": "🥗 General advice: Eat a balanced diet with fruits, vegetables, lean proteins, whole grains, and enough water. Limit sugar and processed foods.",
                "kidney stone": "🚰 For kidney stones: Drink plenty of water. Reduce salt and limit foods high in oxalates (e.g., spinach, nuts). Avoid too much animal protein.",
                "diabetes": "🍎 For diabetes: Focus on low-glycemic foods, fiber-rich vegetables, whole grains, lean proteins. Limit added sugars and refined carbs.",
                "hypertension": "💓 For high blood pressure: Lower salt intake, eat more fruits, vegetables, and potassium-rich foods. Avoid excessive alcohol and processed foods.",
                "anemia": "🩸 For anemia: Eat iron-rich foods (red meat, beans, leafy greens). Add vitamin C to help absorption. Limit tea/coffee near meals.",
            }

            if disease_lower in quick_advice:
                answer = quick_advice[disease_lower]
            else:
                # AI fallback for other conditions
                response = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a nutrition advisor. The user will give a disease name "
                                "(or 'no' for general advice). Provide short, practical nutrition guidance. "
                                "Keep it under 5 sentences. If unsure, give general healthy eating advice."
                            ),
                        },
                        {
                            "role": "user",
                            "content": disease,
                        }
                    ],
                    model=model_name,
                    temperature=0.5,
                    max_tokens=300,
                )
                answer = response.choices[0].message.content

            embed = discord.Embed(
                title="🥦 Nutrition Advice",
                description=answer,
                color=discord.Color.blue()
            )
            embed.set_footer(text="⚠️ Always consult a healthcare professional for personalized advice.")
            await interaction.followup.send(embed=embed)

        except Exception as e:
            await interaction.followup.send(
                f"⚠️ Error while fetching AI response: `{e}`"
            )


async def setup(bot):
    await bot.add_cog(NutritionCommand(bot))
