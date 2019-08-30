import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print('Base Dir :',BASE_DIR)

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
print('Project Root :',PROJECT_ROOT)

p1 = os.path.dirname(os.path.realpath(__file__))
print('P1 :',p1)

MEDIA_ROOT = os.path.join(BASE_DIR, 'orders/static/orders/')
print('Media Root :',MEDIA_ROOT)

a = 'a'
print(a)
print(int(''))