class Game_State:
    def __Init__(self, state):
        self.enter = state.enter
        self.exit = state.exit
        self.pause = state.pause
        self.resume = state.resume
        self.handle_events = state.handle_events
        self.update = state.update
        self.draw = state.draw

running = None
stack = None

def change_state(state):
    global stack
    pop_state()
    stack.append(state)
    state.enter()

def push_state(state):
    global stack
    if(len(stack) > 0):
        stack[-1].pause()
    stack.append(state)
    state.enter()

def pop_state():
    global stack
    if len(stack)>0:
        stack[-1].exit()
        stack.pop()

    if len(stack) > 0:
        stack[-1].resume()

def quit():
    global running
    running= False

def run(start_state):
    global running, stack
    running = True
    stack = [start_state]
    start_state.enter()
    while(running):
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()

    while len(stack) > 0:
        stack[-1].exit
        stack.pop()


