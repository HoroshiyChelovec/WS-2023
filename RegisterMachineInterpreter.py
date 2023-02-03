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

    def set(self, registers):
        r1, r2 = registers.split(' ')
        if r2.isnumeric():
            data = int(r2)
        else:
            data = int(self.registers[r2].value, 2)
        self.registers[r1] = Register()
        self.registers[r1].set(data)

    def dump(self):
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
        if r1_value == r2_value:
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
        if r1_value != r2_value:
            return int(L1)
        else:
            return label + 1

    def read(self, r):
        self.registers[r] = Register()
        data = self.data[self.reading]
        self.registers[r].set(int(data))
        self.reading += 1

    def right(self, r):
        self.registers[r].value = self.registers[r].value[:-1]
        if len(self.registers[r].value) == 0:
            self.registers[r].value = '0'
        # value = int(self.registers[r].value, 2) >> 1
        # self.registers[r].set(value)

    def left(self, registers):
        r1, r2 = registers.split()
        reg = Register()
        if r2.isnumeric():
            value = int(r2)
        else:
            value = int(self.registers[r2].value, 2)
        reg.set(value)
        reg.value.lstrip('0')
        self.registers[r1].value += reg.value

    def execute(self, label, command):
        operator = command[0]
        if operator == '?':
            return int(command[2:])
        if operator == '^':
            return self.jump(label, command[2:])
        if operator == '@':
            return int(self.registers[command[2:]].value, 2)
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
            self.dump()
        if operator == '%':
            return -1
        return label + 1

    def interpret(self, code, data):
        self.data = data
        label = 0
        command = code[label]
        while label >= 0:
            label = self.execute(label, command)
            command = code[label]
        if self.reading != len(self.data):
            a = 1 / 0
        self.registers = {}
        self.data = ''
        self.reading = 0