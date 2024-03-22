def add_bind_to_func_in_objects(ln):
	res=""
	while True:
		func_id = ln.find("func:")
		if func_id!=-1:
			this_id=ln.find("this.", func_id)
			if this_id!=-1:
				if ln.find(".bind(this)",this_id+1)==-1:
					id = this_id+5
					while id<len(ln):
						if ln[id].isalnum() or ln[id]=="_":
							id+=1
						else:
							break
					if id>=len(ln):
						res += ln[0:id]+".bind(this)"
						ln = ln[id:]
					elif ln[id]!=".":
						res += ln[0:id]+".bind(this)"
						ln = ln[id:]
					else:
						res+=ln[0:this_id+5]
						ln = ln[this_id+5:]						
				else:
					res+=ln[0:this_id+5]
					ln = ln[this_id+5:]
			else:
				res+=ln[0:func_id+5]
				ln = ln[func_id+5:]
		else:
			res+=ln
			break
	return res


def add_bind_to_function(ln):
	res=ln
	this_id=ln.find("this.")
	if this_id!=-1:
		# this.funcName -> this.funcName.bind(this)
		if ln.find(".bind(this)")==-1:
			id = this_id+5
			while id<len(ln):
				if ln[id].isalnum() or ln[id]=="_":
					id+=1
				else:
					break
			if id>=len(ln):
				res = ln[0:id]+".bind(this)"+ln[id:]
			elif ln[id]!=".":
				res = ln[0:id]+".bind(this)"+ln[id:]
	return res	

def separate_arguments(args):
	res=[]
	buffer=""
	level=0
	for ch in args:
		if ch in "([{":
			level+=1
			buffer+=ch
		elif ch in "}])":
			level-=1
			buffer+=ch
		elif ch==",":
			if level==1:
				res.append(buffer);
				buffer=""
				pass
			else:
				buffer+=ch
		else:
			buffer+=ch
	if buffer!="":
		res.append(buffer)
	return res

def find_arguments_in_parens(ln, start_id):
	res=""
	level=0
	for id in range(start_id, len(ln)):
		ch = ln[id]
		if ch=="(":
			level+=1
			res+=ch
		elif ch==")":
			level-=1
			res+=ch
			if level==0:
				return res
		else:
			if level>=1:
				res+=ch
	return res

def add_binds(ln):
	# adding binds after:
	# Routines.buildBitBtn(0, 1, 2, this.funcName.bind(this))
	#.registerOn___Function(this.funcName.bind(this)
	# showMessage(0,1,2,[{func:this.funcName.bind(this)}])
	# .addEventListener(0, this.funcName.bind(this))
	res=""
	while (True):
		id = ln.find("Routines.buildBitBtn")
		if id!=-1:
			args_in_parens = find_arguments_in_parens(ln, id+1)
			args_start = ln.find("(",id+1)
			args_end = args_start+len(args_in_parens)

			# print("args_in_parens=",[args_in_parens])
			sep_args=separate_arguments(args_in_parens)
			# print("sep_args=",sep_args)		
			if len(sep_args)>=4:
				sep_args[3] = add_bind_to_function(sep_args[3])
				args_in_parens=",".join(sep_args)
			# print("args_in_parens NEW=",[args_in_parens])
			res+=ln[0:args_start]+args_in_parens
			ln = ln[args_end:]
			# print([ln[0:args_start], ln[args_start:args_end], ln[args_end:]])
		else:
			res+=ln
			break
	ln=res
	res=""
	while (True):
		id = ln.find(".registerOn")
		if id!=-1:
			args_in_parens = find_arguments_in_parens(ln, id+1)
			args_start = ln.find("(",id+1)
			args_end = args_start+len(args_in_parens)

			# print("args_in_parens=",[args_in_parens])
			sep_args=separate_arguments(args_in_parens)
			# print("sep_args=",sep_args)		
			if len(sep_args)>=0:
				sep_args[0] = add_bind_to_function(sep_args[0])
				args_in_parens=",".join(sep_args)
			# print("args_in_parens NEW=",[args_in_parens])
			res+=ln[0:args_start]+args_in_parens
			ln = ln[args_end:]
			# print([ln[0:args_start], ln[args_start:args_end], ln[args_end:]])
		else:
			res+=ln
			break
	ln=res
	res=""
	while (True):
		id = ln.find(".addEventListener")
		if id!=-1:
			args_in_parens = find_arguments_in_parens(ln, id+1)
			args_start = ln.find("(",id+1)
			args_end = args_start+len(args_in_parens)

			# print("args_in_parens=",[args_in_parens])
			sep_args=separate_arguments(args_in_parens)
			# print("sep_args=",sep_args)		
			if len(sep_args)>=1:
				sep_args[1] = add_bind_to_function(sep_args[1])
				args_in_parens=",".join(sep_args)
			# print("args_in_parens NEW=",[args_in_parens])
			res+=ln[0:args_start]+args_in_parens
			ln = ln[args_end:]
			# print([ln[0:args_start], ln[args_start:args_end], ln[args_end:]])
		else:
			res+=ln
			break
	ln=res
	res=""
	while (True):
		id = ln.find(".showMessage")
		if id!=-1:
			args_in_parens = find_arguments_in_parens(ln, id+1)
			args_start = ln.find("(",id+1)
			args_end = args_start+len(args_in_parens)

			# print("args_in_parens=",[args_in_parens])
			sep_args=separate_arguments(args_in_parens)
			# print("sep_args=",sep_args)		
			if len(sep_args)>=4:
				sep_args[3] = add_bind_to_func_in_objects(sep_args[3])
				args_in_parens=",".join(sep_args)
			# print("args_in_parens NEW=",[args_in_parens])
			res+=ln[0:args_start]+args_in_parens
			ln = ln[args_end:]
			# print([ln[0:args_start], ln[args_start:args_end], ln[args_end:]])
		else:
			res+=ln
			break
	return res

# print(add_binds("Routines.buildBitBtn(0, 1, Math.min(2,3,5), this.funcNam ,12)asdasRoutines.buildBitBtn(0, 1, Math.min(2,3,5), this.funcNam ,12)"))