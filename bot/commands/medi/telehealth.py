import discord
from discord.ext import commands
from discord import app_commands

class TelehealthCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="telehealth", description="Prepare for a telehealth consultation 📋")
    async def telehealth(self, interaction: discord.Interaction):
        checklist = (
            "📋 **Telehealth Prep Checklist**\n"
            "1. Write down your symptoms clearly.\n"
            "2. Note when they started and what makes them better/worse.\n"
            "3. List all medicines/supplements you are taking.\n"
            "4. Have your ID and insurance card ready.\n"
            "5. Test your internet, mic, and camera before the call."
        )
        await interaction.response.send_message(embed=discord.Embed(
            title="🖥️ Telehealth Checklist",
            description=checklist,
            color=discord.Color.teal()
        ))

async def setup(bot):
    await bot.add_cog(TelehealthCommand(bot))
