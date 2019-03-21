#!/bin/python2
# Craft, Artisanal, Bespoke, Organic pentest script generator

import sys,os,argparse,ast
testlist="./testlist"
servicearrayfile="./services.array"
modulepath=str(os.path.dirname(os.path.realpath(__file__)))+"/modules/"
queuefile="CABO.sh"
mkdirqueue=[]
cmdqueue=[]

def parsefile(infile):
	with open(infile) as f:
		return ast.literal_eval(f.read())

servicearray = parsefile(servicearrayfile)

for service in servicearray:
	tests=""
		
	try:
		tests=parsefile(modulepath+service)
		print("[+] Found tests for "+service)
	
	
	except:
		pass

	for test in tests:
		print("   [*] Adding "+test+" to the queue")
		testlist=tests[test]
		testtype=testlist[0]
		outputfolder=testlist[1]
		testcommand=testlist[2]
		testprotocol=testlist[3]
		

		mkdirqueue.append("mkdir "+outputfolder)	
		for host in servicearray[service][testprotocol]:
			if service == "plainhttp":
				proto="http"
			elif service == "securehttp":
				proto="https"
			else:
				proto=""
			hostip=host.split(":")[0]
			hostport=host.split(":")[1]
			
			towriteout=str(testcommand)
			towriteout=towriteout.replace("DIR", outputfolder)
			towriteout=towriteout.replace("HOST", host)
			towriteout=towriteout.replace("IP", hostip)
			towriteout=towriteout.replace("PORT", hostport)
			towriteout=towriteout.replace("PROTO", proto)
			cmdqueue.append(towriteout)


with open(queuefile, "w") as f:
	f.write("#!/bin/parallel --shebang\n")
	for line in mkdirqueue:
		f.write(line+"\n")
	for line in cmdqueue:
		f.write(line+"\n")

