import os
import struct
from ACExplorer.misc import BaseTexture


class Texture(BaseTexture):
	def __init__(self, app, texture_file):
		BaseTexture.__init__(self, app)
		try:
			with open(os.path.join(app.CONFIG['dumpFolder'], 'fileTypes', 'A2B7E917'), 'a') as f2:
				f2.write('{}\n'.format('{:02X}'.format(ord(b)) for b in texture_file.read_str(130)))
		except Exception as e:
			app.log.warn(__name__, 'Failed to save header to fileTypes folder\n{}'.format(e))
		texture_file.seek(13)
		self.dwSize = b'\x7C\x00\x00\x00'  # 124
		DDSD_CAPS = DDSD_HEIGHT = DDSD_WIDTH = DDSD_PIXELFORMAT = True
		# (probably should be set based on the data)
		DDSD_PITCH = False
		DDSD_MIPMAPCOUNT = True
		DDSD_LINEARSIZE = True
		DDSD_DEPTH = False
		self.dwFlags = struct.pack('<i', (0x1*DDSD_CAPS)|(0x2*DDSD_HEIGHT)|(0x4*DDSD_WIDTH)|(0x8*DDSD_PITCH)|(0x1000*DDSD_PIXELFORMAT)|(0x20000*DDSD_MIPMAPCOUNT)|(0x80000*DDSD_LINEARSIZE)|(0x800000*DDSD_DEPTH))
		self.dwWidth = texture_file.read_str(4)
		self.dwHeight = texture_file.read_str(4)
		self.dwDepth = texture_file.read_str(4)
		self.imgDXT = texture_file.read_uint_32()
		texture_file.seek(8, 1)  # could be image format. Volume textures have first 4 \x03\x00\x00\x00 all else have \x01\x00\x00\x00
		# next 4 are \x01\x00\x00\x00 for diffuse maps and \x00\x00\x00\x00 for other things like volume textures and maps
		self.dwMipMapCount = texture_file.read_str(4)
		texture_file.seek(84, 1)  # 24 of other data followed by "CompiledTextureMap" which duplicates most of the data
		self.dwPitchOrLinearSize = texture_file.read_str(4)
		self.buffer = texture_file.read_str(struct.unpack('<I', self.dwPitchOrLinearSize)[0])
		self.dwReserved = b'\x00\x00\x00\x00'*11

		self.ddspf = ''  # (pixel format)
		self.ddspf += b'\x20\x00\x00\x00'  # dwSize
		if self.imgDXT in [0, 7]:  # dwFlags
			self.ddspf += b'\x40\x00\x00\x00'
		else:
			self.ddspf += b'\x04\x00\x00\x00'
		# if imgDXT in [0, 7]:
		# 	self.ddspf += 'DXT1'
		if self.imgDXT in [0, 1, 2, 3, 7]:  # dwFourCC
			self.ddspf += 'DXT1'
		elif self.imgDXT == 4:
			self.ddspf += 'DXT3'
		elif self.imgDXT in [5, 6]:
			self.ddspf += 'DXT5'
		elif self.imgDXT in [8, 9, 16]:
			self.ddspf += 'DX10'
		else:
			raise Exception('imgDXT: "{}" is not currently supported'.format(self.imgDXT))

		self.ddspf += b'\x00\x00\x00\x00' * 5  # dwRGBBitCount, dwRBitMask, dwGBitMask, dwBBitMask, dwABitMask
		if self.imgDXT == 8:
			self.DXT10Header = b'\x62\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00'
		else:
			self.DXT10Header = ''
		self.dwCaps = b'\x08\x10\x40\x00'
		self.dwCaps2 = b'\x00\x00\x00\x00'
		self.dwCaps3 = b'\x00\x00\x00\x00'
		self.dwCaps4 = b'\x00\x00\x00\x00'
		self.dwReserved2 = b'\x00\x00\x00\x00'


def export_texture(app, file_id):
	data = app.tempNewFiles.getData(file_id)
	if data is None:
		app.log.warn(__name__, "Failed to find file {:016X}".format(file_id))
		return
	texture_file = app.misc.file_object.FileObjectDataWrapper.from_binary(app, data["rawFile"])
	save_path = os.path.join(app.CONFIG['dumpFolder'], '{}.dds'.format(data['fileName']))
	if os.path.isfile(save_path):
		app.log.info(__name__, 'Texture "{}" already exported'.format(data['fileName']))
		return save_path
	tex = Texture(app, texture_file)
	tex.export_dds(save_path)
	app.log.info(__name__, 'Texture "{}" exported'.format(data['fileName']))
	return save_path