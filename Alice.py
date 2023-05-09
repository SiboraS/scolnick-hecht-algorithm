import numpy as np
from Participant import Participant


class Alice(Participant):

    def __init__(self, dim, h, t):
        Participant.__init__(self, dim, h, t)

    def decode_message(self, d):
        h_compact_k_arr = np.frombuffer(self.session_key, dtype=np.uint8)

        decoded_msg = np.bitwise_xor(d, h_compact_k_arr).tobytes()
        decoded_msg = decoded_msg.strip(b'\x00').decode("UTF-8")

        return decoded_msg
