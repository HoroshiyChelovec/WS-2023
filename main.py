import os
from RegisterMachineInterpreter import RegisterMachineInterpreter
programs_dir = './tests'
programs = os.listdir(programs_dir)

interpreter = RegisterMachineInterpreter()

for i in programs:
    print(i)
    with open(f'./tests/{i}', 'r') as program:
        code = []
        data = ''
        for line in program:
            if ':' in line:
                _, command = line.split(':')
                code.append(command.strip())
            else:
                data = line
                break
        try:
            interpreter.interpret(code, data)
        except:
            print('Runtime Error')
            interpreter.data = ''
            interpreter.registers = {}
            interpreter.reading = 0
