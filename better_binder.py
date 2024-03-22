#adding .bind(this) always if this.function does not have ( or . after it
def find_word_end_after(s, start_id):
	for id in range(start_id, len(s)):
		ch=s[id]
		if not (ch.isalnum() or ch=="_"):
			break
	return id-1

def has_function_call_after(s, start_id):
	res=False
	for id in range(start_id, len(s)):
		ch=s[id]
		if ch=="." or ch=="(":
			return True
		if ch in " 	\n":
			id+=1
		else:
			return False

def better_binds(s, list_of_func):
	res=""
	while s!="":
		thid=s.find("this.")
		if thid!=-1:
			ch=s[thid-1]
			if not (ch.isalpha() or ch=="_"):
				endid=find_word_end_after(s, thid+5)
				wrd=s[thid+5:endid+1]
				if wrd in list_of_func:
					if not has_function_call_after(s, endid+1):
						res+=s[0:endid+1]+".bind(this)"
					else:
						res+=s[0:endid+1]
				else:
					res+=s[0:endid+1]
				s=s[endid+1:]
			else:
				res+=s[0:thid+5]
				s=s[thid+5:]
		else:
			res+=s;
			break
	
	return res