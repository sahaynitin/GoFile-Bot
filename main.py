# Made with python3
# (C) @FayasNoushad
# Copyright permission under MIT License
# All rights reserved by FayasNoushad
# License -> https://github.com/FayasNoushad/GoFile-Bot/blob/main/LICENSE

import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from gofile import uploadFile


Bot = Client(
    "GoFile-Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)


@Bot.on_message(filters.private & filters.command("start"))
async def start(bot, update):
    await update.reply_text(
        text="""Hey {}

Welcome to {}

Using this bot you can get id of any group, user, bot, channel and even stickers with inline mode.

Use below buttons to learn more !

By @Tellybots_4u
    """

    # Home Button
    home_buttons = [
        [InlineKeyboardButton(text="🏠 Return Home 🏠", callback_data="home")],
    ]

    # Rest Buttons
    buttons = [
        [InlineKeyboardButton("✨ Botz Updates ✨", url="https://t.me/tellybots_4u")],
        [
            InlineKeyboardButton("How to Use ❔", callback_data="help"),
            InlineKeyboardButton("🎪 About 🎪", callback_data="about")
        ],
        [InlineKeyboardButton("♥ More Amazing bots ♥", url="https://t.me/tellybots_4u")],
        [InlineKeyboardButton("🎨 Support Group 🎨", url="https://t.me/tellybots_support")],
    ]

    # Help Message
    HELP = """
**Help & Features**

1) Send any message to get your ID.
2) Forward any message from any user/bot/channel or anonymous admins to get ID.
3) Send any sticker to get sticker id.
4) Use Inline Mode to send your ID in any chat.
5) Add in group / channel to get ID.
6) Use /id command:
- in private: To get ID through username
- in group/channel: To get ID of that chat. 

✨ **Available Commands** ✨

/id - Get ID
/about - About The Bot
/help - This Message
/start - Start the Bot
    """",
        disable_web_page_preview=True,
        quote=True
    )


@Bot.on_message(filters.private & filters.media)
async def media_filter(bot, update):
    try:
        message = await update.reply_text(
            text="`Processing...`",
            quote=True,
            disable_web_page_preview=True
        )
        media = await update.download()
        await message.edit_text(
            text="`Downloading...`",
            disable_web_page_preview=True
        )
        response = uploadFile(media)
        await message.edit_text(
            text="`Uploading...`",
            disable_web_page_preview=True
        )
        try:
            os.remove(media)
        except:
            pass
    except Exception as error:
        await update.reply_text(
            text=f"Error :- <code>{error}</code>",
            quote=True,
            disable_web_page_preview=True
        )
        return
    text = f"**File Name:** `{response['fileName']}`" + "\n"
    text += f"**Download Page:** `{response['downloadPage']}`" + "\n"
    text += f"**Direct Download Link:** `{response['directLink']}`" + "\n"
    text += f"**Info:** `{response['info']}`"
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="Open Link", url=response['directLink']),
                InlineKeyboardButton(text="Share Link", url=f"https://telegram.me/share/url?url={response['directLink']}")
            ],
            [
                InlineKeyboardButton(text="Join Updates Channel", url="https://telegram.me/FayasNoushad")
            ]
        ]
    )
    await message.edit_text(
        text=text,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )


Bot.run()
