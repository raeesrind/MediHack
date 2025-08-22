# bot/core/loader.py

import os
import importlib

async def load_cogs(bot):
    base_dir = "bot/commands"
    
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                rel_path = os.path.relpath(os.path.join(root, file), base_dir)
                module_path = rel_path.replace("/", ".").replace("\\", ".").replace(".py", "")
                full_module = f"bot.commands.{module_path}"

                try:
                    await bot.load_extension(full_module)
                    print(f"✅ Loaded {full_module}")
                except Exception as e:
                    print(f"❌ Failed to load cog {full_module}: {e}")
