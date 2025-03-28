from aiogram.fsm.state import State, StatesGroup


class SiteStates(StatesGroup):
    year: State = State()
    semester: State = State()


class AdminStates(StatesGroup):
    func: State = State()
    id: State = State()


class MailingStates(StatesGroup):
    text: State = State()
    media: State = State()
    button_text: State = State()
    button_url: State = State()
    delay: State = State()
