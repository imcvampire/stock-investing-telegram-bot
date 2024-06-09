import logging
import os

import yfinance as yf
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def post_init(application: Application) -> None:
    await application.bot.set_my_commands(
        [("p", "Use /p <ticker> to get the price of a stock.")]
    )


async def p(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id

    try:
        ticker = yf.Ticker(context.args[0])

        await update.effective_message.reply_text(
            f"Current price: {ticker.info.get('currentPrice')}{ticker.info.get('currency')}"
        )
    except (IndexError, ValueError):
        await update.effective_message.reply_text("Usage: /p <ticker>")


def main() -> None:
    """Run the bot."""
    application = (
        Application.builder()
        .token(os.environ.get("TELEGRAM_BOT_TOKEN"))
        .post_init(post_init)
        .build()
    )

    command_handler = CommandHandler("p", p)

    application.add_handler(command_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
