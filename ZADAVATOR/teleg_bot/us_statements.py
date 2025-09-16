from aiogram.fsm.state import State, StatesGroup


# состояния для main 
class Bot_Statements(StatesGroup): 
    answer_wait=State() 
    password_wait=State()
    login_wait=State()
    url_wait=State()