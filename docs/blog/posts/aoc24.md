---
layout: post
title: Advent of Code 2024
description: It's that time of year.
image: https://aplwiki.com/images/0/0d/Advent_Of_Code_Logo.png
tags:
    - coding
date: 2024-12-01
---

I heard about [Advent of Code](https://adventofcode.com/2024/about) last year, but didn't participate because I was busy.

This year I'm still busy, but nonetheless succumbed to the feeling of needing to solve problems simply because they exist. All computer scientists I know have this curse.

## Day 1

The problem: [link](https://adventofcode.com/2024/day/1)

The solution:

```python
left = []
right = []

# https://adventofcode.com/2024/day/1/input
with open("input.txt", "r") as f:
    lines = f.readlines()

for line in lines:
    l,r = line.split()
    left.append(int(l))
    right.append(int(r))

left.sort()
right.sort()

part1 = 0
part2 = 0
for i,l in enumerate(left):
    diff = left[i] - right[i]
    if diff < 0:
        diff *= -1
    part1 += diff

    matches = 0
    for r in right:
        if l == r:
            matches += 1
    part2 += l * matches

print(f"Part 1 solution: {part1}") 
print(f"Part 2 solution: {part2}")
```

## Day 2

The problem: [link](https://adventofcode.com/2024/day/2)

The solution:

```python
def is_safe_w_dampen(nums, i):
    copy1 = nums.copy()
    copy2 = nums.copy()
    copy3 = nums.copy()
    copy1.pop(i)
    copy2.pop(i+1)
    if i > 0:
        copy3.pop(i-1)
    one = is_safe(copy1, False)
    two = is_safe(copy2, False)
    three = is_safe(copy3, False)
    return one or two or three

def is_safe(nums, dampen: bool) -> bool: 
    increasing = True if nums[1] > nums[0] else False
    for i in range(len(nums) - 1):
        diff = nums[i+1] - nums[i]
        if (diff == 0 or diff > 3 or diff < -3) \
        or (diff > 0 and not increasing) \
        or (diff < 0 and increasing):
            if dampen:
                return is_safe_w_dampen(nums, i)
            return False
    return True

with open("input.txt", "r") as f:
    lines = f.readlines()

part1 = 0
part2 = 0
for line in lines:
    nums = [int(x) for x in line.split()]

    if is_safe(nums, False):
        part1 += 1
    if is_safe(nums, True):
        part2 += 1

print(f"Part 1 solution: {part1}") 
print(f"Part 2 solution: {part2}")
```

## Day 3

The problem: [link](https://adventofcode.com/2024/day/3)

The solution:

```python
import re

with open("./input.txt", "r") as f:
    data = f.read()

enabled = True
pattern = r'mul\((\d{1,3}),(\d{1,3})\)|(do\(\))|(don\'t\(\))'
matches = re.findall(pattern, data)
part1 = 0
part2 = 0
for m in matches:
    if m[2]:
        enabled = True
    elif m[3]:
        enabled = False
    else:
        cur = int(m[0]) * int(m[1])
        part1 += cur
        if enabled:
            part2 += cur

print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
```

## Day 4

The problem: [link](https://adventofcode.com/2024/day/4)

The solution:

```python
with open("input.txt", "r") as f:
    lines = [l[:-1] for l in f.readlines()]

part1 = 0
part2 = 0
rows = len(lines)
cols = len(lines[0])

for i in range(rows):
    for j in range(cols):
        # part 1
        words = []
        if j <= cols - 4:
            words.append(lines[i][j] + lines[i][j+1] + lines[i][j+2] + lines[i][j+3])
        if i <= rows - 4 and j <= cols - 4:
            words.append(lines[i][j] + lines[i+1][j+1] + lines[i+2][j+2] + lines[i+3][j+3])
        if i <= rows - 4:
            words.append(lines[i][j] + lines[i+1][j] + lines[i+2][j] + lines[i+3][j])
        if i <= rows - 4 and j > 2:
            words.append(lines[i][j] + lines[i+1][j-1] + lines[i+2][j-2] + lines[i+3][j-3])
        if j > 2:
            words.append(lines[i][j] + lines[i][j-1] + lines[i][j-2] + lines[i][j-3])
        if j > 2 and i > 2:
            words.append(lines[i][j] + lines[i-1][j-1] + lines[i-2][j-2] + lines[i-3][j-3])
        if i > 2:
            words.append(lines[i][j] + lines[i-1][j] + lines[i-2][j] + lines[i-3][j])
        if i > 2 and j <= cols - 4:
            words.append(lines[i][j] + lines[i-1][j+1] + lines[i-2][j+2] + lines[i-3][j+3])
        part1 += sum(1 for w in words if w == "XMAS")

        # part 2
        if j > 1 and i > 1:
            up_left = lines[i][j] + lines[i-1][j-1] + lines[i-2][j-2]
            up_right = lines[i][j-2] + lines[i-1][j-1] + lines[i-2][j]
            if i == 2 and j == 3:
                print(up_left, up_right)
            if (up_left == "MAS" or up_left == "SAM") and (up_right == "MAS" or up_right == "SAM"):
                part2 += 1

print(f"Part1: {part1}")
print(f"Part2: {part2}")
```

## Day 5

The problem: [link](https://adventofcode.com/2024/day/5)

The solution:

```python
# Pardon my ugly code
part1 = 0
part2 = 0
rules = {}
incorrect = []

def check(update):
    for i in range(len(update)):
        # is cur in set of any later nums?
        for j in range(i,len(update)):
            if update[j] in rules:
                if update[i] in rules[update[j]]:
                    return 0

        # any earlier nums in set of cur?
        if update[i] in rules:
            for j in range(0,i):
                if update[j] in rules[update[i]]:
                    return 0
    return update[(len(update) - 1) // 2]

with open("./input.txt", "r") as f:
    line = f.readline()
    while line != "\n":
        l,r = line.split("|")
        l = int(l)
        r = int(r)
        if l not in rules:
            rules[l] = set()
        rules[l].add(r)
        line = f.readline()
    
    updates = []
    for l in f.readlines():
        cur = l.strip().split(",")
        updates.append([int(n) for n in cur])
    
    for update in updates:
        ret = check(update)
        part1 += ret
        if ret == 0:
            incorrect.append(update)
    
for update in incorrect:
    pages = []
    ret = 0
    while update:
        cur = update.pop()
        for i in range(len(pages) + 1):
            new_list = pages.copy()
            new_list.insert(i, cur)
            ret = check(new_list)
            if ret:
                pages = new_list.copy()
                break
    part2 += ret

print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
```

## Day 6

The problem: [link](https://adventofcode.com/2024/day/6)

The solution:

```python
import copy

RIGHT = 1
DOWN = 2
LEFT = 4
UP = 8

with open("./input.txt", "r") as f:
    rows = [list(l.strip()) for l in f.readlines()]

def run(rows):
    xgrid = [[0 for i in range(len(rows[0]))] for j in range(len(rows))]
    headings = [[0 for i in range(len(rows[0]))] for j in range(len(rows))]

    for y,r in enumerate(rows):
        if "^" in r:
            x = r.index("^")
            break

    dir = "up"
    while True:
        xgrid[y][x] = 1
        new_x = x
        new_y = y
        if dir == "up":
            if y == 0:
                break
            new_y -= 1
        if dir == "down":
            if y >= len(rows) - 1:
                break
            new_y += 1
        if dir == "right":
            if x >= len(rows[0]) - 1:
                break
            new_x += 1
        if dir == "left":
            if x < 0:
                break
            new_x -= 1
        
        if rows[new_y][new_x] == "#":
            if dir == "up":
                if headings[y][x] & UP:
                    return 0
                else:
                    headings[y][x] |= UP
                dir = "right"
            elif dir == "right":
                if headings[y][x] & RIGHT:
                    return 0
                else:
                    headings[y][x] |= RIGHT
                dir = "down"
            elif dir == "down":
                if headings[y][x] & DOWN:
                    return 0
                else:
                    headings[y][x] |= DOWN
                dir = "left"
            elif dir == "left":
                if headings[y][x] & LEFT:
                    return 0
                else:
                    headings[y][x] |= LEFT
                dir = "up"
            continue

        x = new_x
        y = new_y

    return sum(sum(r) for r in xgrid)

part2 = 0
for i in range(len(rows)):
    for j in range(len(rows[0])):
        print(i,j)
        if rows[i][j] != "#" and rows[i][j] != "^":
            temp_grid = copy.deepcopy(rows)
            temp_grid[i][j] = "#"
            if run(temp_grid) == 0:
                part2 += 1

print(f"Part 1: {run(rows)}")
print(f"Part 1: {part2}")
```

## Day 7

After solving [the problem](https://adventofcode.com/2024/day/7) today in python, I wondered how much faster it would be in C, so I did both.

| Language | Part 1 Time (sec) | Part 2 Time (sec) |
|----------|-------------------|-------------------|
| C | 0.022 | 0.021 |
| Python | 0.471 | 22.463 |


The solution (in Python and C):

```python
MUL = 0
ADD = 1
CAT = 2

# set to 1 or 2 to get answer for part 1 or 2
PART = 2

def get_ins(n):
    instructions = []
    while n >= 0:
        instructions.append(n % (PART + 1))
        n //= (PART + 1)
        if n == 0:
            break
    return instructions

if __name__ == "__main__":
    with open("./input.txt", "r") as f:
        lines = [l[:-1] for l in f.readlines()]
    
    ans = 0
    for line in lines:
        parts = line.split(":")
        target = int(parts[0])
        operands = parts[1].strip().split(" ")

        # total possible permutations of equations
        total = (PART + 1) ** (len(operands) - 1)
        for n in range(total):
            ins = get_ins(n)
            cur = 0
            while len(ins) < len(operands) - 1:
                ins.append(0)
            res = int(operands[0])
            for o in operands[1:]:
                i = ins[cur]
                if i == MUL:
                    res *= int(o)
                elif i == ADD:
                    res += int(o)
                elif i == CAT:
                    res = int(str(res) + o)
                cur += 1
            if target == res:
                ans += target
                break

    print(ans)
```

```c
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define MUL 0
#define ADD 1
#define CAT 2

#define PART 2

#define OPSSIZE 16

int* get_ops(int n, unsigned int b, int *ops, size_t s) {
    // make sure res is large enough to hold result
    if (pow(b, s) < n)
        return NULL;
    int *p = ops;
    while (n >= 0) {
        *p = n % b;
        n = n / b;
        if (n == 0)
            break;
        p++;
    }
    return ops;
}

int main() {
    unsigned long ans = 0;
    FILE *file = fopen("./input.txt", "r");
    if (file == NULL) return EXIT_FAILURE;

    char line[256] = {0};
    while (fgets(line, sizeof(line), file) != NULL) {
        char *endptr;
        long target = strtol(line, &endptr, 10);
        int nums[32] = {0};
        int num_sz = 0;
        char *p;
        while (*endptr != '\n') {
            p = endptr + 1;
            nums[num_sz++] = (int) strtol(p, &endptr, 10);
        };

        int total = PART == 1 ? pow(2, num_sz - 1) : pow(3, num_sz - 1);
        for (int n = 0; n < total; n++) {
            long outcome = (long)nums[0];
            int ops[OPSSIZE] = {0};
            if (PART == 1) {
                get_ops(n, 2, ops, OPSSIZE);
            }
            else if (PART == 2) {
                get_ops(n, 3, ops, OPSSIZE);
            }
            else {
                fclose(file);
                puts("ERROR: PART must be 1 or 2.");
            }
            for (int i = 1; i < num_sz; i++) {
                int op = ops[i-1];
                if (op == MUL)
                    outcome = outcome * nums[i];
                else if (op == ADD) {
                    outcome = outcome + nums[i];
                }
                else if (op == CAT) {
                    char cat[64];  // plenty big for input
                    sprintf(cat, "%ld%d", outcome, nums[i]);
                    outcome = strtol(cat, NULL, 10);
                }
            }
            if (outcome == target) {
                ans += target;
                break;
            }
        }
    }
    printf("%ld\n", ans);
    fclose(file);
    return 0;
}
```

## Day 8

The problem: [link](https://adventofcode.com/2024/day/8)

The solution:

```python
from typing import Tuple

# Set to False for part 1 and True for part 2
PART2 = False

def get_antinodes(loc1: Tuple[int, int], loc2: Tuple[int, int]):
    if PART2:
        register(loc1)
        register(loc2)

    dx = abs(loc1[0] - loc2[0])
    dy = abs(loc1[1] - loc2[1])

    # loc1 always has lower y, but we don't know about x
    if loc1[0] >= loc2[0]:
        cnt = 1
        while register((loc1[0] + dx * cnt, loc1[1] - dy * cnt)):
            if not PART2:
                break
            cnt += 1
        cnt = 1
        while register((loc2[0] - dx * cnt, loc2[1] + dy * cnt)):
            if not PART2:
                break
            cnt += 1
    else:
        cnt = 1
        while register((loc1[0] - dx * cnt, loc1[1] - dy * cnt)):
            if not PART2:
                break
            cnt += 1
        cnt = 1
        while register((loc2[0] + dx * cnt, loc2[1] + dy * cnt)):
            if not PART2:
                break
            cnt += 1

def register(node: Tuple[int, int]) -> None:
    global resonance
    y = len(resonance)
    x = len(resonance[0])
    # verify if node location is on grid
    if node[0] < 0 or node[1] < 0 or node[0] >= x or node[1] >= y:
        return False
    resonance[node[1]][node[0]] = 1
    return True

with open("./input.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()]

ants = {}
for y, line in enumerate(lines):
    for x, val in enumerate(line):
        if val == ".":
            continue
        if val not in ants:
            ants[val] = [(x, y)]
        else:
            ants[val].append((x, y))

resonance = [[0 for a in range(len(lines[0]))] for b in range(len(lines))]
for ant in ants:
    for i in range(len(ants[ant])):
        # compare every antennae location combination
        for k in range(i+1, len(ants[ant])):
            get_antinodes(ants[ant][i], ants[ant][k])

print(f"Solution: {sum([sum(row) for row in resonance])}")
```
