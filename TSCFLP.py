import math


class TSCFLP:
    # Number of plants
    I = None
    # Number of depots
    J = None
    # Number of customer
    K = None
    # fi is the fixed cost associated to plant i ∈ I
    f = None
    # gj is the fixed cost associated to depot j ∈ J;
    g = None
    # cij is the transportation cost of one unit of the product between plant i ∈ I and depot j ∈ J;
    c = None
    # djk is the transportation cost of one unit of the product between depot j ∈ J and customer k ∈ K ;
    d = None
    # qk is the demand of customer k ∈ K;
    q = None
    # bi is the capacity of plant i ∈ I
    b = None
    # pj is the capacity of satellite j ∈ J.
    p = None
    # Total demand
    Tq = None

    def __init__(self, i, j, k, f, g, c, d, q, b, p):
        self.I = i
        self.J = j
        self.K = k
        self.f = f
        self.g = g
        self.c = c
        self.d = d
        self.q = q
        self.b = b
        self.p = p
        self.Tq = sum(q)

    def Z(self, V):

        V = self.Decode(V)

        Z = 0
        for i in range(self.I):
            Z += self.f[i] * V.y[i]

        for j in range(self.J):
            Z += self.g[j] * V.z[j]

        for i in range(self.I):
            for j in range(self.J):
                Z += self.c[i][j] * V.x[i][j]

        for j in range(self.J):
            for k in range(self.K):
                Z += self.d[j][k] * V.s[j][k]

        V.fitnes = Z
        return V

    def Decode(self, V):
        y = [0] * self.I
        z = [0] * self.J
        x = []
        for i in range(self.I):
            x.append([0] * self.J)
        s = []
        for j in range(self.J):
            s.append([0] * self.K)

        # select plan to open
        capPlan = 0
        for i in range(self.I):
            if V.genes[i] >= 0.5:
                capPlan += self.b[i]
                y[i] = 1

        if capPlan < self.Tq:
            vp = []

            for i in range(self.I):
                vp.append([i, V.genes[i]])
            vp = sorted(vp, key=lambda x: x[1], reverse=True)

            for i in range(self.I):
                if vp[i][1] < 0.5:
                    y[vp[i][0]] = 1
                    capPlan += self.b[vp[i][0]]

                if capPlan >= self.Tq:
                    break

        # select depot for opening
        capDepot = 0
        for j in range(self.J):
            if V.genes [self.I + j] >= 0.5:
                capDepot += self.p[j]
                z[j] = 1

        if capDepot < self.Tq:
            vd = []

            for j in range(self.J):
                vd.append([j, V.genes[self.I + j]])

            vd = sorted(vd, key=lambda x: x[1], reverse=True)

            for j in range(self.J):
                if vd[j][1] < 0.5:
                    z[vd[j][0]] = 1
                    capDepot += self.b[vd[j][0]]

                if capDepot >= self.Tq:
                    break

        # transportation flow from plants to depots
        deman = 0
        for i in range(self.I):
            if y[i] == 1:
                cp = []
                for j in range(self.J):
                    if z[j] == 1:
                        cp.append([j, self.c[i][j]])
                cp = sorted(cp, key=lambda x: x[1], reverse=False)

                capd = 0
                for j in cp:
                    temp = self.p[j[0]]

                    if deman + temp > self.Tq:
                        temp = self.Tq - deman

                    if capd + temp > self.b[i]:
                        temp = self.b[i] - capd

                    t2 = sum([x[q][j[0]] for q in range(self.I)])
                    if t2 + temp > self.p[j[0]]:
                        temp = self.p[j[0]] - t2

                    x[i][j[0]] = temp
                    capd += temp
                    deman += temp

        # transportation flow from depots to customer

        listDepod = []
        for j in range(self.J):
            listDepod.append(sum([x[i][j] for i in range(self.I)]))

        for j in range(self.J):
            cosTransD = []
            for k in range(self.K):
                cosTransD.append([k, self.d[j][k]])
            cosTransD = sorted(cosTransD, key=lambda x: x[1], reverse=False)

            capj = 0
            for k in cosTransD:
                temp = self.q[k[0]]
                if capj == listDepod[j]:
                    break

                if capj + temp > listDepod[j]:
                    temp = listDepod[j] - capj

                tk = sum([s[j1][k[0]] for j1 in range(self.J)])
                if tk + temp > self.q[k[0]]:
                    temp = self.q[k[0]] - tk

                s[j][k[0]] = temp
                capj += temp
        V.y = y
        V.z = z
        V.x = x
        V.s = s
        return V
