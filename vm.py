import sys

REG_NUM = 8
MEM_SIZE = 2**15
MODULO = 2**15

OP_HALT = 0
OP_SET = 1
OP_PUSH = 2
OP_POP = 3
OP_EQ = 4
OP_GT = 5
OP_JMP = 6
OP_JT = 7
OP_JF = 8
OP_ADD = 9
OP_MULT = 10
OP_MOD = 11
OP_AND = 12
OP_OR = 13
OP_NOT = 14
OP_RMEM = 15
OP_WMEM = 16
OP_CALL = 17
OP_RET = 18
OP_OUT = 19
OP_IN = 20
OP_NOP = 21

# Init stack
stack = []
# Init mem
mem = [0 for i in xrange(0, MEM_SIZE)]
# Init regs
regs = {}
for i in xrange(0, REG_NUM):
    regs[MEM_SIZE+i] = 0

# Load program
program_hex = map(ord, open('challenge.bin').read())
for i in xrange(0, len(program_hex), 2):
    mem[i/2] = program_hex[i] | program_hex[i+1]<<8

# Helper, get value
def get_value(num):
    if num < MODULO:
        return num
    elif num in regs:
        return regs[num]
    else:
        print "INVALID NUM %d" % num
        quit()

breakpoints = [0x154b]

# Execute instructions
instr_ptr = 0
halt = False
while instr_ptr >= 0 and instr_ptr < MEM_SIZE and not halt:
    if instr_ptr in breakpoints:
        print "BREAKPOINT %d REACHED at 0x%04x" % (breakpoints.index(instr_ptr), instr_ptr)
        sys.stdin.read(1)
    op = mem[instr_ptr]
    if op == OP_HALT:
        halt = True
    elif op == OP_SET:
        a = mem[instr_ptr+1]
        b = get_value(mem[instr_ptr+2])
        if a not in regs:
            print "[FATAL] NONEXISTING REG %d" % a
            quit()
        regs[a] = b
        instr_ptr += 3
    elif op == OP_PUSH:
        a = get_value(mem[instr_ptr+1])
        stack.append(a)
        instr_ptr += 2
    elif op == OP_POP:
        a = mem[instr_ptr+1]
        if not stack:
            print "[FATAL] POP FROM EMPTY STACK"
            quit()
        if a not in regs:
            print "[FATAL] NONEXISTING REG %d" % a
            quit()
        regs[a] = stack.pop()
        instr_ptr += 2
    elif op == OP_EQ:
        a = mem[instr_ptr+1]
        b = get_value(mem[instr_ptr+2])
        c = get_value(mem[instr_ptr+3])
        if a not in regs:
            print "[FATAL] NONEXISTING REG %d" % a
            quit()
        regs[a] = 1 if b == c else 0
        instr_ptr += 4
    elif op == OP_GT:
        a = mem[instr_ptr+1]
        b = get_value(mem[instr_ptr+2])
        c = get_value(mem[instr_ptr+3])
        if a not in regs:
            print "[FATAL] NONEXISTING REG %d" % a
            quit()
        regs[a] = 1 if b > c else 0
        instr_ptr += 4
    elif op == OP_JMP:
        a = get_value(mem[instr_ptr+1])
        instr_ptr = a
    elif op == OP_JT:
        a = get_value(mem[instr_ptr+1])
        b = get_value(mem[instr_ptr+2])
        if a != 0:
            instr_ptr = b
        else:
            instr_ptr += 3
    elif op == OP_JF:
        a = get_value(mem[instr_ptr+1])
        b = get_value(mem[instr_ptr+2])
        if a == 0:
            instr_ptr = b
        else:
            instr_ptr += 3
    elif op == OP_ADD:
        a = mem[instr_ptr+1]
        b = get_value(mem[instr_ptr+2])
        c = get_value(mem[instr_ptr+3])
        if a not in regs:
            print "[FATAL] NONEXISTING REG %d" % a
            quit()
        regs[a] = (b + c) % MODULO
        instr_ptr += 4
    elif op == OP_MULT:
        a = mem[instr_ptr+1]
        b = get_value(mem[instr_ptr+2])
        c = get_value(mem[instr_ptr+3])
        if a not in regs:
            print "[FATAL] NONEXISTING REG %d" % a
            quit()
        regs[a] = (b * c) % MODULO
        instr_ptr += 4
    elif op == OP_MOD:
        a = mem[instr_ptr+1]
        b = get_value(mem[instr_ptr+2])
        c = get_value(mem[instr_ptr+3])
        if a not in regs:
            print "[FATAL] NONEXISTING REG %d" % a
            quit()
        regs[a] = b % c
        instr_ptr += 4
    elif op == OP_AND:
        a = mem[instr_ptr+1]
        b = get_value(mem[instr_ptr+2])
        c = get_value(mem[instr_ptr+3])
        if a not in regs:
            print "[FATAL] NONEXISTING REG %d" % a
            quit()
        regs[a] = b & c
        instr_ptr += 4
    elif op == OP_OR:
        a = mem[instr_ptr+1]
        b = get_value(mem[instr_ptr+2])
        c = get_value(mem[instr_ptr+3])
        if a not in regs:
            print "[FATAL] NONEXISTING REG %d" % a
            quit()
        regs[a] = b | c
        instr_ptr += 4
    elif op == OP_NOT:
        a = mem[instr_ptr+1]
        b = get_value(mem[instr_ptr+2])
        if a not in regs:
            print "[FATAL] NONEXISTING REG %d" % a
            quit()
        regs[a] = ~b & (MODULO-1)
        instr_ptr += 3
    elif op == OP_RMEM:
        a = mem[instr_ptr+1]
        b = get_value(mem[instr_ptr+2])
        if a not in regs:
            print "[FATAL] NONEXISTING REG %d" % a
            quit()
        regs[a] = mem[b]
        instr_ptr += 3
    elif op == OP_WMEM:
        a = get_value(mem[instr_ptr+1])
        b = get_value(mem[instr_ptr+2])
        mem[a] = b
        instr_ptr += 3
    elif op == OP_CALL:
        a = get_value(mem[instr_ptr+1])
        stack.append(instr_ptr+2)
        instr_ptr = a
    elif op == OP_RET:
        ret_addr = stack.pop()
        instr_ptr = ret_addr
    elif op == OP_OUT:
        a = get_value(mem[instr_ptr+1])
        sys.stdout.write(chr(a))
        instr_ptr += 2
    elif op == OP_IN:
        a = mem[instr_ptr+1]
        if a not in regs:
            print "[FATAL] NONEXISTING REG %d" % a
            quit()
        regs[a] = ord(sys.stdin.read(1))
        instr_ptr += 2
    elif op == OP_NOP:
        instr_ptr += 1
print "Exited successfully"
