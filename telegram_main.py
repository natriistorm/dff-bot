
import os


from dff.script import conditions as cnd
from dff.script import labels as lbl
from dff.script import RESPONSE, TRANSITIONS, Message
from dff.messengers.telegram import PollingTelegramInterface
from dff.pipeline import Pipeline
from dff.utils.testing.common import is_interactive_mode
from general import general_script

from tg_bot_token import TG_BOT_TOKEN
"""
In order to integrate your script with Telegram, you need an instance of
`TelegramMessenger` class and one of the following interfaces:
`PollingMessengerInterface` or `WebhookMessengerInterface`.
`TelegramMessenger` encapsulates the bot logic.
Like Telebot, `TelegramMessenger` only requires a token to run.
However, all parameters from the Telebot class can be passed as keyword arguments.
The two interfaces connect the bot to Telegram. They can be passed directly
to the DFF `Pipeline` instance.
"""

happy_path = (
    (Message(text="/start"), Message(text="Hi")),
    (Message(text="Hi"), Message(text="Hi")),
    (Message(text="Bye"), Message(text="Hi")),
)

interface = PollingTelegramInterface(token=TG_BOT_TOKEN)


pipeline = Pipeline.from_script(
    script=general_script,  # Actor script object
    start_label=("greeting_flow", "start_node"),
    fallback_label=("greeting_flow", "fallback_node"),
    messenger_interface=interface,  # The interface can be passed as a pipeline argument.
)


def main():
    if not TG_BOT_TOKEN:
        print("`TG_BOT_TOKEN` variable needs to be set to use TelegramInterface.")
    pipeline.run()


if __name__ == "__main__" and is_interactive_mode():  # prevent run during doc building
    main()