import com.utilities as u
import numpy as np


def update_strategy(regret):
    strategy = np.copy(regret)
    strategy[strategy < 0] = 0

    summation = float(sum(strategy))
    if summation > 0:
        strategy = np.asarray(strategy)/summation
    else:
        strategy = np.asarray([1./15. for x in range(15)])
    return strategy


def regret(utility, my_move, op_move):
    t = utility[op_move][my_move]
    w = utility[op_move][:]
    return np.asarray([w[i] - t for i in range(len(w))])


def choose(probability, actions):
    return actions[np.random.choice(np.arange(0, 15), p=probability)]


def player():
    actions = ['Sponge', 'Paper', 'Air',
           'Water', 'Dragon', 'Devil',
           'Lightning', 'Gun', 'Rock',
           'Fire', 'Scissors', 'Snake',
           'Human', 'Tree', 'Wolf']

    utility = [[0, -1, -1, -1, -1, -1, -1, -1, 1, 1, 1, 1, 1, 1, 1],
               [1, 0, -1, -1, -1, -1, -1, -1, -1, 1, 1, 1, 1, 1, 1],
               [1, 1, 0, -1, -1, -1, -1, -1, -1, -1, 1, 1, 1, 1, 1],
               [1, 1, 1, 0, -1, -1, -1, -1, -1, -1, -1, 1, 1, 1, 1],
               [1, 1, 1, 1, 0, -1, -1, -1, -1, -1, -1, -1, 1, 1, 1],
               [1, 1, 1, 1, 1, 0, -1, -1, -1, -1, -1, -1, -1, 1, 1],
               [1, 1, 1, 1, 1, 1, 0, -1, -1, -1, -1, -1, -1, -1, 1],
               [1, 1, 1, 1, 1, 1, 1, 0, -1, -1, -1, -1, -1, -1, -1],
               [-1, 1, 1, 1, 1, 1, 1, 1, 0, -1, -1, -1, -1, -1, -1],
               [-1, -1, 1, 1, 1, 1, 1, 1, 1, 0, -1, -1, -1, -1, -1],
               [-1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 0, -1, -1, -1, -1],
               [-1, -1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 0, -1, -1, -1],
               [-1, -1, -1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 0, -1, -1],
               [-1, -1, -1, -1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 0, -1],
               [-1, -1, -1, -1, -1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 0]]

    if u.storage[0] is None:
        u.storage[1] = [[0 for r in range(15)], ""]
        s = update_strategy(u.storage[1][0])
        action = choose(s, actions)
        u.storage[1][1] = action
        return action
    else:
        reg = regret(utility, actions.index(u.storage[1][1]), actions.index(u.storage[0]))
        u.storage[1][0] = np.asarray(u.storage[1][0]) + reg
        s = update_strategy(u.storage[1][0])
        action = choose(s, actions)
        u.storage[1][1] = action
        return action