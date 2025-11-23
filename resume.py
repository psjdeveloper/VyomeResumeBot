import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes,
)
from fpdf import FPDF

# Conversation steps
NAME, CONTACT, EDUCATION, SKILLS, PROJECTS, EXPERIENCE = range(6)


# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()  # reset for each user
    await update.message.reply_text("Welcome to Resume Bot! What's your full name?")
    return NAME


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Great! What's your contact info?")
    return CONTACT


async def get_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["contact"] = update.message.text
    await update.message.reply_text("Your education?")
    return EDUCATION


async def get_education(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["education"] = update.message.text
    await update.message.reply_text("Your skills?")
    return SKILLS


async def get_skills(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["skills"] = update.message.text
    await update.message.reply_text("Your projects?")
    return PROJECTS


async def get_projects(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["projects"] = update.message.text
    await update.message.reply_text("Your experience?")
    return EXPERIENCE


async def get_experience(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["experience"] = update.message.text

    # Generate PDF safely
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for key, value in context.user_data.items():
        pdf.multi_cell(0, 10, f"{key.capitalize()}: {value}")

    file_path = f"resume_{update.effective_user.id}.pdf"
    pdf.output(file_path)

    # Send file
    await update.message.reply_document(document=open(file_path, "rb"))

    return ConversationHandler.END


# CANCEL command
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cancelled. You can start again anytime with /start.")
    context.user_data.clear()
    return ConversationHandler.END


def main():
    TOKEN = os.getenv("BOT_TOKEN")  # safest way

    if not TOKEN:
        raise ValueError("❌ BOT_TOKEN environment variable not set")

    app = Application.builder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            CONTACT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_contact)],
            EDUCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_education)],
            SKILLS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_skills)],
            PROJECTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_projects)],
            EXPERIENCE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_experience)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv)

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
