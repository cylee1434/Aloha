import random
import matplotlib.pyplot as plt

TSLOTS = 10000

class classNode:
	def __init__(self, ttl):
		self.ttl = ttl # slots left until retransmission
	def tick(self):
		self.ttl = self.ttl - 1


def main():
	random.seed()

	for N in [3, 100]:		
		Nlist = []
		selist = []
		print ("Window size: {0:2d}".format(N))

		for N in range(1, 101):
			snode = [classNode(random.randrange(0, N)) for _ in range(N) ]
			successful_slots = 0
			throughput = 0
	
			for slot in range(TSLOTS):
				transmitted_nodes = []
	
				for i in range(N):
					if not snode[i].ttl:
						transmitted_nodes.append(i)
						snode[i].ttl = random.randrange(0, N)
					else:
						snode[i].tick()
	
				if not transmitted_nodes:
					pass
	
				if (len(transmitted_nodes) == 1):
					successful_slots = successful_slots + 1
				
				if (len(transmitted_nodes) > 2):
					for j in transmitted_nodes:
						snode[j].ttl = random.randrange(0, N)
				
			throughput = (successful_slots/float(TSLOTS))
	
			print ("N = {0:2d}: {1:f}".format(N, throughput))
			
			Nlist.append(N)
			selist.append(throughput)
		
		plt.plot(Nlist, selist)
		print ("")

	plt.xlabel("Nodes")
	plt.ylabel("Throughput")
	plt.legend(['W = 3', 'W = 100'], loc='upper right')
	plt.axis([0, 100, 0, 1])
	plt.grid(linestyle='--')
	plt.show()

	return


if __name__ == "__main__":
	main()
