import os
from RegisterMachineInterpreter import RegisterMachineInterpreter, Runtime

def create_programs():
    for i in good_programs:
        program, halt = i
        if halt:
            programs.append((program + '0', halt))
            programs.append((program + '1', halt))
        else:
            for j in alphabet:
                programs.append((program + j, False))
            programs.append((program + '%', True))


operators = ['!', '@', '#', '^', '&', '/', '(', ')', '?', '=']
alphabet = operators + ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] + [chr(ord('a') + i) for i in range(26)] + [',']
programs = []
for i in operators:
    programs.append((i, False))
programs.append(('%', True))

interpreter = RegisterMachineInterpreter()
good_programs = []
bites = int(input())
w = 0
pr = 0
end = 0
pr_halt = 0
pr_not_halt = 0
for q in range(bites):
    if q != bites - 1:
        pr_halt = 0
        pr_not_halt = 0
    for i in programs:
        program, _ = i
        try:
            pr += 1
            interpreter.interpret(program)
            w += 1 / 2 ** (len(program) * 8)
            print(w, pr, program)
            end += 1
        except Runtime:
            if q != bites - 1:
                if '%' in program:
                    pr_halt += 1
                else:
                    pr_not_halt += 1
            good_programs.append((program, '%' in program))
        except:
            pass
        finally:
            interpreter.registers = {}
            interpreter.data = ''
            interpreter.reading = 0
    programs = []
    create_programs()
    good_programs = []
print(f'W:{w}\nПрограмм завершилось:{end}\nПрефиксов с HALT:{pr_halt}\nБез HALT:{pr_not_halt}')