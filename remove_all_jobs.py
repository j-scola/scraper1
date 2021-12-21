import os

for f in os.listdir('data'):
  print(f'removing {f}')
  os.remove(f'data/{f}')
  