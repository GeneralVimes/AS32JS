import json
import os
from converter import remove_types_from_lines
from converter import add_this_to_lines
from converter import second_pass
from bind_adder import add_binds
from better_binder import better_binds
from images_width_fixer import fix_images_width

stored_comments_and_strings=[]
changed_files=[]
def cut_comments_and_strings(ln,dest_ar,only_strings=False):
	need1more=True
	res=""
	while need1more:
		lnlength=len(ln)
		opens=["/*","//","'",'"']
		closes=["*/","\n","'",'"']
		if only_strings:
			opens=["'",'"']
			closes=["'",'"']		
		ids=[]
		for op in opens:
			id = ln.find(op)
			if id==-1:
				id=lnlength		
			ids.append(id)
		mid = min(ids);
		# print(lnlength, ids)
		if mid<lnlength:
			mid_id = ids.index(mid)
			clos = closes[mid_id]
			id2 = ln.find(clos,mid+1)
			
			if clos=="'" or clos=='"':
				while id2!=-1 and ln[id2-1]=="\\":
					
					id2 = ln.find(clos,id2+1)
					
			
			# print([clos, id2, ln])
			if id2!=-1:
				if clos=="\n":
					id2-=1

				part1 = ln[0:mid]
				part2 = ln[mid:id2+len(clos)]
				part3 = ln[id2+len(clos):]

				comm_id = len(dest_ar)
				dest_ar.append(part2)
				placeholder = " _COMMSTRPLACEHOLDER_"+str(comm_id)+"_ "
				
				res+=part1+placeholder;
				ln = part3;
			else:
				res+=ln;
				need1more=False
		else:
			res+=ln;
			need1more=False
	return res;

def add_spaces_between_signs(ln):
	res=""
	prev_ch="\n"
	for ch in ln:
		if ch.isalnum() or ch=="_":
			if prev_ch in "=+*/:;?&|^%!()[]{}>":
				res+=" "
		if ch.isalpha() and prev_ch=="-":
			res+=" "
		if prev_ch=="-":
			if prev_ch.isalpha():
				res+=" "
		if ch in "=+*-/:?&|^%!()[]{}<":
			if prev_ch.isalnum() or prev_ch=="_":
				res+=" "
		res+=ch;
		prev_ch=ch
	return res;

def return_comments_and_strings(ln,dest_ar):
	res=""
	for id in range(len(dest_ar)):
		code="_COMMSTRPLACEHOLDER_"+str(id)+"_"
		found_id=ln.find(code)
		if found_id!=-1:
			
			delta_back = 0
			if ln[found_id-1]==" ":
				delta_back =1
			delta_forward = 0
			if ln[found_id+len(code)]==" ":
				delta_forward =1
			
			part1=ln[0:found_id-delta_back]
			part3=ln[found_id+len(code)+delta_forward:]
			res+=part1+dest_ar[id]
			ln=part3
	res+=ln
	return res;

def finish_lines_with_enters(lns):
	for id in range(len(lns)-1):
		lns[id] = lns[id]+"\n"

def process_file(nm, nm2=None):
	print("process_file",nm)
	if nm2==None:
		nm2=nm
	f = open(nm)
	lines = f.readlines()
	f.close()
	s = "".join(lines)
	stored_comments_and_strings.clear()
	s = cut_comments_and_strings(s,stored_comments_and_strings)
	s = add_spaces_between_signs(s);
	res_lines=s.split("\n")


	finish_lines_with_enters(res_lines)

	res_lines=remove_types_from_lines(res_lines)
	res_lines, list_of_funcs=add_this_to_lines(res_lines)
	res_lines = second_pass(res_lines)	
	s="".join(res_lines)
	s = s.replace(": ",":").replace(" :",":")
	s = better_binds(s,list_of_funcs)
	s=return_comments_and_strings(s,stored_comments_and_strings)
	s=s.replace(" /*","/*")
	s = fix_images_width(s)
	# s=s.replace("\n\n","\n").replace("  "," ")
	stored_comments_and_strings.clear()
	

	dir2 = nm2.replace("\\","/")
	ar_dir2 = dir2.split("/")
	file_name = ar_dir2[len(ar_dir2)-1]
	ar_dir2=ar_dir2[0:len(ar_dir2)-1]
	
	dir2 = "/".join(ar_dir2);

	try:
		os.makedirs(dir2)
	except Exception as e:
		# print("ERROR", e)
		pass

	try:
		f = open(nm2)
		old_lines=f.readlines()
		f.close()

		if "".join(old_lines)!=s:
			changed_files.append(file_name[0:-3])
			# print("CHANGED:",file_name[0:-3], changed_files)
	except Exception as e:
		pass

	f = open(nm2, "w")
	f.writelines([s])
	f.close()

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
				process_file(dir_path+"/"+nm[0:id]+".as", dir_path.replace(orig_dir,dest_dir)+"/"+nm[0:id]+".js")
		else:
			recursively_work_directory(fl2)

orig_dir = "source_as3"
dest_dir = "results_js"
changed_files.clear()
recursively_work_directory(orig_dir)
print("changed_files:",changed_files)