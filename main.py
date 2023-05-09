from Alice import Alice
from Bob import Bob

dim = int(input('Enter the dim value >=16: '))
h = int(input('Enter the h value >=64: '))
t = int(input('Enter the number of iterations t >=10: '))

alice = Alice(dim, h, t)
bob = Bob(dim, h, t)

p_a = alice.get_p_matrix()
p_b = bob.get_p_matrix()

alice.set_core(p_a, p_b)
print(f'Alice Core: {alice.core}')
bob.set_core(p_a, p_b)
print(f'Bob Core: {bob.core}')

U = alice.get_u()
print(f'U: {U}')
V = bob.get_u()
print(f'V: {V}')

# Session key obtained by Alice
session_key_a = alice.get_session_key(V)
print("SHA3-512 Hash A_concat: ", session_key_a)

# Session key obtained by Bob
session_key_b = bob.get_session_key(U)
print("SHA3-512 Hash B_concat: ", session_key_b)

msg = input('Enter message string: ')

# Bob sends the message to Alice
D = bob.encode_message(msg)
print(f'D: {D}')

# Alice recovers the message from Bob
message = alice.decode_message(D)
print(f'Decoded message: {message}')
