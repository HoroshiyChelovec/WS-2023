import os
from RegisterMachineInterpreter import RegisterMachineInterpreter

programs_dir = './tests'
programs = os.listdir(programs_dir)

interpreter = RegisterMachineInterpreter()

for i in programs:
    print(i)
    with open(f'./tests/{i}', 'r') as program:
        code = program.read()
        try:
            interpreter.interpret(code)
        except:
            print('Runtime Error')
            interpreter.data = ''
            interpreter.registers = {}
            interpreter.reading = 0
