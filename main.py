from RegisterMachineInterpreter import RegisterMachineInterpreter, Runtime


def binary_float(x, q):
    a = '0.'
    for i in range(1, q + 1):
        if x >= 1 / 2 ** i:
            a += '1'
            x -= 1 / 2 ** i
        else:
            a += '0'
    return a


def run(program):
    global q, pr, w, end, pref_halt, pref_not_halt
    try:
        pr += 1
        interpreter.interpret(program)
        w += 1 / 2 ** (len(program) * 8)
        print(w, pr, program)
        end += 1
    except Runtime:
        if q != bites - 1:
            if '%' in program:
                pref_halt += 1
            else:
                pref_not_halt += 1
        good_programs1.append(program)
    except:
        pass
    finally:
        interpreter.registers = {}
        interpreter.data = ''
        interpreter.reading = 0


def create_programs():
    x = len(good_programs)
    while x > 0:
        program = good_programs.pop()
        if '%' in program:
            run(program + '0')
            run(program + '1')
        else:
            for j in alphabet:
                run(program + j)
        x -= 1

# -------------------------------------------------------------------------------------
bites = int(input('Байт: '))
w = 0
q = 0
pr = 0
end = 0
pref_halt = 0
pref_not_halt = 0
operators = ['!', '@', '#', '^', '&', '/', '(', ')', '?', '=', '%']
alphabet = operators + ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] + [chr(ord('a') + i) for i in range(26)] + [',']
interpreter = RegisterMachineInterpreter()
good_programs1 = []
good_programs = []
for i in operators:
    run(i)
x = len(good_programs1)
while x > 0:
    good_programs.append(good_programs1.pop())
    x -= 1
print(f'W:{binary_float(w, 64)}({w})\nПрограмм завершилось:{end}\nПрефиксов с HALT:{pref_halt}\nБез HALT:{pref_not_halt}\n----------')
for q in range(1, bites):
    if q != bites - 1:
        pref_halt = 0
        pref_not_halt = 0
    create_programs()
    print(f'W:{binary_float(w, 64)}({w})\nПрограмм завершилось:{end}\nПрефиксов с HALT:{pref_halt}\nБез HALT:{pref_not_halt}\n----------')
    x = len(good_programs1)
    while x > 0:
        good_programs.append(good_programs1.pop())
        x -= 1