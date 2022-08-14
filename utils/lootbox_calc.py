# -*- coding: utf-8 -*-
# Copyright (c) 2022 Parad1se-py

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import random

from data import *


def calculate_cash(lootbox) -> int:
    if lootbox.lower() == 'normal':
        return random.randint(50, 100)
    elif lootbox.lower() == 'gold':
        return random.randint(100, 500)
    elif lootbox.lower() == 'mega':
        return random.randint(500, 1500)
    
def calculate_level(lootbox) -> int:
    if lootbox.lower() == 'normal':
        return random.randint(5, 10)
    elif lootbox.lower() == 'gold':
        return random.randint(10, 20)
    elif lootbox.lower() == 'mega':
        return random.randint(25, 50)

def calculate_ingredients(lootbox) -> dict:
    if lootbox.lower() == 'normal':
        ings = ['cheese', 'veg-salad', 'sauce']
        return {random.choice(ings), random.randint(1, 5)}

    elif lootbox.lower() == 'gold':
        ings = ['cheese', 'veg-salad', 'sauce', 'taco-shell', 'long-bun']
        final = {random.choice(ings): random.randint(2, 5) for _ in range(2)}
        return final

    elif lootbox.lower() == 'mega':
        ings = ['cheese', 'veg-salad', 'sauce', 'taco-shell', 'long-bun', 'rice-fillings', 'long-bun', 'tortilla']
        final = {random.choice(ings): random.randint(2, 5) for _ in range(random.randint(3, 5))}

        return final
    
def calculate_dish(lootbox) -> dict:
    if lootbox.lower() == 'normal':
        return {random.choice(['hot-dog', 'taco']): 1}

    elif lootbox.lower() == 'gold':
        dishes = ['taco', 'hot-dog', 'quesadilla']
        final = {random.choice(dishes): random.randint() for _ in range(2)}

        return final

    elif lootbox.lower() == 'mega':
        dishes = ['taco', 'hot-dog', 'quesadilla', 'burrito']
        final = {random.choice(dishes): random.randint() for _ in range(3)}

        return final