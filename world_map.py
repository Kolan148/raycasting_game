from settings import *

text_map = [
    '111111111111',
    '1......1...1',
    '1..222...3.1',
    '1....2..33.1',
    '1..3....3..1',
    '1..3...222.1',
    '1....1.....1',
    '111111111111'
]

world_map = set()
for j, row in enumerate(text_map):
    for i, char in enumerate(row):
        if char != '.':
            world_map.add((i, j))
