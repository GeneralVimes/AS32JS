import json
import os

def remove_types(str):
	type_names_sms="qwertyuiopasdfghjklzxcvbnm0123456789QWERTYUIOPASDFGHJKLZXCVBNM.<>*"#var obs:Vector.<Object>

	"""
	where should we remove AS3 types 
	var varname: vartype
	between function and {

	"""
	id = str.find("function");
	if id!=-1:
		pass

def remove_types_from_lines(lns):
	res=[];
	type_names_sms="qwertyuiopasdfghjklzxcvbnm0123456789QWERTYUIOPASDFGHJKLZXCVBNM_.<>*"#var obs:Vector.<Object>
	var_names_sms="qwertyuiopasdfghjklzxcvbnm0123456789QWERTYUIOPASDFGHJKLZXCVBNM_"# 
	constructed_token="";
	prev_token="";
	prev_prev_token="";
	prev_prev_prev_token="";
	must_skip=False;
	can_skip=False;	
	rule_token=""
	pre_rule_token="" 
	stored_skipped_text=""
	logic_smbs="!|&*=/%,"
	logic_smbs_pre="=+-/"

	prev_ch=""
	are_inside_multiline_comment=False
	for ln in lns:
		# print("ln:",[ln])
		# ln = ln.replace(": ")
		res_ln = "";
		for ch in ln:
			if not are_inside_multiline_comment:
				if ch=="*" and prev_ch=="/":
					are_inside_multiline_comment=True
			else:
				if ch=="/" and prev_ch=="*":
					are_inside_multiline_comment=False

			if ch in var_names_sms:
				constructed_token+=ch
			else:
				if not can_skip:	
					if constructed_token=="function"  or constructed_token=="catch"  or constructed_token=="var":
						can_skip=True
						rule_token=constructed_token
						pre_rule_token=prev_token
				else:
					if (rule_token=="function" or rule_token=="catch") and ch=="{":
						can_skip=False;
				if constructed_token!="":
					prev_prev_prev_token=prev_prev_token
					prev_prev_token=prev_token
					prev_token=constructed_token
					constructed_token=""
					# print("constructed_token=",constructed_token, "prev_token=",prev_token, "prev_prev_token=",prev_prev_token)
				
			if can_skip:
				if not must_skip:
					if ch==":":
						must_skip=True
						stored_skipped_text=""
					else:
						
						if rule_token=="var" and ch not in "	 " and ch not in var_names_sms:
							can_skip=False
							must_skip=False
							if not stored_skipped_text=="" and not are_inside_multiline_comment:
								res_ln+="/*"+stored_skipped_text+"*/"
							stored_skipped_text=""
				else:
					if (ch not in type_names_sms) and (prev_ch in type_names_sms):
						must_skip=False;
						if rule_token=="var":
							can_skip=False; 
						# if pre_rule_token in ["private","public","ptotected"]:
						if not stored_skipped_text=="" and not are_inside_multiline_comment:
							res_ln+="/*"+stored_skipped_text+"*/"
						stored_skipped_text=""
			else:
				must_skip=False
				if not stored_skipped_text=="" and not are_inside_multiline_comment:
					res_ln+="/*"+stored_skipped_text+"*/"
				stored_skipped_text=""				

			if not must_skip:
				if prev_ch in logic_smbs and ch in var_names_sms:# to separate =new
					res_ln+=" "
				if prev_ch in var_names_sms and ch in logic_smbs_pre:# to separate =new
					res_ln+=" "
				res_ln+=ch
			else:
				stored_skipped_text+=ch
			
			prev_ch = ch;
		# print("res_ln:",[res_ln])
		res.append(res_ln);
	return res;
					
				
	

def prepare_as3_file(nm, dir_name=""):
	if dir_name=="":
		dir_name = "temp/as3files"
	f = open(dir_name+"/"+nm+".as")
	lines = f.readlines()
	f.close();
	res_lines=remove_types_from_lines(lines)

	res_lines=add_this_to_lines(res_lines)

	res_lines = second_pass(res_lines)
	
	dir_js = dir_name.replace("as3files","jss");
	try:
		os.makedirs(dir_js)
	except Exception as e:
		# print("ERROR", e)
		pass
	with open(dir_js+"/"+nm+'.js', "w") as write_file:
		write_file.writelines(res_lines);
		write_file.close();

def extract_front_whitespace(str):
	ws = "	 "#tab and space
	res=""
	for ch in str:
		if ch in ws:
			res+=ch
		else:
			break;
	return res;

def is_classname_interface(nm):
	res=False
	try:
		f = open('temp/jsons/'+nm+'.json')
		data = json.load(f)
		f.close() 
		if data["is_interface"]:
			res=True		
	except:
		pass#print("CHECKED INTERFACE NOT FOUND:",nm)
	# print("data:",data)		

	return res	

# replacing trace with console.log()
def perform_flash2js_replacements(ln_ar):
	for id in range(len(ln_ar)):
		if ln_ar[id]=="trace":
			ln_ar[id]="console.log"
		if ln_ar[id]=="getTimer":
			ln_ar[id]="Date.now"
		if ln_ar[id].endswith(".getStackTrace"):
			ln_ar[id]=ln_ar[id][0:-13]+"toString"
		if ln_ar[id].startswith("flash.ui.Keyboard."):
			ln_ar[id]="FlashKbrd."+ln_ar[id][18:]
		if ln_ar[id].endswith(".keyCode"):
			ln_ar[id] = ln_ar[id][0:-7]+"code"
		if ln_ar[id].endswith(".texture"):
			ln_ar[id] = ln_ar[id][0:-7]+"startlingTexture"
		if ln_ar[id].find("Rectangle")==0:
			ln_ar[id]="Phaser.Geom."+ln_ar[id]
		if ln_ar[id].find("Point")==0:
			ln_ar[id]="Phaser.Geom."+ln_ar[id]
		if ln_ar[id].endswith(".removeAt"):
			last_closing_paren_id=-1
			num_opened_parens=0;
			for id2 in range(id+1, len(ln_ar)):
				if ln_ar[id2]=="(":
					num_opened_parens+=1;
				if ln_ar[id2]==")":
					num_opened_parens-=1;
					if num_opened_parens==0:
						last_closing_paren_id=id2
						break
			if num_opened_parens!=-1:
				ln_ar[id]=ln_ar[id][0:-9]+".splice"
				ln_ar[last_closing_paren_id]=", 1)"
		if ln_ar[id]=="is":
			is_checking_interface = False
			if id>0 and id<len(ln_ar)-1:
				if is_classname_interface(ln_ar[id+1]):
					is_checking_interface=True
			if not is_checking_interface:
				ln_ar[id]="instanceof"
			else:
				ln_ar[id-1]+=".implements"
				ln_ar[id]="&&"
				ln_ar[id+1]=ln_ar[id-1]+".indexOf(\""+ln_ar[id+1]+"\")!=-1"
		if ln_ar[id]=="as":
			if id+1<len(ln_ar):
				ln_ar[id]="/*"+ln_ar[id]
				as_type_name = strip_prog_token(ln_ar[id+1])
				ln_ar[id+1]=ln_ar[id+1][0:len(as_type_name)]+"*/"+ln_ar[id+1][len(as_type_name):]
		if ln_ar[id]=="new":#replacing new Vector.<>() with []
			if id+1<len(ln_ar):
				if (ln_ar[id+1].find("Vector")==0) or (ln_ar[id+1].find("Dictionary")==0):
					if (ln_ar[id+1].find("Vector")==0):
						smbs_to_replace="[]"
					else:
						smbs_to_replace="{}"
					closing_paren_id=id+1
					for id2 in range(id+1,len(ln_ar)):
						if ln_ar[id2].find(")")!=-1:
							closing_paren_id=id2
							break
					ln_ar[id]=smbs_to_replace+"/*"+ln_ar[id]
					ln_ar[closing_paren_id]=ln_ar[closing_paren_id]+"*/" #we will keep the vector to see what should be inside
					# for id2 in range(id+1,closing_paren_id+1):
					# 	ln_ar[id2]=""
					


def strip_prog_token(nm):
	var_names_sms="qwertyuiopasdfghjklzxcvbnm0123456789QWERTYUIOPASDFGHJKLZXCVBNM_";
	res=""
	for ch in nm:
		if ch in var_names_sms:
			res+=ch;
		else:
			break;
	return res;

def find_first_meaningful_word(str):
	if str.startswith("."):
		return "",0
	prev_len=0
	tk=""
	is_building_tk = False
	i=0
	while i<len(str):
		ch = str[i]
		if is_building_tk:
			if ch.isalnum() or ch=="_":
				tk+=ch
			else:
				break
		else:
			if ch.isalnum() or ch=="_":
				is_building_tk=True
				tk+=ch
			else:
				prev_len+=1
		i+=1
	return tk,prev_len
				

def add_this_to_linesar(ln_ar, list_of_var, list_of_funcs, list_of_static,class_name,must_start_after_closing_paren=False):
	first_id_2_start=0;
	if must_start_after_closing_paren:
		for first_id_2_start in range(len(ln_ar)):
			if ")" in ln_ar[first_id_2_start]:
				break;
	for lin_id in range(first_id_2_start, len(ln_ar)):
		str = ln_ar[lin_id]
		tk,pref_len = find_first_meaningful_word(str)
		# tk = strip_prog_token(str)
		if tk in list_of_funcs or tk in list_of_var:
			must_add = True
			
			if lin_id<len(ln_ar)-1:
				if ln_ar[lin_id+1].startswith(":"):
					must_add=False
					if lin_id>0:
						if "?" in ln_ar[lin_id-1]:
							must_add=True #if it's a part of ternary
			
			if must_add:
				ln_ar[lin_id] = ln_ar[lin_id][0:pref_len]+"this."+ln_ar[lin_id][pref_len:]
		else:
			if tk in list_of_static:
				ln_ar[lin_id] = class_name+"."+ln_ar[lin_id]
	return " ".join(ln_ar);

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

def add_this_to_lines(lns):
	list_of_var=[];
	list_of_static=[];
	list_of_funcs=[];
	pre_spaces=[];
	split_lns=[]
	lines_with_functions_declarations=[];
	lines_with_static_declarations=[];
	lines_with_imports=[];

	line_id_with_classname=0;
	line_id_with_constructor=0;

	for ln in lns:
		pre_spaces.append(extract_front_whitespace(ln));
		split_lns.append(
				ln.replace("("," ( ")
					.replace("{"," { ")
					.replace(")"," ) ")
					.replace("}"," } ")
					.replace("[ Inline ]","")#not [Inline] as at thic moment there are spaces: [ Inline  ]
					.replace("["," [ ")
					.replace("]"," ] ")
					.replace("Main.self.","window.main.")
					.replace("TimerEvent.TIMER_COMPLETE","\"timerComplete\"")
					.replace("TimerEvent.TIMER","\"timer\"")
					.split()
					
			);
	
	class_name=""
	parent_class=""
	
	lin_id=0;
	for ln_ar in split_lns:
		if len(ln_ar)>0:
			if ln_ar[0]=="import":
				lines_with_imports.append(lin_id);

		if class_name=="":
			if len(ln_ar)>=3:
				if (ln_ar[1]=="class"):
					class_name=ln_ar[2]
					line_id_with_classname = lin_id
					try:
						id=ln_ar.index("extends")
						parent_class=ln_ar[id+1]
					except:
						pass
					ln_ar.pop(0);#removing word "public"
					try:
						id=ln_ar.index("implements")
						ln_ar[id]="//"+ln_ar[id]
					except:
						pass
		# print("ln_ar=",ln_ar)
		try:
			fid = ln_ar.index("var")
			if fid==1:
				if ln_ar[0] in ["private","protected","public"]:
					list_of_var.append(strip_prog_token(ln_ar[2]))
					ln_ar.pop(0)
					ln_ar.pop(0)
					ln_ar[0]="this."+ln_ar[0]
			if fid==2:
				if ln_ar[0] in ["private","protected","public","static"]:
					if ln_ar[1] in ["private","protected","public","static"]:
						list_of_static.append(strip_prog_token(ln_ar[3]))
						ln_ar.pop(0)
						ln_ar.pop(0)
						ln_ar[0]="static"
						lines_with_static_declarations.append(lin_id)
		except:
			pass
		
		try:
			fid = ln_ar.index("function")
			match fid:
				case 1:
					if ln_ar[0] in ["private","protected","public"]:
						func_name = strip_prog_token(ln_ar[2])
						if func_name=="get" or func_name=="set":
							func_name = strip_prog_token(ln_ar[3])
							list_of_var.append(func_name)
						else:
							if func_name!=class_name:
								list_of_funcs.append(func_name)
						ln_ar.pop(0)
						ln_ar.pop(0)
						lines_with_functions_declarations.append(lin_id)
						if func_name==class_name:
							ln_ar[0] = "constructor"
							line_id_with_constructor=lin_id;
							
				case 2:
					if ln_ar[0] in ["private","protected","public","override"]and ln_ar[1] in ["private","protected","public","override"]:
						list_of_funcs.append(strip_prog_token(ln_ar[3]))
						ln_ar.pop(0)
						ln_ar.pop(0)
						ln_ar.pop(0)
						lines_with_functions_declarations.append(lin_id)
					else:
						if ln_ar[0] in ["private","protected","public","static"]and ln_ar[1] in ["private","protected","public","static"]:
							list_of_static.append(strip_prog_token(ln_ar[3]))
							ln_ar.pop(0)
							ln_ar.pop(0)
							ln_ar[0]="static"
							lines_with_static_declarations.append(lin_id)
		except:
			pass
		lin_id+=1;

	# print("list_of_var:",list_of_var)
	# print("list_of_funcs:",list_of_funcs)
	# print(split_lns)
	if parent_class!="":
		add_vars_and_functions_from_parent(parent_class,list_of_var,list_of_funcs)

	res_lns=[];
	# print("line_id_with_classname",split_lns[line_id_with_classname])
	for lin_id in range(len(split_lns)):
		if lin_id not in lines_with_imports and lin_id>=line_id_with_classname:
			ln_ar = split_lns[lin_id];

			perform_flash2js_replacements(ln_ar)

			if lin_id not in lines_with_static_declarations:
				if lin_id not in lines_with_functions_declarations:
					must_start_after_closing_paren=False
				else:
					must_start_after_closing_paren=True
				str_add = add_this_to_linesar(ln_ar, list_of_var, list_of_funcs, list_of_static,class_name,must_start_after_closing_paren)
			else:
				str_add = " ".join(ln_ar)
			str_add = str_add.replace(" (","(").replace(" )",")").replace(" {","{").replace(" }","}").replace(" [","[").replace(" ]","]").replace("( ","(").replace(") ",")").replace("{ ","{").replace("} ","}").replace("[ ","[").replace("] ","]")
			res_lns.append(pre_spaces[lin_id]+str_add+"\n")

	return res_lns, list_of_funcs

def find_next_word(ln, start_id):
	res=""
	is_in_word=False
	for chid in range(start_id, len(ln)):
		ch = ln[chid]
		if ch.isalnum() or ch=="_":
			is_in_word=True
			res+=ch
		else:
			if is_in_word:
				break;
	return res

def find_implemented_interfaces(ln):
	res=[]
	id = ln.find("implements")
	if id!=-1:
		intrf = find_next_word(ln, id+len("implements"))
		if intrf!="":
			res.append(intrf)
	return res

def second_pass(lns):
	# print(lns)
	constructor_id=-1;
	constructor_opening_curl_id=-1;
	first_this_id=-1;
	last_closing_curl_id=-1;
	ln_id=0;
	for ln_id in range(len(lns)):
		ln = lns[ln_id]
		if first_this_id==-1:			
			if ln.find("this.")!=-1:
				first_this_id=ln_id;
		if ln.find("constructor")!=-1:
			constructor_id=ln_id
		if constructor_id!=-1:
			if ln.find("{")!=-1:
				constructor_opening_curl_id=ln_id
				break;
	# finding last {
	for ln_id in range(len(lns)-1, 0, -1):
		if ln.find("}")!=-1:
			last_closing_curl_id=ln_id
			break;
	
	#removing initial tabs
	for ln_id in range(len(lns)):
		ln = lns[ln_id]
		if not (first_this_id<=ln_id<constructor_id):
			if ln[0]=="	":
				lns[ln_id]=ln[1:]
			else:
				if ln[0:4]=="    ":
					lns[ln_id]=ln[4:]
	
	# swapping parts
	if constructor_id!=-1 and first_this_id!=-1:
		res = lns[0:first_this_id]+lns[constructor_id:constructor_opening_curl_id+1]+lns[first_this_id:constructor_id]+lns[constructor_opening_curl_id+1:last_closing_curl_id]
		lns = res;
		new_constructor_open_curl_id = first_this_id+constructor_opening_curl_id-constructor_id
	else:
		new_constructor_open_curl_id=constructor_opening_curl_id
	# checking if super(is called right after the constructor)	
	# print(lns)
	first_this_id=0
	super_id = -1
	extends_id = -1
	for ln_id in range(len(lns)):
		ln = lns[ln_id]
		if ln.find("extends")!=-1:
				extends_id=ln_id
		if ln.find("super(")!=-1:
				super_id=ln_id
				break;
	# print(lns[0],first_this_id,constructor_id,constructor_opening_curl_id,new_constructor_open_curl_id,super_id)
	if super_id!=-1:
		lns = lns[0:new_constructor_open_curl_id+1]+[lns[super_id]]+lns[new_constructor_open_curl_id+1:super_id]+lns[super_id+1:]
	else:
		if extends_id!=-1:
			lns = lns[0:new_constructor_open_curl_id+1]+["		super()\n"]+lns[new_constructor_open_curl_id+1:]
	# print(lns)
		
	#removing initial tab it it was left
	if lns[0].startswith("	"):
		lns[0]=lns[0][1:]

	# removing last } if it is not needed
	last_closing_curl_id=-1
	last_num_of_closing_curl_id=-1
	level=0
	for ln_id in range(len(lns)):
		ln = lns[ln_id]
		count_close_curl = ln.count("}")
		count_open_curl = ln.count("{")
		level+=count_open_curl-count_close_curl
		if count_close_curl>0:
			last_closing_curl_id=ln_id
			last_num_of_closing_curl_id=count_close_curl

	if level==-1:
		if last_num_of_closing_curl_id==1:
			lns=lns[0:last_closing_curl_id]
	
	#adding implements
	if lns[0].find("implements")!=-1:
		implemented_interfaces=find_implemented_interfaces(lns[0])
		if len(implemented_interfaces)>0:
			added_implements = ["		if (!this.implements){this.implements=[]}\n",
								'		this.implements.push("'+implemented_interfaces[0]+'")\n',
								"		\n"]
			possible_super_line_id = new_constructor_open_curl_id+1
			possible_super_line = lns[possible_super_line_id]
			if possible_super_line.find("super")!=-1:
				# adding implements after super
				lns=lns[0:possible_super_line_id+1]+added_implements+lns[possible_super_line_id+1:]
			else:
				lns=lns[0:possible_super_line_id]+added_implements+lns[possible_super_line_id:]

	return lns

lines_for_index=[]

def recursively_work_directory(dir_path):
	global lines_for_index
	for fl in os.listdir(dir_path):
		# print(fl)
		fl2 = os.path.join(dir_path, fl)
		if os.path.isfile(fl2):
			# print(fl)
			# pass
			nm = os.path.basename(os.path.normpath(fl))
			id = nm.find(".as")
			if id!=-1:
				# print(nm[0:id])
				lines_for_index.append("<script src=\"src/conversions/"+dir_path+"/"+nm[0:id]+".js\"></script>"+"\n")
				prepare_as3_file(nm[0:id], dir_path)
		else:
			recursively_work_directory(fl2)

def recursively_find_path_to_as3file(fnm, dir_path):
	res=None
	for fl in os.listdir(dir_path):
		fl2 = os.path.join(dir_path, fl)
		if os.path.isfile(fl2):
			nm = os.path.basename(os.path.normpath(fl))
			id = nm.find(".as")
			if id!=-1:
				if nm[0:id]==fnm:
					res=dir_path
					break
		else:
			res = res or recursively_find_path_to_as3file(fnm, fl2)
	return res;
			

def prepare_file_from_tree(fnm, dir_path):
	path = recursively_find_path_to_as3file(fnm, dir_path)
	prepare_as3_file(fnm, path)

