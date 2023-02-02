class RegisterMachineInterpreter:
    registers = {}

    def set(self, registers):
        r1, r2 = registers.split(' ')
        if r2.isnumeric():
            data = int(r2)
        else:
            data = int(self.registers[r2], 2)
        self.registers[r1] = ''
        for i in range(8):
            self.registers[r1] = str(data % 2) + self.registers[r1]
            data = data >> 1

    def dump(self):
        for key in self.registers:
            print(f'{key}: {self.registers[key]}')

    def execute(self, label, command):
        operator = command[0]
        if operator == '?':
            return int(command[2:])
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
