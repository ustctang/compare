!/grid/common/pkgsData/pypy3.6-v7.3.1/Linux/RHEL6.0-2013-x86_64/bin/pypy3
import sys
import difflib
import os 
import pandas as pd 
import re
import subprocess as sb
import compare  
path1=compare.path1
path2=compare.path2
l1=len(path1)
l2=len(path2)
#import binarydif
def readfile(file1):
    try:
       fd=open(file1,"r")
       text=fd.read().splitlines()
       return text
      
    except Exception as e:
       print("read file error")
       print(e)
       sys.exit()
def Compare(file_1, file_2,strname):
    if file_1==" " or file_2==" ":
       print("file_1 or file_2 not empty")
       sys.exit()
    text1=readfile(file_1)
    text2=readfile(file_2)
    diff=difflib.HtmlDiff()
    result=diff.make_file(text1,text2, context=True)

    f_name = strname
    tmp_file_name = f_name+'.html'#the son html name
    try:
        fd_diff=open(tmp_file_name ,"w")
        fd_diff.write(result)
        fd_diff.close()
        return tmp_file_name 
    except Exception as e:
        print("write text file error")
        print(e)
        sys.exit()
def generate_miss(cols,filelist,filename):
   con=0
   folder=os.getcwd()
   for  i in range(cols) :
       file1=filelist [0][i]
       file2=filelist [1][i]
       con=con+1
       if file1!="MISS":
          file1_name=file1[l1:]
          file2_name=file2
       else:
          file1_name=file1
          file2_name=file2[l2:]

       listname=str(con)+'-->'+'&ensp;'+str(file1_name)+'&emsp;'+'---vs---'+'&emsp;'+str(file2_name)
       filename.write('    '+'    '+'    '+'     '+'<li>'+listname+'</a></li>')
       filename.write('<br>')
       filename.write('\r\n')

def generate_different(cols,filelist,filename):
   con=0
   folder=os.getcwd()
  # print(path1)
   for  i in range(cols) :
       file1=filelist [0][i]
       file2=filelist [1][i]
       #if os.path.isfile(file1)and os.path.isfile(file2):
       fileaccess=(select_file(file1)and select_file(file2))
       flag1=file_type(file1)
       flag2=file_type(file2)
       if fileaccess and  flag1==1 and flag2==1:
          str1=str(file1).split('/')
          str2=str(file2).split('/')
          if str1[-1]==str2[-1]:
            strname=str1[-1]
            con=con+1
            htmlname=Compare(file1,file2,strname)
            html_name=str(folder)+'/'+str(htmlname)
            listname=str(con)+'-->'+'&ensp;'+str(file1[l1:])+'&emsp;'+'---vs---'+'&emsp;'+str(file2[l2:])
            #listname=str(con)+'-->'+'&ensp;'+str(file1)+'&emsp;'+'<font color ="#555555";style="font-size:50px;">'+'---vs---'+'</font>'+'&emsp;'+str(file2)
            filename.write('    '+'    '+'    '+'     '+'<li><a href='+'\"'+html_name+'\"'+'>'+listname+'</a></li>')
            filename.write('<br>')
            filename.write('\r\n')

       elif  flag1==2 and flag2==2:
          cmd1='cksum '+file1
          cmd2='cksum '+file2
          output1=str(run_it(cmd1))
          output2=str(run_it(cmd2))
          str1=str(file1).split('/')
          str2=str(file2).split('/')
          if str1[-1]==str2[-1]:
            strname=str1[-1]
            con=con+1
            folder = os.getcwd()# work directory
            fname=strname+".html"#the main html file name
            f=open(fname,"w")
            f.write("Result of comparison: "),f.write('<br>')
            f.write(output1),f.write('<br>')
            f.write(output2),f.write('<br>')
            #f.write("Num. differences: ", len(binarydif.c.diff_list)),f.write('\r\n')
            f.close()
            html_name=str(folder)+'/'+str(fname)
            #listname=str(con)+'-->'+'&ensp;'+str(file1)+'&emsp;'+'---vs---'+'&emsp'+str(file2)
            listname=str(con)+'-->'+'&ensp;'+str(file1[l1:])+'&emsp;'+'<font color ="#555555";style="font-size:50px;">'+'---vs---'+'</font>'+'&emsp;'+str(file2[l2:])
            filename.write('    '+'    '+'    '+'     '+'<li><a href='+'\"'+html_name+'\"'+'>'+listname+'</a></li>')
            filename.write('<br>')
            filename.write('\r\n')
       elif flag1==3 and flag2==3:
          output1,output2=linkdif(file1,file2)
          str1_link=str(file1).split('/')
          str2_link=str(file2).split('/')
          out_link_sep1=output1.split(' ')
          out_link_sep2=output2.split(' ')
          if str1_link[-1]==str2_link[-1]:
            strname=str1_link[-1]
            con=con+1
            folder=os.getcwd()
            fname=strname+".html"#the main html file name
            f=open(fname,"w")
            if out_link_sep1[-1]!=out_link_sep2[-1]:
               f.write("link to file: ")
            else:
               f.write("the file of link is different:")
            f.write('<br>')
            f.write(output1)
            f.write('<br>')
            f.write(output2)
            f.write('<br>')
            #f.write("Num. differences: ", len(binarydif.c.diff_list)),f.write('\r\n')
            f.close()
            html_name=str(folder)+'/'+str(fname)
            listname=str(con)+'-->'+'&ensp;'+str(file1[l1:])+'&emsp;'+'<font color ="#555555";style="font-size:50px;">'+'---vs---'+'</font>'+'&emsp;'+str(file2[l2:])
            filename.write('    '+'    '+'    '+'     '+'<li><a href='+'\"'+html_name+'\"'+'>'+listname+'</a></li>')
            filename.write('<br>')
            filename.write('\r\n')
       else:
          continue  
            
def linkdif(file1,file2):
   cmd1='file -b '+file1
   cmd2='file -b '+file2
    
   str1=str(run_it(cmd1))
   str2=str(run_it(cmd2))
   f1=str1.split(" ")
   f2=str2.split(" ")
   return f1[-1],f2[-1]

def run_it(cmd):
    p = sb.Popen(cmd, stdout=sb.PIPE, shell=True,
                         stderr=sb.PIPE, close_fds=True)
    stdout,stderr=p.communicate()
    return stdout
def select_file(filename):
    ret=os.access(filename,os.R_OK)
    return ret 

def file_type(file1):
   cmd='file -b '+file1
   str1=str(run_it(cmd))
   key1='ASCII'
   #key2='GDSII'
   key3='link'
   if re.search(key1,str1):
       judge=1
   #elif re.search(key2,str1):
   #    judge=2
   elif re.search(key3,str1):
       judge=3
   else:
       judge=2 
   return judge
 






def __SUMMARY__():
   folder = os.getcwd()# work directory
   fname=folder+"/summary.html"#the main html file name
   filename=open(fname,"w")#generate a main list html file name a the_one.html
   filename.write('<!DOCTYPE html>')
   filename.write('\r\n')
   filename.write('<html>'),filename.write('\r\n')
   filename.write('<head>'),filename.write('\r\n')
   filename.write('<meta charset="utf-8">'),filename.write('\r\n')
   filename.write('<title>'+'summary'+'</title>'),filename.write('\r\n')
   filename.write('<body>'),filename.write('\r\n')
   #filename.write('<h2>MISS files </h2>'),filename.write('\r\n')
   filename.write('</head>'),filename.write('\r\n')
   UR=["differentfiles.html","missfiles.html","errorlink.csv.html","samefiles.csv.html","samedirectory.csv.html"]
   for ur in UR:
     filename.write('<br>')
     url=folder+"/"+ur#folder
     i=ur.split(".")[0]
     
     filename.write('<a href='+url+'>')#,filename.write('\r\n')
     
     filename.write('<input type="button" value='+i+' style="font-size:30px;heigth=60px;width=100px;background-color:#008CBA ;">')
     filename.write('</a>')
     filename.write('\r\n')
   

#   filename.write('<br>')
#   url=folder+"/missfiles.html"#folder
#   filename.write('<a href='+url+'>')#,filename.write('\r\n')
#   filename.write('<input type="button" value="Miss Files" style="font-size:30px;heigth=60px;width=100px;background-color:#008CBA ;">')
#   filename.write('</a>')
#   filename.write('\r\n')
#   
#   filename.write('<br>')
#   ur2=folder+"/errorlink.csv.html"#folder
#   filename.write('<a href='+ur2+'>')#,filename.write('\r\n')
#   filename.write('<input type="button" value="error_links" style="font-size:30px;heigth=60px;width=100px;background-color:#008CBA ;">')
#   filename.write('</a>')
#   filename.write('\r\n')
#
#   filename.write('<br>')
#   ur3=folder+"/samefiles.csv.html"#folder
#   filename.write('<a href='+ur3+'>')#,filename.write('\r\n')
#   filename.write('<input type="button" value="samefiles" style="font-size:30px;heigth=60px;width=100px;background-color:#008CBA ;">')
#   filename.write('</a>')
#   filename.write('\r\n')
#
#   filename.write('<br>')
#   ur4=folder+"/samedirectory.csv.html"#folder
#   filename.write('<a href='+ur4+'>')#,filename.write('\r\n')
#   filename.write('<input type="button" value="samedirectory" style="font-size:30px;heigth=60px;width=100px;background-color:#008CBA ;">')
#   filename.write('</a>')
#   filename.write('\r\n')
#
   filename.write('<br>')
   
   #filename.write('<h2>End </h2>'),filename.write('\r\n')
   filename.write('<body>'),filename.write('\r\n')

   filename.write('<h1  style="font-size:20px;color:rgba(11,19,86,0.5);">'+'path1: '+path1+'</h1>'),filename.write('\r\n')
   filename.write('<h1  style="font-size:20px;color:rgba(11,19,86,0.5);">'+'path2: '+path2+'</h1>'),filename.write('<br>'),filename.write('\r\n')

   #filename.write('<h2>Different files </h2>')
   #filename.write('\r\n')
   #filename.write('    '+'<header>'),filename.write('\r\n')
   #filename.write('    '+'    '+'<nav>'),filename.write('\r\n')
   #filename.write('    '+'    '+'    '+'<ul>'), filename.write('\r\n')
   #generate_summary(cols,filelist,filename)
   #filename.write('    '+'    '+'    '+'</ul>'), filename.write('\r\n')
   #filename.write('    '+'    '+'</nav>'),filename.write('\r\n')
   #filename.write('    '+'</header>'),filename.write('\r\n')
   #filename.write('<h2>end</h2>'),filename.write('\r\n')
   filename.write('</body>'),filename.write('\r\n')
   filename.write('</html>'),filename.write('\r\n')
   filename.close      

def different_files(cols,filelist):
   folder = os.getcwd()# work directory
   fname=folder+"/differentfiles.html"#the main html file name
   filename=open(fname,"w")#generate a main list html file name a the_one.html
   filename.write('<!DOCTYPE html>')
   filename.write('\r\n')
   filename.write('<html>'),filename.write('\r\n')
   filename.write('<head>'),filename.write('\r\n')
   filename.write('<meta charset="utf-8">'),filename.write('\r\n')
   filename.write('<title>'+'differentfiles'+'</title>'),filename.write('\r\n')
   
   filename.write('</head>'),filename.write('\r\n')
   filename.write('<h1  style="font-size:20px;color:rgba(11,19,86,0.5);">'+'path1: '+path1+'</h1>'),filename.write('\r\n')
   filename.write('<h1  style="font-size:20px;color:rgba(11,19,86,0.5);">'+'path2: '+path2+'</h1>'),filename.write('<br>'),filename.write('\r\n')

   filename.write('<body>'),filename.write('\r\n')
   filename.write('<h2>different Files</h2>'),filename.write('\r\n')
   filename.write('    '+'<header>'),filename.write('\r\n')
   filename.write('    '+'    '+'<nav>'),filename.write('\r\n')
   filename.write('    '+'    '+'    '+'<ul>'), filename.write('\r\n')
   generate_different(cols,filelist,filename)
   filename.write('    '+'    '+'    '+'</ul>'), filename.write('\r\n')
   filename.write('    '+'    '+'</nav>'),filename.write('\r\n')
   filename.write('    '+'</header>'),filename.write('\r\n')
   filename.write('<h2>end</h2>'),filename.write('\r\n')
   filename.write('</body>'),filename.write('\r\n')
   filename.write('</html>'),filename.write('\r\n')
   
   filename.close      



def miss_files(cols,filelist):
   folder = os.getcwd()# work directory
   fname=folder+"/missfiles.html"#the main html file name
   filename=open(fname,"w")#generate a main list html file name a the_one.html
   filename.write('<!DOCTYPE html>')
   filename.write('\r\n')
   filename.write('<html>'),filename.write('\r\n')
   filename.write('<head>'),filename.write('\r\n')
   filename.write('<meta charset="utf-8">'),filename.write('\r\n')
   filename.write('<title>'+'missfiles'+'</title>'),filename.write('\r\n')
   
   filename.write('</head>'),filename.write('\r\n')
   filename.write('<h1  style="font-size:20px;color:rgba(11,19,86,0.5);">'+'path1: '+path1+'</h1>'),filename.write('\r\n')
   filename.write('<h1  style="font-size:20px;color:rgba(11,19,86,0.5);">'+'path2: '+path2+'</h1>'),filename.write('<br>'),filename.write('\r\n')

   filename.write('<body>'),filename.write('\r\n')
   filename.write('<h2>Miss Files</h2>'),filename.write('\r\n')
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



 
if __name__ == '__main__':
  filepath=os.getcwd()
  
  file_path=filepath+"/different_files.csv"
  file_path1=filepath+"/missfiles.csv"
  __SUMMARY__()
  if os.path.getsize(file_path):
     file_target=pd.read_csv(file_path,header=None,usecols=[1,2]).T
     filelist= file_target.values.tolist()
     (row, cols)=file_target.shape
     different_files(cols,filelist)
  else:
     print("no different files, please check ",file_path)
  if os.path.getsize(file_path1):
     file_target=pd.read_csv(file_path1,header=None,usecols=[1,2]).T
     filelist= file_target.values.tolist()
     (row, cols)=file_target.shape
     miss_files(cols,filelist)
  else:
     print("no miss files, please check ",file_path1)

  
  print("the diff.py finish")
  file_dir=filepath+"/makefile.py"
  os.system(file_dir)
