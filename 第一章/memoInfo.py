import psutil
class MemoInfo:
	def bytes2human(self, n):
		symbols = ('K','M','G','T','P','E','Z','Y')
		prefix = {}
		for index,symbol in enumerate(symbols):
			prefix[symbol] = 1 << (index+1)*10
		for symbol in reversed(symbols):
			if n >= prefix[symbol]:
				value = float(n) / prefix[symbol]
				return '%.1f%s' % (value,symbol)
		return '%sB' % n
	def pprint_ntuple(self,nt):
		for name in nt._fields:
			value = getattr(nt,name)
			if name != 'percent':
				value = self.bytes2human(value)
			print('%-10s: %7s'%(name.capitalize(),value))
	def main(self):
		print("MEMORY\n--------")
		self.pprint_ntuple(psutil.virtual_memory())
		print("\nSWAP\n--------")
		self.pprint_ntuple(psutil.swap_memory())

if __name__ == '__main__':
	MemoInfo().main()
