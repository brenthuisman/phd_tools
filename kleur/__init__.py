class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

def header(instr):
	return bcolors.HEADER + str(instr) + bcolors.ENDC
def blue(instr):
	return bcolors.OKBLUE + str(instr) + bcolors.ENDC
def green(instr):
	return bcolors.OKGREEN + str(instr) + bcolors.ENDC
def warning(instr):
	return bcolors.WARNING + str(instr) + bcolors.ENDC
def fail(instr):
	return bcolors.FAIL + str(instr) + bcolors.ENDC
def bold(instr):
	return bcolors.BOLD + str(instr) + bcolors.ENDC
def underline(instr):
	return bcolors.UNDERLINE + str(instr) + bcolors.ENDC

def strs(*args):
	outp=""
	for arg in args:
		outp+=str(arg)+" "
	return outp
