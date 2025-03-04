#!/usr/bin/python3

import curses, shutil
import socket, signal
import fcntl, ctypes
import struct
import binascii
from random import randint # Used for generating random source-port

def shortToBin(num):
	return struct.pack('!h', num)

def intToBin(num):
	return struct.pack('!b', num)

def checksum(data):
	## == UDP calculates checksums this way, TCP does it differently.
	c = 0
	for index, c_int in enumerate(data):
		if index & 1:
			c += int(c_int)
		else:
			c += int(c_int) << 8 # Bitshift 8bit to the left
	return c

def pack_Ethernet(src_mac, dst_mac, flags=b'\x08\x00'):
	if not type(src_mac) is bytes: src_mac = bytes(src_mac, 'UTF-8')
	if not type(dst_mac) is bytes: dst_mac = bytes(dst_mac, 'UTF-8')
	if not type(flags) is bytes: flags = bytes(flags, 'UTF-8')

	src_mac = src_mac.replace(b':', b'')
	dst_mac = dst_mac.replace(b':', b'')

	return struct.pack("!6s6s2s", *(src_mac, dst_mac, flags))

def pack_IP(src_addr=b'\x7f\x00\x00\x01', dst_addr=b'\x7f\x00\x00\x01',
				version_ihl=b'E',
				DSCP_ECN=b'\x00',
				total_length=b'\x00M',
				identification=b'i\x06',
				flags_offset=b'@\x00',
				ttl=b'@',
				protocol=b'\x11',
				header_checksum=b'\xd3\x97'):
	
	return struct.pack("!12s4s4s", *(version_ihl, DSCP_ECN, total_length,
									identification, flags_offset, ttl,
									protocol, header_checksum,
									src_addr, dst_addr))

def pack_UDP(payload, addr=b'127.0.0.1', port=5554):
	## == returns (<UDP_HEADERS+payload>, <checksum>)
	proto = socket.IPPROTO_UDP
	if type(payload) != bytes:
		payload = bytes(payload, 'UTF-8')
	if type(addr) != bytes:
		addr = bytes(addr, 'UTF-8')

	csum = 0
	csum += checksum(payload)
	csum += checksum(addr)
	csum += proto + len(payload)

	while csum >> 16:
		csum = (csum & 0xFFFF)+(csum >> 16)

	csum = ~csum
	csum = csum >> 8 # Could also be "sum & 0xFF" - not quite sure:
			# https://gist.github.com/fxlv/81209bbd150abfeaceb1f85ff076c9f3

	udp = struct.pack("!2s2s2s2s", *(intToBin(randint(3000, 6000)),
										intToBin(port),
										intToBin(len(message)),
										intToBin(csum)) )

	return udp + payload, int(binascii.hexlify(intToBin(csum)), 16)

def unpack_Ethernet(frame_slize): # frame[0:14]
	ethernet_segments = struct.unpack("!6s6s2s", frame_slize)
	mac_src, mac_dst = (binascii.hexlify(mac) for mac in ethernet_segments[:2])
	return {'source' : 
				b':'.join(mac_src[i:i+2] for i in range(0, len(mac_src), 2)),
			'destination' :
				b':'.join(mac_dst[i:i+2] for i in range(0, len(mac_dst), 2))}

def unpack_IP(frame_slize): # frame[14:34]
	## TODO: Actually parse the early header items.
	##       For instance it would be beneficial to get the protocol identifier
	ip_segments = struct.unpack("!12s4s4s", frame_slize)
	ip_source, ip_dest = (socket.inet_ntoa(ip) for ip in ip_segments[1:3])
	return {'source' : ip_source, 'destination' : ip_dest}

def unpack_UDP(frame_slize): # frame[34:42]
	udp_header = struct.unpack("!2s2s2s2s", frame_slize[:8])

	## == I do not like these row breaks, but trying to keep width of 80 :/
	udp_sourcePort, \
	udp_destPort, \
	udp_length, \
	udp_checksum = [int(binascii.hexlify(x), 16) for x in udp_header[:4]]

	data = frame_slize[8:8+udp_length]

	return {'source' : {'port' : udp_sourcePort},
			'destination' : {'port' : udp_destPort},
			'meta' : {'length' : udp_length, 'checksum' : udp_checksum},
			'payload' : data}

class ifreq(ctypes.Structure):
	## == This is a ctype structure that matches the
	##		requirements to set a socket in promisc mode.
	##		In all honesty don't know where i found the values :)
	_fields_ = [("ifr_ifrn", ctypes.c_char * 16),
				("ifr_flags", ctypes.c_short)]

class promiscuous():
	def __init__(self, s, interface=b'lo'):
		self.s = s
		self.interface = interface
		self.ifr = ifreq()

		self.IFF_PROMISC = 0x100
		self.SIOCGIFFLAGS = 0x8913
		self.SIOCSIFFLAGS = 0x8914

	def on(self):
		## -- Set up promisc mode:
		self.ifr.ifr_ifrn = self.interface

		fcntl.ioctl(self.s.fileno(), self.SIOCGIFFLAGS, self.ifr)
		self.ifr.ifr_flags |= self.IFF_PROMISC

		fcntl.ioctl(self.s.fileno(), self.SIOCSIFFLAGS, self.ifr)

	def off(self):
		## -- Turn promisc mode off:
		self.ifr.ifr_flags &= ~self.IFF_PROMISC
		fcntl.ioctl(self.s.fileno(), self.SIOCSIFFLAGS, self.ifr)

class rawstock():
	def __init__(self, ifname, promisc=True):

		if type(ifname) is not bytes:
			ifname = bytes(ifname, 'UTF-8')
		self.ifname = ifname

		# == socket.ntohs(0x0003) is black magic in the making.
		#		Normally you'd do:
		#		.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
		#		However socket.noths(0x0003) does the trick better.
		#		If someone can explain why, i'd be happy to know.

		self.sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW,
										socket.ntohs(0x0003))

		if promisc:
			self.promiscuousMode = promiscuous(self.sock, self.ifname) # self being socket()
			self.promiscuousMode.on()
		else:
			self.promiscuousMode = False

	def send(self, message, addr='127.0.0.1', port=5554):
		ethernet = pack_Ethernet(src_mac=b'00:00:00:00:00:00',
									dst_mac=b'00:00:00:00:00:00',
									flags=b'\x08\x00')

		ip = pack_IP(src_addr=b'\x7f\x00\x00\x01',
					 dst_addr=b'\x7f\x00\x00\x01',
						version_ihl=b'E',
						DSCP_ECN=b'\x00',
						total_length=b'\x00M',
						identification=b'i\x06',
						flags_offset=b'@\x00',
						ttl=b'@',
						protocol=b'\x11',
						header_checksum=b'\xd3\x97')

		udp, udp_checksum = pack_UDP(message, addr, port)

		## == Because I'm not the sharpest tool in the shed,
		##		I literally have no idea how to send data on
		##		our promisc socket, so we'll create a tmp one for now.
		tmp_sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
		tmp_sock.bind((self.ifname.decode('UTF-8'), 0))
		tmp_sock.send(ethernet + ip + udp)
		tmp_sock.close()

	def recv(self):
		frame, addr = self.sock.recvfrom(65565)

		parsed_frame = {}

		parsed_frame['ethernet'] = unpack_Ethernet(frame[0:14])
		parsed_frame['IP'] = unpack_IP(frame[14:34])
		if len(frame) >= 34: ## TODO: Replace and check IP protocol...
			parsed_frame['UDP'] = unpack_UDP(frame[34:]) # No end given because payload-len unknown

		return parsed_frame

	def close(self):
		self.promiscuousMode.off()
		self.sock.close()