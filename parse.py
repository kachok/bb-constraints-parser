f = open("sectionmatrix.csv", "rU")

count = 0

ts =[]
t_oids=[]

sections = {}
templates={}

templates_constraints=[]

for line in f:
	line=line.strip()

	#list of templates
	if count == 4:
		ts = line.split(",")[1:]

	#list of templates oids
	if count == 6:
		t_oids = line.split(",")[1:]

		#compile list of templates
		for i, item in enumerate(ts):
			templates[item]=t_oids[i]


	#sections constraints
	if count >6:
		section = line.split(",")[0]
		oid = section.split("(")[1].split(")")[0]
		section  = section.split("(")[0]

		sections[section]=oid

		constraints = line.split(",")[1:]

		#extract all constraints into separata list
		for i, item in enumerate(constraints):
			if len(item)>0:
				#print item, templates[i], section
				print item, ts[i], section
				templates_constraints.append([item, ts[i], section])


	#print line.strip()
	count=count+1

#print ts
#print t_oids

print "\n"
print templates
print sections



f2 = open("clinicalstatementmatrix.csv", "rU")
count = 0

ts =[]
t_oids=[]

sections = {}
templates={}

statements = {}

sections_constraints=[]


print "======"

count=0
for line in f2:
	#list of templates
	if count == 4:
		ts = line.strip().split(",")[1:]
	#list of templates oids
	if count == 6:
		t_oids = line.strip().split(",")[1:]

	#clinical statements constraints
	if count >6:
		statement = line.strip().split(",")[0]
		oid = statement.split("(")[1].split(")")[0]
		statement  = statement.split("(")[0]

		statements[statement]=oid

		constraints = line.split(",")[1:]

		#print constraints

		#extract all constraints into separata list
		for i, item in enumerate(constraints):
			if len(item.strip())>0:
				item=item.strip()
				#print item, templates[i], section
				print ">>> ",item, ts[i], statement
				sections_constraints.append([item, ts[i], statement])


	#print line.strip()
	count=count+1

print "\n"
print statements

#print len(statements)

print "\n"
print templates_constraints
print "\n"
print sections_constraints

tc={}

for item in templates_constraints:
	c, template, section = item
	const = c.split(" ")[0]
	if const == "O": const = "may"
	if const == "R": const = "shall"
	if const == "R2": const = "should"
	num = c.split(":")[1][:-1]
	print const, num, template, section

	if template not in tc.keys():
		tc[template]={}

	if const not in tc[template].keys():
		tc[template][const]={}

	tc[template][const][section]=num

	if "full" not in tc[template].keys():
		tc[template]["full"]={}

	tc[template]["full"][section]={"constraint":const,"id":num}
	



sc={}
for item in sections_constraints:
	#print item
	c, section, statement = item
	const = c.split(" ")[0]
	if const == "O": const = "may"
	if const == "R": const = "shall"
	if const == "R2": const = "should"
	if len(c.split(":"))==2:
		num = c.split(":")[1][:-1]
		num2=""
	else:
		num= c.split(":")[1].split("CONF")[0]
		num2= c.split(":")[2][:-1]
	print const, num, num2, section, statement

	if section not in sc.keys():
		sc[section]={}

	if const not in sc[section].keys():
		sc[section][const]={}

	if num2=="": sc[section][const][statement]=[num]
	else: sc[section][const][statement]=[num, num2]

	if "full" not in sc[section].keys():
		sc[section]["full"]={}

	if num2=="": sc[section]["full"][statement]={"constraint":const,"id":[num]}
	else: sc[section]["full"][statement]={"constraint":const,"id":[num, num2]}




print "\n"
print tc
print "\n"
print sc
