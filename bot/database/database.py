import aiosqlite
import os
from datetime import datetime

DB_PATH = os.path.join("bot", "database", "healthbot.db")

async def init_db():
    """Initialize database and tables if not exist."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    async with aiosqlite.connect(DB_PATH) as db:
        # Users (added gender)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                gender TEXT,
                created_at TEXT
            )
        """)

        # BMI Logs
        await db.execute("""
            CREATE TABLE IF NOT EXISTS bmi_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                weight REAL,
                height REAL,
                bmi REAL,
                logged_at TEXT,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        """)

        # Hydration Logs
        await db.execute("""
            CREATE TABLE IF NOT EXISTS hydration_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                weight REAL,
                climate TEXT,
                activity TEXT,
                water_liters REAL,
                logged_at TEXT,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        """)


        # Stress Logs
        await db.execute("""
            CREATE TABLE IF NOT EXISTS stress_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                score INTEGER,
                logged_at TEXT,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        """)

        # Weight Logs
        await db.execute("""
            CREATE TABLE IF NOT EXISTS weight_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                weight REAL NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        """)

        await db.commit()


# ----------------- Helper Functions ----------------- #

async def ensure_user(user_id: int, gender: str = None):
    """Ensure user exists in users table, optionally set gender."""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,))
        exists = await cursor.fetchone()
        if not exists:
            await db.execute(
                "INSERT INTO users (user_id, gender, created_at) VALUES (?, ?, ?)",
                (user_id, gender, datetime.utcnow().isoformat())
            )
            await db.commit()
        elif gender:  # Update gender if provided
            await db.execute(
                "UPDATE users SET gender = ? WHERE user_id = ?",
                (gender, user_id)
            )
            await db.commit()


# ----------------- BMI, Hydration, Stress, Weight Logging ----------------- #

async def log_bmi(user_id: int, weight: float, height: float, bmi: float):
    await ensure_user(user_id)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO bmi_logs (user_id, weight, height, bmi, logged_at) VALUES (?, ?, ?, ?, ?)",
            (user_id, weight, height, bmi, datetime.utcnow().isoformat())
        )
        await db.commit()


async def log_hydration(user_id: int, weight: float, climate: str, activity: str, water_liters: float):
    await ensure_user(user_id)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            INSERT INTO hydration_logs (user_id, weight, climate, activity, water_liters, logged_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, weight, climate, activity, water_liters, datetime.utcnow().isoformat())
        )
        await db.commit()


async def log_stress(user_id: int, score: int):
    await ensure_user(user_id)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO stress_logs (user_id, score, logged_at) VALUES (?, ?, ?)",
            (user_id, score, datetime.utcnow().isoformat())
        )
        await db.commit()


async def log_weight(user_id: int, weight: float):
    await ensure_user(user_id)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO weight_logs (user_id, weight) VALUES (?, ?)",
            (user_id, weight)
        )
        await db.commit()


async def get_user_weights(user_id: int, limit: int = 10):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT weight, timestamp FROM weight_logs WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?",
            (user_id, limit)
        )
        rows = await cursor.fetchall()
        return rows[::-1]


# ----------------- Fetch History ----------------- #

async def fetch_bmi_history(user_id: int, limit: int = 10):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT weight, height, bmi, logged_at FROM bmi_logs WHERE user_id = ? ORDER BY logged_at DESC LIMIT ?",
            (user_id, limit)
        )
        return await cursor.fetchall()


async def fetch_hydration_history(user_id: int, limit: int = 10):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT water_liters, logged_at FROM hydration_logs WHERE user_id = ? ORDER BY logged_at DESC LIMIT ?",
            (user_id, limit)
        )
        return await cursor.fetchall()


async def fetch_stress_history(user_id: int, limit: int = 10):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT score, logged_at FROM stress_logs WHERE user_id = ? ORDER BY logged_at DESC LIMIT ?",
            (user_id, limit)
        )
        return await cursor.fetchall()
