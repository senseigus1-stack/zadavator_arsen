import os
import sqlalchemy

from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile


from config import TOKEN
from teleg_bot.us_statements import Bot_Statements
 
bot = Bot(token=TOKEN)
router = Router()

