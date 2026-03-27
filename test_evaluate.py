import random, subprocess

INPUT_ALPHA = set(">}])x!<{[(")
STACK_ALPHA = set("!<{[(")
EMPTY_STACK_SYMBOL = "Z"
EPSILON_SYMBOL = "E"
FINAL_STATES = set([2]) # q2
START_STATE = 0         # q0
BRCKT_CLOSE = {open : close for open, close in ["<>", "{}", "[]", "()"]} # map open brackets to its close bracket counterpart.


class Transition:
    def __init__(self, symbol: str, top: str, replaced_top: str, to_state: int):
        self.symbol = symbol
        self.top = top
        self.replaced_top = replaced_top
        self.to_state = to_state
    
    def __repr__(self):
        return f"({self.symbol}, {self.top}, {self.replaced_top})"

class State:
    input_symbols = set()
    def __init__(self, symbol: str, transitions: dict[tuple, Transition]):
        self.symbol = symbol
        self.transitions = transitions
    
    def is_valid_transition(self, input_c, top_c):
        return (input_c, top_c) in self.transitions

    def get_transition(self, input_c, top_c):
        return self.transitions[(input_c, top_c)]

states = [
    State(
        symbol="q0",
        transitions={
            ("!", EMPTY_STACK_SYMBOL) : Transition("!", EMPTY_STACK_SYMBOL, "!"+EMPTY_STACK_SYMBOL, 1)
        }
    ),
    State(
        symbol="q1",
        transitions={
            **{("x", top) : Transition("x", top, top, 1) for top in INPUT_ALPHA},
            **{(open_brckt, top) : Transition(open_brckt, top, open_brckt+top, 1) for open_brckt in BRCKT_CLOSE.keys() for top in INPUT_ALPHA},
            **{(close, open) : Transition(close, open, "", 1) for open, close in BRCKT_CLOSE.items()},
            **{("!", "!") : Transition('!', "!", "", 2)}
        } # ** operator unpacks a dictionary. here, we unpacked dictionary comprehensions and combined then into one.
    ),
    State(
        symbol="q2",
        transitions={(EPSILON_SYMBOL, EMPTY_STACK_SYMBOL) : Transition(EPSILON_SYMBOL, EMPTY_STACK_SYMBOL, EMPTY_STACK_SYMBOL, 2)}
    )
]

def is_balanced(input_string):

    stack = [EMPTY_STACK_SYMBOL]
    s_i = START_STATE              # state (0, 1, 2)
    i = 0                          # input_string index. if i==n, consider an epsilon character.
    
    while i <= len(input_string):
        input_c = (input_string[i] if i < len(input_string) else "E")
        top_c = stack[-1]

        if not states[s_i].is_valid_transition(input_c, top_c):
            break
            
        transition = states[s_i].get_transition(input_c, top_c)

        if transition.replaced_top == "":
            stack.pop()
        else:
            stack[-1] = transition.replaced_top[-1] # replace top of the stack with the last char of replaced_top
            # push all remaining chars of replaced_top in reverse order.
            for c in reversed(transition.replaced_top[:-1]):
                stack.append(c)
        
        s_i = transition.to_state
        i += 1

    if s_i in FINAL_STATES and i > len(input_string):
        return True
    return False
        

random.seed(69)
def generate():
    s_i = 0
    stack = [EMPTY_STACK_SYMBOL]
    input_string = ""
    
    while True:
        if s_i == 2:
            break
        input_c, top_c = ("garbage", "garbage")
        transition = None
        while True:
            if len(input_string) >= 10:
                if stack[-1] in BRCKT_CLOSE:
                    input_c, top_c = (BRCKT_CLOSE[stack[-1]], stack[-1])
                else:
                    input_c, top_c = ("!", "!")
                break
            else:

                input_c, top_c = random.choice(list(states[s_i].transitions.keys()))
                
                
                if top_c == stack[-1]:
                    break

        input_string += input_c
        transition = states[s_i].get_transition(input_c, top_c)
        

        if transition.replaced_top == "":
            stack.pop()
        else:
            stack[-1] = transition.replaced_top[-1] # replace top of the stack with the last char of replaced_top
            # push all remaining chars of replaced_top in reverse order.
            for c in reversed(transition.replaced_top[:-1]):
                stack.append(c)

        s_i = transition.to_state
    
    return input_string
    
# def generate_cases(t):
#     for i in range(t):
#         s = generate()
#         print(generate())
#         assert(is_balanced(s))
# generate_cases(100)

sol1 = input("Solution 1 file: ")
sol2 = input("Solution 2 file: ")

passed = 0
input_file = "input_stress_evaluate.txt"
while passed <= 1000:
    test_case = generate()
    with open(input_file, mode='w') as f:
        print(test_case, file=f)
    p1 = subprocess.run(
        f'py {sol2} < {input_file}',
        check=True, shell=True, capture_output=True, text=True
    )
    p2 = subprocess.run(
        f'py {sol1} < {input_file}',
        check=True, shell=True, capture_output=True, text=True
    )
    if p1.stdout != p2.stdout:
        print('Failed!') 
        print('Sol1 Output:', p1.stdout)
        print('Sol2 Output:', p2.stdout)  
        print("Test Case:\n" + test_case)
        break

    passed += 1
    print(f'{passed} cases passed')