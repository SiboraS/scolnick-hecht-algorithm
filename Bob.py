import numpy as np
from Participant import Participant


class Bob(Participant):

    def __init__(self, dim, h, t):
        Participant.__init__(self, dim, h, t)

    def encode_message(self, message):
        msg = message.encode().ljust(64, b"\x00")

        h_compact_k_arr = np.frombuffer(self.session_key, dtype=np.uint8)
        msg_arr = np.frombuffer(msg, dtype=np.uint8)
        d = np.bitwise_xor(h_compact_k_arr, msg_arr)

        return d
