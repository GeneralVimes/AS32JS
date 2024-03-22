import os
# converting functions like this
	# func1(a/*int*/, b/*String*/){
"""
into JSDoc format
	/**
	 * 
	 * @param {int} a 
	 * @param {String} b 
	 */
	func1(a/*int*/, b/*String*/){

"""	

def convert_arg_to_jsdoc(arg):
	id1 = arg.find("/*");
	id2 = arg.find("*/");
	if id1!=-1:
		part1 = arg[0:id1].strip()
		part2 = arg[id1+2:id2].strip()
	else:
		part1 = arg.strip()
		part2="*"
	if part2.startswith(":"):
		part2 = part2[1:]
	return "@param {"+part2+"} "+part1;

def strip_old_jsdoc_comments(ln):
	ar = ln.split("/*")
	res_ar_id=-1
	res_smb_id=-1
	for id in range(len(ar)):
		if res_ar_id!=-1:
			break
		sub_ln = ar[id]
		close_id = sub_ln.find("*/")
		for i in range(close_id+2,len(sub_ln)):
			if sub_ln[i].isalpha():
				res_ar_id = id		
				res_smb_id = i		
				break
	id2cut = res_smb_id
	for id in range(len(ar)):
		if id<res_ar_id:
			id2cut+=len(ar[id])+2
	# print("id2cut=",id2cut)
	return remove_old_comment_from(ln[0:id2cut])+ln[id2cut:]

def find_last_enter_before_name(ln):
	res=-1
	for id in range(len(ln)):
		ch = ln[id]
		if ch=="\n":
			res=id
		if ch not in " 	\n":
			break;
	# print("res=",res)
	return res;

def find_last_enter_backwards(ln, id0):
	res=id0
	for id in range(id0,0,-1):
		if ln[id]=="\n":
			res=id
			break;
	return res;

def remove_old_comment_from(ln):
	id0 = ln.find("/*")
	if id0!=-1:
		id1 = ln.find("*/",id0)
		if id1!=-1:
			mid_part = ln[id0:id1+2]
			if mid_part.find("\n")!=-1:
				mid_part=""
			return ln[0:id0]+mid_part+remove_old_comment_from(ln[id1+2:])
		else:
			return ln
	else:
		return ln

def add_jsdoc_comment(ln):
	ln = strip_old_jsdoc_comments(ln)
	
	res=""
	
	id0 = find_last_enter_before_name(ln)
	# print(ln,id0)
	if id0!=-1:
		white_part = ln[0:id0+1]
		smb_part = ln[id0+1:]
	else:
		white_part=""
		smb_part=ln
	# print([white_part, smb_part])
	# res=white_part
	id1 = smb_part.find("(")
	id2 = smb_part.find(")")
	args_str = smb_part[id1+1:id2]
	
	args_ar = args_str.strip().split(",")
	res="\n	/**\n"
	res+="	 * \n"
	if len(args_ar)>0:
		for arg in args_ar:
			if arg.strip()!="":
				res+="	 * "+convert_arg_to_jsdoc(arg)+"\n"
	res+="	 */\n"
	return res+smb_part;

def comment_js_file(nm,nm2=None):
	if nm2==None:
		nm2=nm;
	
	f = open(nm);
	lines = f.readlines()
	f.close()
	s=("").join(lines)
	level=0
	res=""
	buffer=""
	prev_ch=""

	constr_id = s.find("constructor")
	enter_id = find_last_enter_backwards(s,constr_id)
	res=s[0:enter_id+1]
	res=remove_old_comment_from(res).strip()
	s=s[enter_id+1:]
	level=1
	prev_ch=res[-1] if len(res)>0 else ""
	ignore_comment_block=False
	ignore_comment_line=False
	for ch in s:
		# print("ignore_braces=",ignore_braces, ch, prev_ch)
		if ch=="{":
			if not (ignore_comment_block or ignore_comment_line):
				level+=1
				if level==1:
					buffer=""
				if level==2:
					res+=add_jsdoc_comment(buffer)
				res+=ch;
			else:
				if level==1:
					buffer+=ch
				else:
					res+=ch
		elif ch=="}":
			if not (ignore_comment_block or ignore_comment_line):
				res+=ch
				level-=1
				if level==1:
					buffer=""
			else:
				if level==1:
					buffer+=ch
				else:
					res+=ch				
		else:
			if ch=="*":
				if prev_ch=="/":
					if not ignore_comment_block and not ignore_comment_line:
						ignore_comment_block=True
			if ch=="/":
				if prev_ch=="*":
					if ignore_comment_block:
						ignore_comment_block=False
				if prev_ch=="/":
					if not ignore_comment_line and not ignore_comment_block:
						ignore_comment_line=True
			if ch=="\n":
				if ignore_comment_line:
					ignore_comment_line=False
			if level==1:
				buffer+=ch
			else:
				res+=ch
		prev_ch=ch
	f = open(nm2,"w");
	f.writelines([res]);
	f.close()



def process_folder(dir_path):
	for fl in os.listdir(dir_path):
			fl2 = os.path.join(dir_path, fl)
			if os.path.isfile(fl2):
				comment_js_file(fl2,fl2)
			else:
				process_folder(fl2)


# comment_js_file("temp/test2.js","temp/test2.js")
process_folder("src")