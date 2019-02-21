def main():

	for x in range(2**8):
		y = format(x,'08b')
		for t in range(8):
			print(y[t])


if __name__ == '__main__':
	main()