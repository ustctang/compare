#!/grid/common/pkgsData/pypy3.6-v7.3.1/Linux/RHEL6.0-2013-x86_64/bin/pypy3
import os
import pandas as pd
import compare  
path1=compare.path1
path2=compare.path2
l1=len(path1)
l2=len(path2)

def generate_files(cols,filelist,file_path):
   #folder = os.getcwd()# work directory
   fname=file_path+".html"#the main html file name
   title_name=file_path.split('/')[-1].split('.')[-2]
   filename=open(fname,"w")#generate a main list html file name a the_one.html
   filename.write('<!DOCTYPE html>')
   filename.write('\r\n')
   filename.write('<html>'),filename.write('\r\n')
   #filename.write()
   filename.write('<head>'),filename.write('\r\n')
   filename.write('<meta charset="utf-8">'),filename.write('\r\n')
   filename.write('<title>'+title_name+'</title>'),filename.write('\r\n')
   filename.write('</head>'),filename.write('\r\n')
   filename.write('<body>'),filename.write('\r\n')

   filename.write('<h1  style="font-size:20px;color:rgba(11,19,86,0.5);">'+'path1: '+path1+'</h1>'),filename.write('\r\n')
   filename.write('<h1  style="font-size:20px;color:rgba(11,19,86,0.5);">'+'path2: '+path2+'</h1>'),filename.write('<br>'),filename.write('\r\n')



   filename.write('<h2>'+title_name+'</h2>'),filename.write('\r\n')
   filename.write('    '+'<header>'),filename.write('\r\n')
   filename.write('    '+'    '+'<nav>'),filename.write('\r\n')
   filename.write('    '+'    '+'    '+'<ul>'), filename.write('\r\n')
   generate_miss(cols,filelist,filename)
   filename.write('    '+'    '+'    '+'</ul>'), filename.write('\r\n')
   filename.write('    '+'    '+'</nav>'),filename.write('\r\n')
   filename.write('    '+'</header>'),filename.write('\r\n')
   filename.write('<h2>end</h2>'),filename.write('\r\n')
   filename.write('</body>'),filename.write('\r\n')
   filename.write('</html>'),filename.write('\r\n')
   
   filename.close


