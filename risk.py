import os, codecs
import shutil

src_dir=os.curdir

for f in sorted(os.listdir('good')):
	if f.endswith(".txt"):
		name=os.path.splitext(f)[0]
		dst_dir=os.path.join(os.curdir,name,f)
		src_file=os.path.join(src_dir,'good',f)
		shutil.copy(src_file,dst_dir)
		
		dst_file=os.path.join(name,f)
		new_file=os.path.join(name,"risk.txt")
		os.rename(dst_file,new_file)