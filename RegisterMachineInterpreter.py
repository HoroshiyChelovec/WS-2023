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

    def execute(self, label, command):
        operator = command[0]
        if operator == '?':
            return int(command[2:])
        if operator == '^':
            return self.jump(label, command[2:])
        if operator == '@':
            return int(self.registers[command[2:]].value, 2)
        if operator == '&':
            self.set(command[2:])
        if operator == '/':
            self.dump()
        if operator == '%':
            return -1
        return label + 1

    def interpret(self, code):
        label = 0
        command = code[label]
        while label >= 0:
            label = self.execute(label, command)
            command = code[label]
