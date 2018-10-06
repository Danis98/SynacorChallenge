import sys
import string

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[34m'
    OKGREEN = '\033[32m'
    WARNING = '\033[33m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
LINE_WIDTH = 80

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

op_memo = {
    OP_HALT: "halt",
    OP_SET: "set",
    OP_PUSH: "push",
    OP_POP: "pop",
    OP_EQ: "eq",
    OP_GT: "gt",
    OP_JMP: "jmp",
    OP_JT: "jt",
    OP_JF: "jf",
    OP_ADD: "add",
    OP_MULT: "mult",
    OP_MOD: "mod",
    OP_AND: "and",
    OP_OR: "or",
    OP_NOT: "not",
    OP_RMEM: "rmem",
    OP_WMEM: "wmem",
    OP_CALL: "call",
    OP_RET: "ret",
    OP_OUT: "out",
    OP_IN: "in",
    OP_NOP: "nop"
}

op_len = {
    OP_HALT: 1,
    OP_SET: 3,
    OP_PUSH: 2,
    OP_POP: 2,
    OP_EQ: 4,
    OP_GT: 4,
    OP_JMP: 2,
    OP_JT: 3,
    OP_JF: 3,
    OP_ADD: 4,
    OP_MULT: 4,
    OP_MOD: 4,
    OP_AND: 4,
    OP_OR: 4,
    OP_NOT: 3,
    OP_RMEM: 3,
    OP_WMEM: 3,
    OP_CALL: 2,
    OP_RET: 1,
    OP_OUT: 2,
    OP_IN: 2,
    OP_NOP: 1
}

# Init stack
stack = []
# Init mem
mem = [0 for i in xrange(0, MEM_SIZE)]
# Init regs
regs = {}
for i in xrange(0, REG_NUM):
    regs[MEM_SIZE+i] = 0
# Init instruction pointer
instr_ptr = 0
# Init halt flag
halt = False
# Saved labels
labels = {}

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

def get_memo(num):
    if num < 2**15:
        if num in labels:
            return "[%s]" % labels[num]
        return "0x%04x" % num
    elif num - 2**15 <8:
        return "r%d" % (num-2**15+1)
    else:
        # print "INVALID NUMBER %d" % num
        quit()

def get_ascii(num):
    if num < 256:
        if num == ord('\n'):
            return '\\n'
        elif num == ord('\t'):
            return '\\t'
        if num < 32:
            return "0x%04x" % num
        return "%c" % chr(num)
    elif num < 2**15:
        return "0x%04x" % num
    elif num - 2**15 <8:
        return "reg%d" % (num-2**15+1)
    else:
        # print "INVALID NUMBER %d" % num
        quit()

breakpoints = []

# Execute instruction
def exec_instr():
    global instr_ptr, mem, halt, regs, stack
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
        ret_addr= stack.pop()
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

# Decompile instruction at address
def decompile_instr(addr):
    op = mem[addr]
    if op == OP_HALT:
        return "0x%04x: %s" % (addr, op_memo[op])
    elif op == OP_SET:
        a = get_memo(mem[addr+1])
        b = get_memo(mem[addr+2])
        return "0x%04x: %s %s %s" % (addr, op_memo[op], a, b)
    elif op == OP_PUSH:
        a = get_memo(mem[addr+1])
        return "0x%04x: %s %s" % (addr, op_memo[op], a)
    elif op == OP_POP:
        a = get_memo(mem[addr+1])
        return "0x%04x: %s %s" % (addr, op_memo[op], a)
    elif op == OP_EQ:
        a = get_memo(mem[addr+1])
        b = get_memo(mem[addr+2])
        c = get_memo(mem[addr+3])
        return "0x%04x: %s %s %s %s" % (addr, op_memo[op], a, b, c)
    elif op == OP_GT:
        a = get_memo(mem[addr+1])
        b = get_memo(mem[addr+2])
        c = get_memo(mem[addr+3])
        return "0x%04x: %s %s %s %s" % (addr, op_memo[op], a, b, c)
    elif op == OP_JMP:
        a = get_memo(mem[addr+1])
        return "0x%04x: %s %s" % (addr, op_memo[op], a)
    elif op == OP_JT:
        a = get_memo(mem[addr+1])
        b = get_memo(mem[addr+2])
        return "0x%04x: %s %s %s" % (addr, op_memo[op], a, b)
    elif op == OP_JF:
        a = get_memo(mem[addr+1])
        b = get_memo(mem[addr+2])
        return "0x%04x: %s %s %s" % (addr, op_memo[op], a, b)
    elif op == OP_ADD:
        a = get_memo(mem[addr+1])
        b = get_memo(mem[addr+2])
        c = get_memo(mem[addr+3])
        return "0x%04x: %s %s %s %s" % (addr, op_memo[op], a, b, c)
    elif op == OP_MULT:
        a = get_memo(mem[addr+1])
        b = get_memo(mem[addr+2])
        c = get_memo(mem[addr+3])
        return "0x%04x: %s %s %s %s" % (addr, op_memo[op], a, b, c)
    elif op == OP_MOD:
        a = get_memo(mem[addr+1])
        b = get_memo(mem[addr+2])
        c = get_memo(mem[addr+3])
        return "0x%04x: %s %s %s %s" % (addr, op_memo[op], a, b, c)
    elif op == OP_AND:
        a = get_memo(mem[addr+1])
        b = get_memo(mem[addr+2])
        c = get_memo(mem[addr+3])
        return "0x%04x: %s %s %s %s" % (addr, op_memo[op], a, b, c)
    elif op == OP_OR:
        a = get_memo(mem[addr+1])
        b = get_memo(mem[addr+2])
        c = get_memo(mem[addr+3])
        return "0x%04x: %s %s %s %s" % (addr, op_memo[op], a, b, c)
    elif op == OP_NOT:
        a = get_memo(mem[addr+1])
        b = get_memo(mem[addr+2])
        return "0x%04x: %s %s %s" % (addr, op_memo[op], a, b)
    elif op == OP_RMEM:
        a = get_memo(mem[addr+1])
        b = get_memo(mem[addr+2])
        return "0x%04x: %s %s %s" % (addr, op_memo[op], a, b)
    elif op == OP_WMEM:
        a = get_memo(mem[addr+1])
        b = get_memo(mem[addr+2])
        return "0x%04x: %s %s %s" % (addr, op_memo[op], a, b)
    elif op == OP_CALL:
        a = get_memo(mem[addr+1])
        return "0x%04x: %s %s" % (addr, op_memo[op], a)
    elif op == OP_RET:
        return "0x%04x: %s" % (addr, op_memo[op])
    elif op == OP_OUT:
        a = get_ascii(mem[addr+1])
        return "0x%04x: %s %s" % (addr, op_memo[op], a)
    elif op == OP_IN:
        a = get_memo(mem[addr+1])
        return "0x%04x: %s %s" % (addr, op_memo[op], a)
    elif op == OP_NOP:
        return "0x%04x: %s" % (addr, op_memo[op])
    else:
        return "0x%04x: db 0x%04x" % (addr, mem[addr])

def print_state():
    print bcolors.HEADER + bcolors.BOLD + "="*LINE_WIDTH + bcolors.ENDC
    print bcolors.OKGREEN + "Registers:" + bcolors.ENDC
    print bcolors.OKBLUE + "\tinstr_ptr" + bcolors.ENDC + " = 0x%04x" % instr_ptr
    for i in xrange(0, REG_NUM, 2):
        print (bcolors.OKBLUE + "\tr%d" % (i+1) + bcolors.ENDC + " = 0x%04x " % regs[MEM_SIZE+i] + (" ("+get_ascii(regs[MEM_SIZE+i])+")" if regs[MEM_SIZE+i] < 256 and chr(regs[MEM_SIZE+i]) in string.printable else "")).ljust(40) + (bcolors.OKBLUE + "\tr%d" % (i+2) + bcolors.ENDC + " = 0x%04x " % regs[MEM_SIZE+i+1] + (" ("+get_ascii(regs[MEM_SIZE+i+1])+")" if regs[MEM_SIZE+i+1] < 256 and chr(regs[MEM_SIZE+i+1]) in string.printable else "")).ljust(40)
    print bcolors.OKGREEN + "Stack:" + bcolors.ENDC
    for i in xrange(0, min([5, len(stack)])):
        print "\t0x%04x" % stack[len(stack)-i-1]
    print bcolors.OKGREEN + "Instructions:" + bcolors.ENDC

    decompile_scope = 4
    ctr = 0
    addr = instr_ptr
    print bcolors.WARNING + bcolors.BOLD + "\t" + decompile_instr(instr_ptr) + bcolors.ENDC
    ctr = 0
    addr = instr_ptr + op_len[mem[instr_ptr]]
    while ctr < decompile_scope and addr < MEM_SIZE:
        print "\t" + decompile_instr(addr)
        if mem[addr] in op_len:
            addr += op_len[mem[addr]]
        else:
            addr += 1
        ctr += 1
    print bcolors.HEADER + bcolors.BOLD + "="*LINE_WIDTH + bcolors.ENDC

def save_snapshot(filename):
    f = open(filename, "w")
    f.write("%04x" % instr_ptr)
    f.write("%04x" % len(stack))
    for elem in stack:
        f.write("%04x" % elem)
    for i in xrange(0, MEM_SIZE):
        f.write("%04x" % mem[i])
    for i in regs:
        f.write("%04x" % regs[i])
    f.close()

def load_snapshot(filename):
    global instr_ptr, stack, mem, regs
    snap = open(filename, "r").read()
    instr_ptr = int(snap[0:4], 16)
    stack_len = int(snap[4:8], 16)
    stack = []
    for i in xrange(0, stack_len):
        stack.append(int(snap[8+4*i:12+4*i], 16))
    for i in xrange(0, MEM_SIZE):
        mem[i] = int(snap[8+4*stack_len+4*i:12+4*stack_len+4*i], 16)
    for i in xrange(0, REG_NUM):
        regs[MEM_SIZE+i] = int(snap[8+4*stack_len+4*MEM_SIZE+4*i:12+4*stack_len+4*MEM_SIZE+4*i], 16)

last_cmd = []

print_state()
while not halt and instr_ptr >= 0 and instr_ptr < MEM_SIZE:
    cmd = sys.stdin.readline().rstrip().lstrip().split()
    print ""
    if len(cmd) == 0:
        cmd = last_cmd
    else:
        last_cmd = cmd
    if len(cmd) == 0:
        continue
    if cmd[0] == 'start':
        for r in regs:
            regs[r] = 0
        instr_ptr = 0
        stack = []
        print_state()
    elif cmd[0] == 'run':
        while instr_ptr not in breakpoints:
            exec_instr()
        print_state()
    elif cmd[0] == 'step' or cmd[0] == 's':
        exec_instr()
        print_state()
    elif cmd[0] == 'break' or cmd[0] == 'b':
        if len(cmd) == 1:
            breakpoints.append(instr_ptr)
        else:
            if cmd[1] == 'list':
                for i in xrange(0, len(breakpoints)):
                    print "%d:\t0x%04x" % (i, breakpoints[i])
            else:
                breakpoints.append(int(cmd[1], 16))
    elif cmd[0] == 'remove' or cmd[0] == 'r':
        if len(cmd) != 2:
            print "Invalid sintax"
        else:
            ind = int(cmd[1])
            if ind >= len(breakpoints) or ind < 0:
                print "Non-existing breakpoint %d" % ind
            else:
                breakpoints.pop(ind)
    elif cmd[0] == 'mem':
        ptr = int(cmd[1], 16)
        block_len = int(cmd[2])
        for line_addr in xrange(ptr, ptr+block_len, 8):
            hex_mem = ""
            ascii_mem = ""
            for word_addr in xrange(line_addr, min(ptr+block_len, line_addr+8)):
                hex_mem += "0x%04x " % mem[word_addr]
                ascii_mem += chr(mem[word_addr]) if mem[word_addr] >= 32 and mem[word_addr] < 256 else "."
            print "0x%04x: %s| %s" % (line_addr, hex_mem.ljust(7*8), ascii_mem.ljust(8))
    elif cmd[0] == 'disas':
        if len(cmd) != 3:
            print "Invalid sintax"
        else:
            ptr = int(cmd[1], 16)
            if cmd[2] == 'func':
                addr = ptr
                while (mem[addr] != OP_RET and mem[addr] != OP_HALT) and addr < MEM_SIZE:
                    print decompile_instr(addr)
                    if mem[addr] in op_len:
                        addr += op_len[mem[addr]]
                    else:
                        addr += 1
                if addr < MEM_SIZE:
                    print decompile_instr(addr)
                continue
            block_len = int(cmd[2])
            ctr = 0
            addr = ptr
            while ctr < block_len and addr < MEM_SIZE:
                print decompile_instr(addr)
                if mem[addr] in op_len:
                    addr += op_len[mem[addr]]
                else:
                    addr += 1
                ctr += 1
    elif cmd[0] == 'snap':
        ind = int(cmd[2])
        if cmd[1] == 'take':
            save_snapshot('snap%d' % ind)
        elif cmd[1] == 'load':
            load_snapshot('snap%d' % ind)
            print_state()
    elif cmd[0] == 'label':
        if len(cmd) != 2 and len(cmd) != 3:
            print "Invalid sintax"
        else:
            if cmd[1] == 'list':
                    print "%d labels" % len(labels)
                    for addr in labels:
                        print "0x%04x: %s" % (addr, labels[addr])
            else:
                addr = int(cmd[1], 16)
                name = cmd[2]
                labels[addr] = name
    elif cmd[0] == 'help' or cmd[0] == 'h':
        print "Commands: start, run, step(s), break(b) list/[addr], remove(r)"

print bcolors.OKGREEN + bcolors.BOLD + "Program exited correctly" + bcolors.ENDC
