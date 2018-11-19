import time

LAE = []
SAE = []
CAE = []
effiS = {}
effiL = {}
p = []
b = []
SAN = []
LAN = []

memS = {}
memL = {}
f = open('something.txt', 'w+')


def SPLA(node):
    maxES = -1
    f.write(str(['SPLA', node.value, node.EL, node.ES]))
    f.write('\n')
    try:
        return memS[node.value]
    except:

        for child in node.children:
            if child.noMoveL:
                ES, EL = SPLA(child)
            else:
                ES, EL = LHSA(child)
            if maxES < ES:
                node.ES = ES
                node.EL = EL
                maxES = ES

        memS[node.value] = [node.ES, node.EL]
        return node.ES, node.EL


def LHSA(node):
    maxEL = -1
    f.write(str(['LHSA', node.value, node.EL, node.ES]))
    f.write('\n')
    try:
        return memL[node.value]
    except:

        # print node.value
        for child in node.children:
            if child.noMoveS:
                ES, EL = LHSA(child)
            else:
                ES, EL = SPLA(child)
            if maxEL < EL:
                node.ES = ES
                node.EL = EL
                maxEL = EL

        memL[node.value] = [node.ES, node.EL]
        return node.ES, node.EL


def allnneg(arr):
    for i in arr:
        if i < 0:
            return False
    return True


class State:

    def __init__(self, L, S, currES, currEL, bedR, parkR, currPS=True, noMovesS=False, noMovesL=False):
        self.L = L
        self.S = S
        self.currES = currES
        self.currEL = currEL
        self.bedR = bedR
        self.parkR = parkR
        self.currPS = currPS
        self.noMovesS = noMovesS
        self.noMovesL = noMovesL

    def nextiter(self):
        global LAE, SAE, CAE, effiS, effiL, p, b, SAN, LAN
        if self.noMovesS and self.noMovesL:
            return []

        if self.currPS or self.noMovesL:
            li = []
            found = False
            for i in CAE + SAE:
                if i not in self.S + self.L:
                    a = [x - y for x, y in zip(self.parkR, i[1])]
                    if allnneg(a):
                        found = True
                        li.append(State(self.L, self.S + [i], self.currES + effiS[i[0]], self.currEL, self.bedR, a,
                                        False))

            if not found:  # change this to add the ones with the max number of ones
                li.append(State(self.L, self.S, self.currES, self.currEL, self.bedR, self.parkR, False, noMovesS=True,
                                noMovesL=self.noMovesL))
            return li

        elif (not self.currPS) or self.noMovesS:
            li = []
            found = False
            for i in CAE + LAE:
                if i not in self.S + self.L:
                    a = [x - y for x, y in zip(self.bedR, i[1])]
                    if allnneg(a):
                        found = True
                        li.append(State(self.L + [i], self.S, self.currES, self.currEL + effiL[i[0]], a, self.parkR,
                                        True))
            if not found:
                li.append(State(self.L, self.S, self.currES, self.currEL, self.bedR, self.parkR, True,
                                noMovesL=True, noMovesS=self.noMovesS))

            return li

    def printer(self):
        a1 = []
        a2 = []
        for i in self.L:
            a1.append(i[0])
        for i in self.S:
            a2.append(i[0])
        # print a1
        # print a2
        # print self.currE
        # print "============================"
        return a1, a2, self.currEL, self.currES, self.noMovesS, self.noMovesL


class Node:

    def __init__(self, EL, ES, value, noMoveS, noMoveL):
        self.EL = EL
        self.ES = ES
        self.value = value
        self.noMoveS = noMoveS
        self.noMoveL = noMoveL
        self.children = []

    def addchild(self, obj):
        self.children.append(obj)


def main():
    global LAE, SAE, CAE, effiS, p, b, SAN, LAN, effiL
    f = open("input5", 'r')
    b = [int(f.readline().strip())] * 7
    bs = b[0] * 7.0
    p = [int(f.readline().strip())] * 7
    ps = p[0] * 7.0  # type: float
    L = int(f.readline().strip())
    LA = []
    SA = []
    for _ in range(L):
        LA.append(int(f.readline().strip()))
    S = int(f.readline().strip())
    for _ in range(S):
        SA.append(int(f.readline().strip()))
    A = int(f.readline().strip())
    AA = []
    for _ in range(A):
        AA.append(f.readline().strip())

    """Splitting input"""
    for i in AA:
        LAEB = (i[9] == 'N' and i[5] == 'F' and int(i[6:9]) > 17)
        SAEB = (i[10:13] == "NYY")

        id = int(i[:5])
        d = [int(x) for x in i[13:]]

        LAB = id in LA
        SAB = id in SA

        '''Update B and P'''
        '''Update efficiency'''
        effiS[id] = sum(d) / ps
        effiL[id] = sum(d) / bs

        if LAB:
            b = [b[j] - d[j] for j in range(len(d))]
            LAN.append([id, d])
            continue
        if SAB:
            p = [p[j] - d[j] for j in range(len(d))]
            SAN.append([id, d])
            continue

        '''update LAE, SAE, CAE'''
        if SAEB and LAEB:
            CAE.append([id, d])
        elif SAEB:
            SAE.append([id, d])
        elif LAEB:
            LAE.append([id, d])
    bfsQ = []
    hashmap = {}
    print LAE
    print CAE
    print SAE
    print effiL
    print effiS

    import xlwt
    filename = "python_excel_test.xls"
    excel_file = xlwt.Workbook()
    sheet = excel_file.add_sheet('2016')
    row = 0
    answer = []
    for i in CAE + SAE:
        print "here1"
        if allnneg([(x - y) for x, y in zip(p, i[1])]):
            e = 0
            # for j in SAN:
            #     e += sum(j[1])
            # e = e / ps
            a = [x - y for x, y in zip(p, i[1])]
            state = State([], [i], e + effiS[i[0]], 0, b, a, False)

            bfsQ.append(state)
            first = True
            while bfsQ:
                '''bfs shit'''
                # k = []
                # for j in bfsQ:
                #     t = j.printer()
                #     k.append((t[0], t[1]))
                # print k

                a = bfsQ.pop()
                k = a.printer()
                value = (str(sorted(k[0])).replace(' ', '') + str(sorted(k[1])).replace(' ', ''))
                node = Node(k[2], k[3], value,k[4],k[5])
                if first:
                    answer.append([i[0], node])
                    first = False
                try:
                    node = hashmap[value]
                except:
                    hashmap[value] = node

                '''excel shit'''
                something = a.printer()
                sheet.write(row, 0, str(something[0]))
                sheet.write(row, 1, str(something[1]))
                sheet.write(row, 2, str(something[2]))
                sheet.write(row, 3, str(something[3]))
                row += 1
                if row == 65536:
                    row = 0
                    sheet = excel_file.add_sheet(str(time.strftime("%Y%m%d-%H%M%S")))
                t = a.nextiter()
                t1 = []
                for n in t:
                    k = n.printer()
                    chivalue = (str(sorted(k[0])).replace(' ', '') + str(sorted(k[1])).replace(' ', ''))
                    if chivalue == value:
                        t1.append(n)
                        continue
                    try:
                        trysome = hashmap[chivalue]
                        node.addchild(trysome)
                    except:
                        chinode = Node(k[2], k[3], chivalue,k[4],k[5])
                        node.addchild(chinode)
                        hashmap[chivalue] = chinode
                        t1.append(n)
                bfsQ += t1
    excel_file.save(str(time.strftime("%Y%m%d-%H%M%S") + filename))

    maximum = 0
    for i in answer:
        semians = SPLA(i[1])[0]
        print semians, i[0]
        if maximum < semians:
            maximum = semians
            maxi = i[0]

    print '%05d' % maxi


if __name__ == "__main__":
    main()
    f.close()
