# in Flash and Starling we change the image scale by changing its width, but in Phaser we do this with displayWidth
def find_variable_beginning_id_before(s, id):
	res=-1
	# we must see, in reversed order: :, *, /
	if s[id-3:id]=="/*:":
		id2 = id-4
		is_writing_token = False

		while id2>=0:
			ch = s[id2]
			if ch.isalnum() or ch=="_":
				if not is_writing_token:
					is_writing_token=True
			else:
				if is_writing_token:
					res=id2
					break
			id2-=1
	return res

def find_images_list(s):
	res=[]
	id=-1
	need_1_more=True
	while (need_1_more):
		need_1_more=False
		tks = ["Image","MovieClip","DisplayObject"]
		
		best_idn=-1
		best_n=-1
		for n in range(len(tks)):
			id_n = s.find(tks[n], id+1)
			if id_n!=-1:
				if best_idn==-1 or id_n<best_idn:
					best_idn = id_n
					best_n = n
		id = best_idn
		if id!=-1:
			tk_len = len(tks[best_n])
		# print("id=",id)
		if id!=-1:
			nxt_ch = s[id+tk_len]
			# print("nxt_ch=",nxt_ch)
			if not (nxt_ch.isalnum() or nxt_ch=="_"):
				id2 = find_variable_beginning_id_before(s,id)
				# print("id2=",id2)
				if id2!=-1:
					res.append(s[id2+1:id-3])
					# print([s[id2+1:id-3]])
			need_1_more=True
	return res


def add_display_after_img(s, im):
	res=""
	while len(s)>0:
		id = s.find(im)
		# print("id=",id)
		if id!=-1:
			ch_nxt = s[id+len(im)]
			# print("ch_nxt=",ch_nxt)
			will_add_display = False
			added_ch = ""
			nxt_token_len = 0
			if not (ch_nxt.isalnum() or ch_nxt=="_"):
				if s[id+len(im)]==".":
					if s[id+len(im)+1:id+len(im)+6]=="width":
						added_ch=".displayWidth"
						nxt_token_len=5
					if s[id+len(im)+1:id+len(im)+7]=="height":
						added_ch=".displayHeight"
						nxt_token_len=6
					if s[id+len(im)+1:id+len(im)+6]=="color":
						added_ch=".tint"
						nxt_token_len=5
					ch_nxt = s[id+len(im)+nxt_token_len+1]
					if not (ch_nxt.isalnum() or ch_nxt in "_.[({"):
						will_add_display=True
			# print("will_add_display=",will_add_display)
			if will_add_display:
				res+=s[0:id+len(im)]+added_ch
				s = s[id+len(im)+nxt_token_len+1:]				
			else:
				res+=s[0:id+1]
				s = s[id+1:]
		else:
			res+=s
			s=""
		# print(["res",res,"s",s])
	return res

def fix_images_width(s):
	imgs=find_images_list(s)
	# print(imgs)
	# looking for all Image
	# and replacing width, height
	# into  displayWidth, displayHeight
	for im in imgs:
		s = add_display_after_img(s, im)
	return s
