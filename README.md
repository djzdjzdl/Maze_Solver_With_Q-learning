# README

## Introduction

---

### What is that Code?

- Maze Solver using Q-Learning

### How To Run?

- python Q-learning.py

### Requirements

```bash
numpy
pygame
random
turtle
```

## Source Information

---

### Classes

- Learning_Environments
    - Initialize array, states, q_table
    - Get random walls, penalties
- Q_Learning
    - Visualize Map
    - Do Q_learning

### Learning_Environments

- **__Init__ [Input - x_position, y_position]**
    - Initialize color array
    - Call `Set_Reward` function
    - Call `Set_State` function
    - Initialize Terminal
    - Initialize q_table array
- **Set_Reward**
    - Initialize reward
    - Set two penalties, walls using `Set_Penalty` , `Set_Wall` Function
    - Set goal value as reward=1
- **Set_Penalty**
    - Get random x, y position
    - if random x, y position == reward 0, and not start or goal then set reward -1
- **Set_Wall**
    - Get random x, y position
    - if random x, y position == reward 0, and not start or goal then append random position at wall array
- **Set_State**
    - Initialize State queue

### Q_Learning

- **__init__ [Input - x_position, y_position]**
    - Making Game Screen using `pygame` package
    - Do Q-learning based on current position
- **Visual_Map**
    - Visualize map as n x n
- **Select_Action**
    - Making Possible actions based on current position
- **Steps**
    - Do steps per action
    - Set actions using current state
    - calculate Q value