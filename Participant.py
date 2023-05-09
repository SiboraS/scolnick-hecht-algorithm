import numpy as np
import random
import decimal
from thewalrus import perm
import hashlib


class Participant:

    def __init__(self, dim, h, t):
        decimal.getcontext().prec = 1000

        # rows_A > columns_A
        self.rows_A = self.columns_B = dim
        self.columns_A = self.rows_B = random.randint(0, dim - 1)
        self.h = h
        self.t = t
        self.core = []
        self.expo = []
        self.U = []
        self.session_key = ''

    def matrix_power_mod(self, X, expo):
        # Initialize an identity matrix I with the same size as X
        I = np.eye(X.shape[0], dtype=np.int64)

        # Express expo as a sum of powers of 2.
        powers = []
        while expo > 0:
            powers.append(expo % 2)
            expo //= 2

        # Compute the powers of X and multiply them into I
        powers_of_X = [X]
        for i in range(1, len(powers)):
            powers_of_X.append(np.matmul(powers_of_X[-1], powers_of_X[-1]) % 256)
        for i in range(len(powers)):
            if powers[i] == 1:
                I = np.matmul(I, powers_of_X[i]) % 256

        return I.astype(np.int64)

    def get_p_matrix(self):
        p = []
        for k in range(0, self.t):
            a1 = np.random.randint(256, size=(self.rows_A, self.columns_A))
            b1 = np.random.randint(256, size=(self.rows_B, self.columns_B))

            p_k = np.matmul(a1, b1)
            p_k = np.mod(p_k, 256)

            p.append(p_k)

        return p

    def set_core(self, p_a, p_b):
        for k in range(0, self.t):
            core_k = np.matmul(p_a[k], p_b[k])
            core_k = np.mod(core_k, 256)

            self.core.append(core_k)

    def set_u(self):
        for k in range(0, self.t):
            expo_k = random.randint(pow(2, self.h - 1), pow(2, self.h))
            self.expo.append(expo_k)
            u_k = self.matrix_power_mod(self.core[k], expo_k)

            self.U.append(u_k)

    def get_u(self):
        self.set_u()
        return self.U

    def set_session_key(self, u):
        a_key = []
        for k in range(0, self.t):
            v_k_pow = self.matrix_power_mod(u[k], self.expo[k])
            perm_v_k = decimal.Decimal(perm(v_k_pow))
            power = decimal.Decimal(2 ** self.h)

            a_key_k = perm_v_k % power
            a_key_k = int(a_key_k)
            if a_key_k < 0:
                a_key_k += power

            a_key.append(a_key_k)

        a_concat = ''.join(map(str, a_key))

        self.session_key = hashlib.new("sha3_512", a_concat.encode()).digest()

    def get_session_key(self, u):
        self.set_session_key(u)
        return self.session_key
