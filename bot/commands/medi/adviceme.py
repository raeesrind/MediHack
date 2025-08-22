import discord
from discord.ext import commands
from discord import app_commands
from openai import OpenAI
import os

token = os.environ.get("GITHUB_TOKEN")
endpoint = "https://models.github.ai/inference"
model_name = "openai/gpt-4o"

client = OpenAI(base_url=endpoint, api_key=token)

class AdviceCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="adviseme",
        description="Get AI-powered lifestyle advice 🧘‍♂️"
    )
    @app_commands.describe(
        category="Choose advice type (optional)",
        custom="Or write your own topic (e.g. athlete diet, skincare routine)"
    )
    @app_commands.choices(category=[
        app_commands.Choice(name="Weight Gain", value="weightgain"),
        app_commands.Choice(name="Weight Loss", value="weightloss"),
        app_commands.Choice(name="Healthy Skin", value="healthyskin"),
        app_commands.Choice(name="Calm Mind", value="calmmind"),
        app_commands.Choice(name="Fitness & Energy", value="fitness"),
        app_commands.Choice(name="Better Sleep", value="sleep"),
        app_commands.Choice(name="Balanced Diet", value="diet"),
        app_commands.Choice(name="Healthy Hair", value="hair"),
        app_commands.Choice(name="Strong Immunity", value="immunity"),
    ])
    async def adviseme(
        self,
        interaction: discord.Interaction,
        category: app_commands.Choice[str] = None,
        custom: str = None
    ):
        await interaction.response.defer()

        try:
            # Determine the topic
            if custom:
                topic = custom
            elif category:
                topic = category.name
            else:
                await interaction.followup.send("⚠️ Please select a category or provide a custom topic.")
                return

            # Ask AI for lifestyle advice
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a friendly health and lifestyle coach. "
                            "The user will ask for advice (like weight loss, skin care, calm mind). "
                            "Give 3–5 practical, safe, short tips in bullet points. "
                            "Keep the advice motivating and easy to follow."
                        ),
                    },
                    {
                        "role": "user",
                        "content": f"Give me lifestyle advice for {topic}.",
                    },
                ],
                temperature=0.7,
                max_tokens=350,
            )

            advice = response.choices[0].message.content

            embed = discord.Embed(
                title=f"🌱 Lifestyle Advice: {topic}",
                description=advice,
                color=discord.Color.blue()
            )
            embed.set_footer(text="⚠️ This is general advice. Consult professionals for personalized guidance.")
            await interaction.followup.send(embed=embed)

        except Exception as e:
            await interaction.followup.send(f"⚠️ Error while fetching advice: `{e}`")

async def setup(bot):
    await bot.add_cog(AdviceCommand(bot))
