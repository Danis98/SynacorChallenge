r8 = 1

dp = {}

err = False
msg = ""

maxr1=0
maxr2=0

def f(r1, r2):
    global maxr1, maxr2, dp
    state = (r1, r2)
    if state in dp:
        return dp[state]
    if r1 != 0:
        if r2 != 0:
            dp[state] = f(r1-1, f(r1, r2-1))
            return dp[state]
        dp[state] = f(r1-1, r8)
        return dp[state]
    dp[state] = (r2+1) % 0x8000
    return dp[state]

def iterative_dp():
    for r1 in xrange(0, 4):
        for r2 in xrange(0, 0x8000):
            state = (r1, r2)
            if r1 == 0:
                dp[state] = (r2 + 1) % 0x8000
            elif r1 == 1:
                dp[state] = (r8 + r2 + 1) % 0x8000
            elif r1 == 2:
                dp[state] = ((r2 + 2) * r8 + r2 + 1) % 0x8000
            elif r1 == 3:
                if r2 == 0:
                    dp[state] = (r8**2 + 3*r8 + 1) % 0x8000
                else:
                    dp[state] = ((r8 +1) * dp[(3, r2-1)] + 2*r8 + 1) % 0x8000

for v in xrange(0, 0x8000):
    r8 = v
    err = False
    msg = "%04x: " % r8
    dp = {}
    maxr1 = 0
    maxr2 = 0
    try:
        iterative_dp()
        res = f(4, 1)
        # res = (2**(2**(r8+3)-3)-3) % 0x8000
    except RuntimeError as e:
        msg += "Maximum recursion depth exceeded (%d, %d)" % (maxr1, maxr2)
        err = True
    if not err:
        msg += "%d (%d, %d)" % (res, maxr1, maxr2)
    if res < 0x10:
        print msg
    if v % 0x100 == 0:
        print "%04x reached" % v
