class Register:
    value = '00000000'

    def set(self, value):
        self.value = ''
        for i in range(8):
            self.value = str(value % 2) + self.value
            value = value >> 1


class RegisterMachineInterpreter:
    registers = {}

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
        if self.registers[r1].value == self.registers[r2].value:
            return int(L1)
        else:
            return label + 1

    def neq(self, label, command):
        r1, r2, L1 = command.split(' ')
        if self.registers[r1].value != self.registers[r2].value:
            return int(L1)
        else:
            return label + 1

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
        if operator == '/':
            self.dump()
        if operator == '%':
            return -1
        return label + 1

    def interpret(self, raw_code):
        code = []
        for line in raw_code:
            if ':' in line:
                _, command = line.split(':')
                code.append(command.strip())
            else:
                data = line
                break
        label = 0
        command = code[label]
        while label >= 0:
            label = self.execute(label, command)
            command = code[label]
        self.registers = {}
