import sys

import os
import sys

class Chunk:
    offset: int
    tx_index: int
    def __init__(self, offset, tx_index):
        self.offset = offset
        self.tx_index = tx_index


def get_bitcode():
	return [0xf73524c107000000, 0x44f258daf3f32ee8,
		0xf4cfcee0ae056a88, 0x7a0b8e9827e5c162,
		0x84807c35793713ad, 0x5a576ac3c8f5ffec,
	]
 
def normalize_offset(offset):
	if offset & 0xfff != 0:
		return offset - (offset & 0xfff)
 
def decode_chunk(chunk_data, num):
	bitcode = get_bitcode()
	chunkfile = open('chunks/chunk_{}.dat'.format(num), 'wb')
 	
	for i in range(0, int(0x40000/0x8)):
		dat8 = int.from_bytes(chunk_data[i*8:i*8+8], 'little')
		res = dat8 ^ bitcode[i % 0x6]
 
		chunkfile.write(res.to_bytes(8, 'little'))
 
def parse(filename):
	print('[INFO] Loading ar file {} .....'.format(filename))
	print('[INFO] AR file size: {}'.format(os.path.getsize(filename)))
	arfile = open(filename, 'rb')

	# Read file flag 10 bytes
	file_flag = int.from_bytes(arfile.read(10), 'little')
	print('[INFO] file flag {}'.format(file_flag))
	# Read file version 4 bytes
	file_ver = int.from_bytes(arfile.read(4), 'little')
	print('[INFO] file version {}'.format(file_ver))
	# Read tx path 4 bytes
	tx_path_num = int.from_bytes(arfile.read(4), 'little')
	print('[INFO] tx path number {}'.format(hex(tx_path_num)))
	# Read chunk number 4
	chunk_num = int.from_bytes(arfile.read(4), 'little')
	print('[INFO] chunk number {}'.format(hex(chunk_num)))
	# Read offset 8
	offset = int.from_bytes(arfile.read(8), 'little')
	print('[INFO] weave offset {}'.format(hex(offset)))
	# Read weave size 8
	weave_size = int.from_bytes(arfile.read(8), 'little')
	print('[INFO] weave size {}'.format(hex(weave_size)))

	# Read tx paths
	for i in range(0, tx_path_num):
		tx_path = int.from_bytes(arfile.read(2), 'little')
		print('[INFO] tx path {}'.format(tx_path))

	chunks = []

	# Read chunks
	for i in range(0, chunk_num):
		# Read chunk offset 4
		choff = int.from_bytes(arfile.read(4), 'little')
		# Read chunk weave offset 8
		weave_offset = int.from_bytes(arfile.read(8), 'little')
		# Read chunk weave size 4
		weave_size = int.from_bytes(arfile.read(4), 'little')
		# Read tx index	4
		tx_index = int.from_bytes(arfile.read(4), 'little')

		chunk = Chunk(choff, tx_index)
		chunks.append(chunk)

	for i,chunk in enumerate(chunks):
		wtd = chunk.offset + (chunk.tx_index - 0x40000)
		print('[*] Decoding chunk {} at offset {} ....'.format(i, hex(wtd)))

		arfile.seek(wtd)
		decode_chunk(arfile.read(0x40000), i)

if __name__ == '__main__':
    parse(sys.argv[1])
