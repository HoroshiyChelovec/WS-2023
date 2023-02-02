import os
from RegisterMachineInterpreter import RegisterMachineInterpreter
programs_dir = './tests'
programs = os.listdir(programs_dir)

interpreter = RegisterMachineInterpreter()

for i in programs:
    print(i)
    with open(f'./tests/{i}', 'r') as program:
        code = []
        for line in program:
            code.append(line.strip())
        interpreter.interpret(code)
