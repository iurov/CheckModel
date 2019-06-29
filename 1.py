dct = {}
chreb = 0
chver = 0
chf = 0
f = open('test.obj')
for line in f.readlines():
    if line[0] + line[1] == 'v ':
        chver += 1
    if line[0] == 'f':
        chf += 1
        for i in range(len(line)):
            if (line[i]=='/') and (line[i-1]!='/'):
                l = i-1
                s = ''
                while ( line[l] >= '0' ) and ( line[l]<= '9'):
                    s += line[l]
                    l -=1
                k = s[::-1]
                chreb += 1
                if k in dct:
                    dct[k] += 1
                else:
                    dct[k] = 1 

eiler = chver - (chreb//2) + chf
if eiler != 2:
    print('Фигуры не замкнуты')
else:
    print('Фигуры замкнуты')

# for i in sorted(dct):
#     print("'%d':%d" % (int(i),dct[i]))
# print(dct)
# for i in dct:
#     if dct[i] < 3:
#         k = 1

# if k ==1:
#     print('Фигуры не замкнуты')
# else:
#     print('Фигуры замкнуты')