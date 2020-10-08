import math
from pyfinite import ffield

# Rijndael S-Box
s_box =  [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67,
        0x2b, 0xfe, 0xd7, 0xab, 0x76, 0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59,
        0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0, 0xb7,
        0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1,
        0x71, 0xd8, 0x31, 0x15, 0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05,
        0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75, 0x09, 0x83,
        0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29,
        0xe3, 0x2f, 0x84, 0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b,
        0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf, 0xd0, 0xef, 0xaa,
        0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c,
        0x9f, 0xa8, 0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc,
        0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2, 0xcd, 0x0c, 0x13, 0xec,
        0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19,
        0x73, 0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee,
        0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb, 0xe0, 0x32, 0x3a, 0x0a, 0x49,
        0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
        0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4,
        0xea, 0x65, 0x7a, 0xae, 0x08, 0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6,
        0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a, 0x70,
        0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9,
        0x86, 0xc1, 0x1d, 0x9e, 0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e,
        0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf, 0x8c, 0xa1,
        0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0,
        0x54, 0xbb, 0x16]

# Rijndael Inverted S-box
inv_s_box = [0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3,
        0x9e, 0x81, 0xf3, 0xd7, 0xfb , 0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f,
        0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb , 0x54,
        0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b,
        0x42, 0xfa, 0xc3, 0x4e , 0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24,
        0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25 , 0x72, 0xf8,
        0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d,
        0x65, 0xb6, 0x92 , 0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda,
        0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84 , 0x90, 0xd8, 0xab,
        0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3,
        0x45, 0x06 , 0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1,
        0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b , 0x3a, 0x91, 0x11, 0x41,
        0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6,
        0x73 , 0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9,
        0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e , 0x47, 0xf1, 0x1a, 0x71, 0x1d,
        0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b ,
        0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0,
        0xfe, 0x78, 0xcd, 0x5a, 0xf4 , 0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07,
        0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f , 0x60,
        0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f,
        0x93, 0xc9, 0x9c, 0xef , 0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5,
        0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61 , 0x17, 0x2b,
        0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55,
        0x21, 0x0c, 0x7d]

mix_mat =  [[0x2,0x3,0x1,0x1],
			[0x1,0x2,0x3,0x1],
			[0x1,0x1,0x2,0x3],
			[0x3,0x1,0x1,0x2]]

inv_mix_mat =  [[0xe,0xb,0xd,0x9],
				[0x9,0xe,0xb,0xd],
				[0xd,0x9,0xe,0xb],
				[0xb,0xd,0x9,0xe]]

GF_irr = 283 # Irreducible Polynomial for GF(2^8) || GF(2^3) - 19
GF_8 = ffield.FField(8)

def get_s_box_lookup(r,c,inv=False):
	if inv:
		return inv_s_box[r*16 + c]
	return s_box[r*16 + c]

def transpose(state_arr):
	for i in range(4):
		for j in range(i):
			state_arr[i*4 + j],state_arr[j*4 + i] = state_arr[j*4 + i],state_arr[i*4 + j]
	return state_arr

def pretty_print_state(state_arr):
	for i in range(4):
		for j in range(4):
			print(state_arr[i*4+j], end=" ")
		print()
	print()

def get_state_hex(state_arr):
	text = 0x0
	for i in range(4):
		for j in range(4):
			text = (text<<8) + state_arr[j*4+i]
	return text

def get_rem(divisor,dividend):
		if dividend < divisor:
			return dividend
		elif dividend == divisor:
			return 0
		msb_dividend = int(math.log(dividend,2))
		msb_divisor = int(math.log(divisor,2))
		shift = msb_dividend - msb_divisor
		rem = (divisor << shift) ^ dividend
		return get_rem(divisor,rem)
				
							# ________
def gf_mult(a,b): # divisor | dividend
	prod = a*b
	c = get_rem(GF_irr,prod)
	return c

def gf_add(a,b):
	c = a ^ b
	return  c

def mix_columns(state_arr, inv=False):
	global GF_8
	mixer = mix_mat
	if inv:
		mixer = inv_mix_mat
	new_arr = [0 for i in range(16)]
	for i in range(4):
		for j in range(4):
			for k in range(4):
				# new_arr[4*i+j] = gf_add(new_arr[4*i+j],gf_mult(int(str(mixer[i][k]),16),state_arr[k*4+j]))
				m1,m2 = mixer[i][k], state_arr[k*4+j]
				new_arr[4*i+j] = gf_add(GF_8.Multiply(m1,m2),new_arr[4*i+j])
			# new_arr[4*i+j] = get_rem(GF_irr,new_arr[4*i+j])
	return new_arr

def switch_rows(state_arr, inv=False):
	if inv:
		for i in range(4):
			state_arr[4*i+(i)%4],state_arr[4*i+(i+1)%4],state_arr[4*i+(i+2)%4],state_arr[4*i+(i+3)%4] = state_arr[4*i],state_arr[4*i+1],state_arr[4*i+2],state_arr[4*i+3]
		return state_arr

	for i in range(4):
		state_arr[4*i],state_arr[4*i+1],state_arr[4*i+2],state_arr[4*i+3] = state_arr[4*i+(i)%4],state_arr[4*i+(i+1)%4],state_arr[4*i+(i+2)%4],state_arr[4*i+(i+3)%4]
	return state_arr

def encrypt(plaintext,key_sys):

	intermediate_states = []

	hex_plaintext = hex(plaintext)[2:]
	state_arr = [int("0x"+hex_plaintext[i*2:(i+1)*2],16) for i in range(16)]
	state_arr = transpose(state_arr) # read columnwisex

	state_arr = key_sys.add_rnd_key(state_arr,0)
	intermediate_states.append(get_state_hex(state_arr))

	for rnd in range(10):

		if rnd == 9:
			intermediate_states.append(get_state_hex(state_arr))

		# substitute bytes
		for i in range(len(state_arr)):
			row_ind, column_ind = int(state_arr[i]//16), int(state_arr[i]%16)
			state_arr[i] = get_s_box_lookup(row_ind,column_ind)

		# Shift rows
		state_arr = switch_rows(state_arr)

		# mix columns
		if rnd !=9:
			state_arr = mix_columns(state_arr)

		state_arr = key_sys.add_rnd_key(state_arr,rnd+1)


	ciphertext = get_state_hex(state_arr)

	return hex(ciphertext), intermediate_states
		


def decrypt(ciphertext,key_sys):

	intermediate_states = []

	hex_ciphertext = ciphertext[2:]
	state_arr = [int("0x"+hex_ciphertext[i*2:(i+1)*2],16) for i in range(16)]
	state_arr = transpose(state_arr) # read columnwisex

	for rnd in range(10):

		state_arr = key_sys.add_rnd_key(state_arr,10-rnd)

		# mix columns
		if rnd !=0:
			state_arr = mix_columns(state_arr,inv=True)

		# Shift rows
		state_arr = switch_rows(state_arr, inv=True)
		
		# substitute bytes
		for i in range(len(state_arr)):
			row_ind, column_ind = int(state_arr[i]//16), int(state_arr[i]%16)
			state_arr[i] = get_s_box_lookup(row_ind,column_ind,inv=True)

		if rnd == 0:
			intermediate_states.append(get_state_hex(state_arr))

	intermediate_states.append(get_state_hex(state_arr))

	state_arr = key_sys.add_rnd_key(state_arr,0)
	
	plaintext = get_state_hex(state_arr)

	return hex(plaintext), intermediate_states[::-1]
		

		
class KeyManager:

	def __init__(self,base_key):
		self.base_key = base_key
		self.key_arr = self.get_key_arr()
		self.round_keys = [self.key_arr]
		self.gen_rnd_keys()

	def get_key_arr(self):
		hex_plaintext = hex(self.base_key)[2:]
		state_arr = [int("0x"+hex_plaintext[i*2:(i+1)*2],16) for i in range(16)]
		state_arr = transpose(state_arr) # read columnwise
		return state_arr

	def g_box_op(self,rc):
		temp = [0 for i in range(4)]
		temp[0], temp[1], temp[2], temp[3] = self.key_arr[1*4 + 3], self.key_arr[2*4 + 3], self.key_arr[3*4 + 3], self.key_arr[0*4 + 3]
		for i in range(4):
			row_ind, column_ind = int(temp[i]//16), int(temp[i]%16)
			temp[i] = get_s_box_lookup(row_ind,column_ind)	 
		temp[0] = temp[0] ^ rc
		return temp

	def gen_rnd_keys(self):
		global GF_8
		rc = 1

		for rnd in range(10):
			temp = self.g_box_op(rc)
			rc = GF_8.Multiply(rc,2)

			for i in range(4):
				for j in range(4):
					self.key_arr[j*4+i] = temp[j] ^ self.key_arr[j*4+i]
					temp[j] = self.key_arr[j*4+i]

			self.round_keys.append(self.key_arr)

	def add_rnd_key(self,state_arr,rnd):
		for i in range(16):
			state_arr[i] = self.round_keys[rnd][i] ^ state_arr[i]
		return state_arr


def main():
	plaintexts = [0x1023456789ABCDEFFD325973CA2B310C, 0xFD325973CA2B310C1023456789ABCDEF]
	key_sys = KeyManager(base_key = 0x770A8A65DA156D24EE2A093277530142)

	print("___________________________________________________________________________")
	print()

	for plaintext in plaintexts:

		ciphertext,encrpyt_rnds = encrypt(plaintext,key_sys)
		decryptedtext,decrpyt_rnds = decrypt(ciphertext,key_sys)

		print("Original Plaintext = ",hex(plaintext))
		print("Ciphertext = ",ciphertext)
		print("Decrypted Plaintext = ",decryptedtext)
		print("Verification : Decrypted plaintext - Original plaintext = ",int(decryptedtext,16)-plaintext)
		print("===========================================================================")
		print("Verifying Intermediate States of each round during encryption and decryption")
		print("Format - Encryption state , Decryption state , Difference (Should be 0)")
		print()
		for i in range(len(encrpyt_rnds)):
			print(hex(encrpyt_rnds[i]),hex(decrpyt_rnds[i]),encrpyt_rnds[i]-decrpyt_rnds[i])
		print("___________________________________________________________________________")
		print("___________________________________________________________________________")
		print()



if __name__ == '__main__':
	main()