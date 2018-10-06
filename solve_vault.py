room_id = 0
state = (0, 22, "")
val_queue = []

visited = []
prev = {}

adj_list = [
    [1, 4],
    [2, 5],
    [1, 3, 6],
    [2, 7],
    [5, 8],
    [1, 4, 6, 9],
    [2, 5, 7, 10],
    [3, 6, 11],
    [4, 9, 12],
    [5, 8, 10, 13],
    [6, 9, 11, 14],
    [7, 10, 15],
    [8, 13],
    [9, 12, 14],
    [10, 13, 15],
    [11, 14]
]

node_val = [
    22, 0, 9, 0,
    0, 4, 0, 18,
    4, 0, 11, 0,
    0, 9, 0, 1
]

def perform_op(n, state):
    if n == 1 or n == 6 or n == 14:
        return (n, state[1], "-")
    elif n == 4:
        return (n, state[1], "+")
    elif n == 3 or n == 9 or n == 11 or n == 12:
        return (n, state[1], "*")
    else:
        if state[2] == "+":
            return (n, state[1]+node_val[n], "")
        elif state[2] == "*":
            return (n, state[1]*node_val[n], "")
        elif state[2] == "-":
            return (n, state[1]-node_val[n], "")
        else:
            print "WUT"

while state != (15, 30, ""):
    for n in adj_list[state[0]]:
        val = perform_op(n, state)
        if val in visited:
            continue
        if val[0] == 15 and val[1] != 30:
            continue
        if val[1] < 0:
            continue
        if val[1] > 1000:
            continue
        visited.append(val)
        val_queue.append(val)
        prev[val] = state
    state = val_queue.pop(0)
    print "%d - %r" % (len(val_queue), state)
print "Found"
while state in prev:
    print "%r" % (state, )
    state = prev[state]
