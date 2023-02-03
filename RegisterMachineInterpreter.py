class Runtime(Exception):
    pass


class Register:
    value = '00000000'

    def set(self, value):
        self.value = ''
        for i in range(8):
            self.value = str(value % 2) + self.value
            value = value >> 1


class RegisterMachineInterpreter:
    registers = {}
    data = ''
    reading = 0

    def syntaxis(self, code):
        for label in range(len(code)):
            command = code[label]
            operator = command[0]
            if operator == '?':
                r = command[2:]
                if len(r) == 0 or not r.isdigit() or r.count(' ') != 0:
                    raise Exception()
            if operator == '^':
                r, L1 = command[2:].split()
                if r.isdigit() or not L1.isdigit():
                    raise Exception()
            if operator == '@':
                r = command[2:]
                if len(r) == 0 or r.isdigit() or r.count(' ') != 0:
                    raise Exception()
            if operator == '=':
                r1, r2, L1 = command[2:].split(' ')
                if r1.isdigit() or not L1.isdigit():
                    raise Exception()
            if operator == '#':
                r1, r2, L1 = command[2:].split(' ')
                if r1.isdigit() or not L1.isdigit():
                    raise Exception()
            if operator == '&':
                registers = command[2:]
                r1, r2 = registers.split(' ')
                if r1.isdigit():
                    raise Exception()
            if operator == '!':
                r = command[2:]
                if len(r) == 0 or r.isdigit() or r.count(' ') != 0:
                    raise Exception()
            if operator == ')':
                r = command[2:]
                if len(r) == 0 or r.isdigit() or r.count(' ') != 0:
                    raise Exception()
            if operator == '(':
                registers = command[2:]
                r1, r2 = registers.split()
                if r1.isdigit():
                    raise Exception()
            if operator == '/':
                if len(command[2:]) != 0:
                    raise Exception()

    def parse(self, raw_code):
        code = []
        operators = ['(', ')', '!', '@', '#', '=', '/', '%', '&', '^', '?']
        data = ''
        j = -1
        is_data = False
        for i in raw_code:
            if not is_data:
                if i in operators:
                    j += 1
                    code.append(i + ' ')
                elif i == ',':
                    code[j] += ' '
                else:
                    code[j] += i
                if i == '%':
                    is_data = True
            else:
                data += i
        return code, data

    def set(self, registers):
        r1, r2 = registers.split(' ')
        if r2.isnumeric():
            data = int(r2)
        else:
            data = int(self.registers[r2].value, 2)
        self.registers[r1] = Register()
        self.registers[r1].set(data)

    def dump(self, command):
        for key in self.registers:
            print(f'{key}: {self.registers[key].value}')

    def jump(self, label, command):
        r, L1 = command.split()
        self.registers[r] = Register()
        self.registers[r].set(label + 1)
        return int(L1)

    def eq(self, label, command):
        r1, r2, L1 = command.split(' ')
        r1_value = int(self.registers[r1].value, 2)
        if r2.isnumeric():
            r2_value = int(r2)
        else:
            r2_value = int(self.registers[r2].value, 2)
        if r1_value % 256 == r2_value % 256:
            return int(L1)
        else:
            return label + 1

    def neq(self, label, command):
        r1, r2, L1 = command.split(' ')
        r1_value = int(self.registers[r1].value, 2)
        if r2.isnumeric():
            r2_value = int(r2)
        else:
            r2_value = int(self.registers[r2].value, 2)
        if r1_value % 256 != r2_value % 256:
            return int(L1)
        else:
            return label + 1

    def read(self, r):
        self.registers[r] = Register()
        if self.reading >= len(self.data):
            raise Runtime('ok')
        data = self.data[self.reading]
        self.registers[r].set(int(data))
        self.reading += 1

    def right(self, r):
        self.registers[r].value = self.registers[r].value[:-1]
        if len(self.registers[r].value) == 0:
            self.registers[r].value = '0'

    def left(self, registers):
        r1, r2 = registers.split()
        reg = Register()
        if r2.isnumeric():
            value = int(r2)
        else:
            value = int(self.registers[r2].value, 2)
            self.registers[r2].value = ''
        reg.set(value)
        reg.value.lstrip('0')
        self.registers[r1].value += reg.value

    def goback(self, r):
        return int(self.registers[r].value, 2)

    def goto(self, r):
        return int(r)

    def execute(self, label, command):
        operator = command[0]
        if operator == '?':
            return self.goto(command[2:])
        if operator == '^':
            return self.jump(label, command[2:])
        if operator == '@':
            return self.goback(command[2:])
        if operator == '=':
            return self.eq(label, command[2:])
        if operator == '#':
            return self.neq(label, command[2:])
        if operator == '&':
            self.set(command[2:])
        if operator == '!':
            self.read(command[2:])
        if operator == ')':
            self.right(command[2:])
        if operator == '(':
            self.left(command[2:])
        if operator == '/':
            self.dump(command[2:])
        if operator == '%':
            return -1
        return label + 1

    def interpret(self, raw_code):
        moves = 0
        code, self.data = self.parse(raw_code)
        # print(code)
        if code[-1] != '% ':
            raise Runtime('ok')
        self.syntaxis(code)
        label = 0
        command = code[label]
        while label >= 0 and moves < 100:
            label = self.execute(label, command)
            command = code[label]
            moves += 1
        if moves >= 100:
            raise Exception
        if self.reading != len(self.data):
            a = 1 / 0
        self.registers = {}
        self.data = ''
        self.reading = 0
