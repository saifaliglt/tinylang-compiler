counter = 0
limit = 3
L1:
t1 = counter < limit
ifFalse t1 goto L2
print counter
t2 = counter + 1
counter = t2
goto L1
L2:
