import discord
from discord.ext import commands
from discord import app_commands

class FirstAidCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="firstaid",
        description="🚑 Get quick first aid steps for emergencies (burns, cuts, fainting, choking, nosebleeds, etc.)"
    )
    @app_commands.describe(
        emergency="Type of emergency (burn, cut, fainting, choking, nosebleed)"
    )
    async def firstaid(self, interaction: discord.Interaction, emergency: str):
        await interaction.response.defer()

        # ✅ Quick reference steps
        first_aid_steps = {
            "burn": [
                "Cool the burn under **running cool water** for 10–20 minutes.",
                "Remove **tight clothing/jewelry** near the area (not stuck fabric).",
                "Cover with a **clean, non-fluffy cloth or sterile gauze**.",
                "Do **not apply butter, toothpaste, or oils**.",
                "Seek medical help if burn is severe or blistering."
            ],
            "cut": [
                "Wash hands before touching the wound.",
                "Apply **gentle pressure with a clean cloth** to stop bleeding.",
                "Rinse with **clean water** to remove dirt.",
                "Cover with **sterile bandage**.",
                "If bleeding is heavy or won’t stop, seek emergency care."
            ],
            "fainting": [
                "Lay the person **flat on their back**.",
                "Raise legs **above heart level** if possible.",
                "Loosen tight clothing.",
                "Check breathing & responsiveness.",
                "If not recovering within 1–2 minutes → call emergency help."
            ],
            "choking": [
                "Ask if the person can **cough or speak**.",
                "If not, perform **5 back blows** between shoulder blades.",
                "If unsuccessful, do **5 abdominal thrusts (Heimlich)**.",
                "Alternate until object is expelled or person becomes unresponsive.",
                "If unresponsive → begin **CPR** and call emergency services."
            ],
            "nosebleed": [
                "Sit the person down and **lean forward** (not back).",
                "Pinch the soft part of the nose for **10–15 minutes**.",
                "Apply a **cold compress** to the bridge of the nose.",
                "Avoid blowing or picking the nose for several hours.",
                "Seek care if bleeding is heavy or lasts >20 minutes."
            ]
        }

        # ✅ Normalize input
        emergency = emergency.lower()
        steps = first_aid_steps.get(emergency)

        if not steps:
            await interaction.followup.send(
                "⚠️ Unknown emergency type. Please choose from: **burn, cut, fainting, choking, nosebleed**."
            )
            return

        # ✅ Build embed
        embed = discord.Embed(
            title=f"🚑 First Aid Guide: {emergency.capitalize()}",
            color=discord.Color.red()
        )
        for i, step in enumerate(steps, start=1):
            embed.add_field(name=f"Step {i}", value=step, inline=False)

        embed.set_footer(text="⚠️ This is not a substitute for professional medical help. Call emergency services if needed.")
        await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(FirstAidCommand(bot))
