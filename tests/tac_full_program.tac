x = 1
y = 2.5
limit = 4
t1 = 2 * limit
t2 = x + t1
x = t2
t3 = x / 2
t4 = y + t3
y = t4
t5 = x > limit
if t5 goto L1
goto L2
L1:
print x
goto L3
L2:
print y
L3:
L4:
t6 = x < 10
ifFalse t6 goto L5
t7 = x + 1
x = t7
print x
goto L4
L5:
