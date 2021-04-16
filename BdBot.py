import logging
import platform

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

import state


class BdBot(state.State):
    def __init__(self):
        super().__init__()

        # persistent state stuff
        state_file="bot.state"
        try:
            self.load(state_file)
        except Exception as e:
            logging.error(str(e))
            logging.info("Created new state file.")
            self.save(state_file)

        # update missing defaults
        self.defaults({
            'token': '1677325747:AAGeNn-PubBMUq74XLwM1OKrj4AoxqBcWwY',
            'joined_ids': []
        })


        # Initialize bot and dispatcher
        self.bot = Bot(token=self.state.token)
        self.dp = Dispatcher(self.bot)

        @self.dp.message_handler(commands=['join'])
        async def handle_join(message: types.Message):
            if message.chat.id in self.state.joined_ids:
                await message.reply("Already joined")
            else:
                self.state.joined_ids.append(message.chat.id)
                self.save()
                await message.reply("Joined {}".format(platform.node()))

        @self.dp.message_handler(commands=['leave'])
        async def handle_leave(message: types.Message):
            if message.chat.id in self.state.joined_ids:
                self.state.joined_ids.remove(message.chat.id)
                self.save()
                await message.reply("Left")

    async def on_startup(self,dispatcher, url=None, cert=None):
        await self.send_message_joined("Started: {}".format(platform.node()))

    async def on_shutdown(self, dispatcher, url=None, cert=None):
        await self.send_message_joined("Stopped: {}".format(platform.node()))

    async def send_message_joined(self, text):
        """send message to all joined clients"""
        for chat_id in self.state.joined_ids:
            await self.bot.send_message(chat_id, text)

    def run(self):
        executor.start_polling(self.dp, skip_updates=True, on_startup=self.on_startup, on_shutdown=self.on_shutdown)