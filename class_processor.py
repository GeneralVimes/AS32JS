import json
import os
# open as3 class
# taking out the info of its ancestor, methods and fields
# save json
current_classname = ""

def strip_prog_token(nm):
	var_names_sms="qwertyuiopasdfghjklzxcvbnm0123456789QWERTYUIOPASDFGHJKLZXCVBNM_";
	res=""
	for ch in nm:
		if ch in var_names_sms:
			res+=ch;
		else:
			break;
	return res;

def has_class_method(ln_ar):
	res=False
	if len(ln_ar)>=3:
		if ln_ar[0] in ["private","protected","public"] and ln_ar[1]=="function":
			res=True
	return res;
	
def has_class_field(ln_ar):
	res=False
	if len(ln_ar)>=3:
		if ln_ar[0] in ["private","protected","public"] and ln_ar[1]=="var":
			res=True
	return res;

def run_interface_check(ln_ar):
	res=False
	if len(ln_ar)>=3:
		if ln_ar[0]=="public" and ln_ar[1]=="interface":
			res=True
	return res;
	
def has_class_name(ln_ar):
	res=False
	if len(ln_ar)>=3:
		if ln_ar[0]=="public" and ln_ar[1]=="class":
			res=True
	return res;

def add_vars_and_functions_from_parent(class_parent,list_vars,list_functions):
	data = None
	try:
		f = open('temp/jsons/'+class_parent+'.json')
		data = json.load(f)
		f.close() 
	except:
		print("PARENT JSON NOT FOUND:",class_parent)
	# print("data:",data)
	if data:		
		for x in data["fields"]:
			if x not in list_vars:
				list_vars.append(x)
		for x in data["methods"]:
			if x not in list_functions:
				list_functions.append(x)


def process_class(clnm, file=None):
	global current_classname
	current_classname = clnm
	if not file:
		file = "temp/as3files/"+current_classname+".as"
	f = open(file)
	lines = f.readlines()
	f.close();

	split_lns=[]
	for ln in lines:
		split_lns.append(
			ln.replace("("," ( ")
				.replace("{"," { ")
				.replace(")"," ) ")
				.replace("}"," } ")
				.replace("["," [ ")
				.replace("]"," ] ")
				.split()
		)
	# print(split_lns);
	class_parent=""
	list_vars=[]
	list_functions=[]

	is_interface=False
	# 1. looking for public class and extends
	for ln_ar in split_lns:
		is_interface = is_interface or run_interface_check(ln_ar)

		if has_class_name(ln_ar):
			try:
				id=ln_ar.index("extends")
				class_parent=ln_ar[id+1]
				break
			except:
				pass
	# 2. looking for [private/public/protected] var 
	# 3. looking for [private/public/protected] function 
	for ln_ar in split_lns:
		if has_class_field(ln_ar):
			list_vars.append(strip_prog_token(ln_ar[2]))
		if has_class_method(ln_ar):
			func_name = strip_prog_token(ln_ar[2])
			if func_name=="set" or func_name=="get":
				func_name = strip_prog_token(ln_ar[3])
				list_vars.append(func_name)
			else:
				if func_name!=current_classname:#class name not included as a method
					list_functions.append(func_name)
	# 4. looking for ancestor's json and adding its firelds and methods, too
	# 5. warning if it is not found
	if class_parent!="":
		add_vars_and_functions_from_parent(class_parent,list_vars,list_functions)
	# 6. generating json 
	ob={"class_name":current_classname, "parent":class_parent, "fields":list_vars, "methods":list_functions}
	if is_interface:
		ob["is_interface"]=is_interface
	with open('temp/jsons/'+current_classname+'.json', "w") as write_file:
		json.dump(ob, write_file,indent=4, sort_keys=True, ensure_ascii=False)
		write_file.close();
	


# process_class("World")
# process_class("IdleWorld")
# process_class("FarmWorld")
# process_class("BasicGameObject")

def recursively_work_directory(dir_path):
	for fl in os.listdir(dir_path):
		# print(fl)
		fl2 = os.path.join(dir_path, fl)
		if os.path.isfile(fl2):
			# print(fl)
			# pass
			nm = os.path.basename(os.path.normpath(fl))
			id = nm.find(".as")
			if id!=-1:
				print(nm[0:id])
				process_class(nm[0:id], fl2)
		else:
			recursively_work_directory(fl2)

# run several times to get list of methods of parents' parents' parents'
orig_dir = "source_as3"
recursively_work_directory(orig_dir)
