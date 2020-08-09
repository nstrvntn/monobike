import asyncio
from timer import UserTimer
from config import helpButton, timerButton
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

class Quiz():
    def __init__(self, db, bot, id):
        self.tasks = db["tasks"]
        self.bot = bot
        self.chat_id = id

    def start(self):
        first_task = self.tasks.find_one({"operation":"ready"})

        self.timer = UserTimer(self.chat_id, self.stopTimeout)
        self.run_task(first_task)

    def stop(self):
        self.current_task = None
        self.timer.stop()

    def stopTimeout(self):
        self.stop()
        self.sendMessage("Время вышло. ⏳ Ты проиграл 😢", menu=ReplyKeyboardRemove())

    def run_task(self, task):
        self.current_task = task
        self.current_task_help_penalty = False

        print(self.current_task)
        question = self.current_task.get("question")
        help = self.current_task.get("help")
        answer = self.current_task.get("answer")
        nextButtons = self.current_task.get("nextButtonText")
        menu = ReplyKeyboardMarkup(resize_keyboard=True).row(timerButton)

        if not help is None:
            menu.insert(helpButton)

        if not nextButtons is None:
            if isinstance(nextButtons, list):
                if len(nextButtons) > 1:
                    menu.row(nextButtons[0])

                    for button in nextButtons[1:]:
                        menu.insert(KeyboardButton(button))
                else:
                    menu.insert(nextButtons[0])
            else:
                menu.insert(nextButtons)

        if nextButtons is None and answer is None:
            self.stop()
            menu = ReplyKeyboardRemove()

        self.sendMessage(question, menu=menu)

    def answer(self, text):
        if self.current_task is None:
            self.sendMessage('Для начала квеста нажмите /start')
            return

        if text == helpButton.text:
            self.sendMessage(self.current_task.get("help"))
            if not self.current_task_help_penalty:
                self.current_task_help_penalty = True
                self.timer.penaltyTime(15*60)
                self.sendMessage("-15 минут времени")
            return

        task = self.tasks.find_one({ "operation": text })
        correctAnswer = self.current_task.get("answer")
        nextButtons = self.current_task.get("nextButtonText")

        print(list(self.tasks.find({})))

        print(text)
        print(task)

        if not correctAnswer is None:
            if correctAnswer == text:
                self.run_task(task)
            else:
                self.sendMessage("Не правильный ответ! 😡 -15 минут времени 🧨")
                self.timer.penaltyTime(15*60)
        elif not nextButtons is None:
            if isinstance(nextButtons, list) and text in nextButtons or text == nextButtons:
                self.run_task(task)
            else:
                self.sendMessage("Воспользуйтесь кнопками")

    def sendMessage(self, text, menu = None):
        asyncio.run_coroutine_threadsafe(
            self.bot.send_message(self.chat_id, text=text, reply_markup=menu),
            self.bot.loop
        )