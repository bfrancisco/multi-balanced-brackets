import random, subprocess

ALPHA = "{}()<>[]{}()<>[]{}()<>[]x" # more probability for brackets
    
def generate():
    ret = "!"
    n = random.randint(1, 10)
    for _ in range(n):
        ret += random.choice(ALPHA)
    ret += "!"

# def generate_cases(t):
#     for i in range(t):
#         s = generate()
#         print(generate())
# generate_cases(100)

sol1 = input("Solution 1 file: ")
sol2 = input("Solution 2 file: ")

passed = 0
input_file = "input_stress_isbalanced.txt"
while passed <= 1000:
    test_case = generate()
    with open(input_file, mode='w') as f:
        print(test_case, file=f)
    p1 = subprocess.run(
        f'py {sol1} < {input_file}',
        check=True, shell=True, capture_output=True, text=True
    )
    p2 = subprocess.run(
        f'py {sol2} < {input_file}',
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