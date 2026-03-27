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
ID_data = [] # [(state, remaining string, stack snapshot)]
is_balanced_response = ""

def is_balanced(input_string):
    global is_balanced_response

    stack = [EMPTY_STACK_SYMBOL]
    s_i = START_STATE              # state (0, 1, 2)
    i = 0                          # input_string index. if i==n, consider an epsilon character.
    
    while i <= len(input_string):
        input_c = (input_string[i] if i < len(input_string) else "E")
        top_c = stack[-1]

        # store such values for ID
        ID_data.append(
            (
                states[s_i].symbol, 
                input_string[i:] if i < len(input_string) else "E", 
                ''.join(reversed(stack))
            )
        )

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
        is_balanced_response = f"{states[s_i].symbol} is a final state.\n{input_string} is valid and has balanced brackets."
        return True
    elif s_i not in FINAL_STATES and i >= len(input_string):
        # done reading the string BUT is not on a final state.
        is_balanced_response = f"Invalid string. {states[s_i].symbol} is not a final state."
    else:
        is_balanced_response = f"Invalid string. Failed at position {i+1}.\nRemaining unprocessed input string: {input_string[i:]}"
    return False
        
def evaluate(input_string):
    def eval(start_i, open_brckt):
        x_count = 0
        i = start_i
        while i < len(input_string):
            if input_string[i] == "x":
                x_count += 1
                i += 1
            elif input_string[i] in "<{[(":
                xs, ends_at = eval(i+1, input_string[i])
                x_count += xs
                i = ends_at+1
            elif input_string[i] == '!' or input_string[i] == BRCKT_CLOSE[open_brckt]:
                break
        
        if open_brckt == "<":
            x_count *= 2
        elif open_brckt == "{":
            x_count += 1
        elif open_brckt == "[":
            x_count = 0
        elif open_brckt == "(":
            x_count = max(0, x_count-1)

        return (x_count, i)

    x_count, ends_at = eval(1, "!")
    assert(ends_at == len(input_string)-1) # make sure that we read all characters of input_string
    return x_count

s = input()
if is_balanced(s):
    print("YES")
else:
    print("NO")
# print(evaluate(s))