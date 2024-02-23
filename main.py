

from time import sleep
from src.sudoku import get_num,sudoku,finish
from PIL import ImageGrab



sleep(3)
num=get_num(ImageGrab.grab())
sudo=sudoku(num)
print(sudo)
finish(num,sudo)