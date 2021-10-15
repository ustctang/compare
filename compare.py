#!/grid/common/pkgsData/pypy3.6-v7.3.1/Linux/RHEL6.0-2013-x86_64/bin/pypy3
import os 
import sys
import pandas as pd 
import numpy as np
import gzip
import subprocess as sb 
import re 
#import commands as cd 
#path1="/dpc/tsmc_project15/jasons01/tsmc7nm/EC117718/nicolasc/oio_tight_integration_demo_v5a_test_psdl"
#path1="/dpc/project48/xlchen/SMIC_PROG/IT360396/hanyut/test/65LP.gds"
#path2="/dpc/project48/xlchen/SMIC_PROG/IT360396/hanyut/test/64LP"
#path2="/dpc/tsc_project15/jasons01/tsmc7nm/EC117718/nicolasc/oio_tight_integration_demo_v5a_test_early_psdl"
#path1= "/dpc/project48/xlchen/SMIC_PROG/IT360396/hanyut/test/ts1"
#path2 ="/dpc/project48/xlchen/SMIC_PROG/IT360396/hanyut/test/ts2"

path1= "/dpc_it/sjcladpc01p7_scratch05/hanyut/a2021_08_24_19_38_01_sjfdcl732_405153/dpc_hanyu/RAK_3DIC/tmp/sipi_demo_scirpts1"
path2= "/dpc_it/sjcladpc01p7_scratch05/hanyut/a2021_08_24_19_38_01_sjfdcl732_405153/dpc_hanyu/RAK_3DIC/tmp/sipi_demo_scirpts"
#path2 ="/dpc_it/sjcladpc01p7_scratch04/nicolasc/a2021_07_20_20_18_47_sjfdcl834_151533/nicolasc_scratch/riscv_3dic_v2L/input_data"






#path1="/dpc/project48/xlchen/SMIC_PROG/IT360396/hanyut/RAK_3DIC/sipi_demo_scirpts/clarity_setup"
#path2="/dpc_it/sjcladpc01p7_scratch04/nicolasc/a2021_07_20_20_18_47_sjfdcl834_151533/nicolasc_scratch/sipi_demo_scirpts/clarity_setup"
#def bisFileopen(file,judge):
#  if judge is True:
#       f=gzip.open(file,"wb")
#       print("is a zip file")
#       f.close
#  elif judge is False:
#       print("is not a zip file")
def run_it(cmd):
    p = sb.Popen(cmd, stdout=sb.PIPE, shell=True,
                         stderr=sb.PIPE, close_fds=True)
    stdout,stderr=p.communicate()
    return stdout
def select_file(filename):
    ret=os.access(filename,os.W_OK)
    return ret 
def traverse1(filepath):
    files=os.listdir(filepath)
    for fi in files:
        fi_d = os.path.join(filepath, fi)
        ret=select_file(fi_d)
        if os.path.isdir(fi_d):# whether it is a empty directory
            if not os.listdir(fi_d) and ret:#if it an empty directory, delete it 
                os.rmdir(fi_d)
            else:
                traverse1(fi_d)
        else:
            file1=os.path.join(filepath, fi_d)
            filetype=file_type(file1)
            fileaccess=select_file(file1)
            if filetype==1 and fileaccess:
                if os.path.getsize(file1)==0: #file size is 0
                    os.remove(file1)#delete the file
def file_type(file1):
   cmd='file -b '+file1
   str1=str(run_it(cmd))
   key1='ASCII'
   #key2='GDSII'
   key3='link'
   key4='broken'
   if re.search(key4,str1):
       judge=0
   elif re.search(key1,str1):
       judge=1
   #elif re.search(key2,str1):
    #   judge=2
   elif re.search(key3,str1):
       judge=3
   else:
       judge=2
   return judge
def binarydif(file1,file2):
   cmd1='cksum '+file1
   cmd2='cksum '+file2
   str1=str(run_it(cmd1))
   str2=str(run_it(cmd2))
   f1=[float(a)for a in re.findall(r"(\b\d+\b)", str1)]
   f2=[float(a)for a in re.findall(r"(\b\d+\b)", str2)]
   if f1!=f2:
      return False
   else: 
      return True
def linkdif(file1,file2):
   cmd1='file -b '+file1
   cmd2='file -b '+file2
    
   link_str1=str(run_it(cmd1))
   link_str2=str(run_it(cmd2))
   f1=link_str1.split(" ")
   f2=link_str2.split(" ")
   if f1[-1]!=f2[-1]:
      return False
   else: 
      return True
def get_file(path):# creat a new list 
    file_dirname=[] # file path name
    
    for root,dirs,files in os.walk(path,topdown=True):#go through all the director 
        for name in files:# yi ji zi mu lu
            file_top_name=os.path.join(root,name)
            file_dirname.append(file_top_name)
        for name in dirs:# n ji zi mu lu
            file_down_name=os.path.join(root,name)
            file_dirname.append(file_down_name)
    return file_dirname
def errorjudge(f1,f2):
    flag1=file_type(f1)
    flag2=file_type(f2)
    if flag1==0 or flag2==0:
       #return False
       print("broken links")
       return False
    else:
       return True
def folder_level(file1, path1, file2, path2):
    f1=set(sorted(file1.split(os.path.sep)))-set(sorted(path1.split(os.path.sep)))
    f2=set(sorted(file2.split(os.path.sep)))-set(sorted(path2.split(os.path.sep)))
    
    if f1!=f2:
      return False
    else:
      return True 

def cmp_file(f1, f2):
    flag1=file_type(f1)
    flag2=file_type(f2)
    st1 = os.stat(f1)
    st2 = os.stat(f2)
    if st1.st_size != st2.st_size:
        return False
    bufsize = 8*1024
    #print(flag1)
    if flag1==2 and flag2==2:
       flagBinary=binarydif(f1,f2)
       if flagBinary:
          return True 
       else
          return False 
    elif  flag1==1 and flag2==1:      
       with open(f1, 'rb') as fp1, open(f2, 'rb') as fp2:
         while True:
            b1 = fp1.read(bufsize)  # read the size of data
            b2 = fp2.read(bufsize)
            if b1 != b2:
                return False
            if not b1:
                return True      
    elif flag1==3 and flag2==3:
       links=linkdif(f1,f2)
       if links:
          return True
       else:
          return False
    else:
       return False
       

if __name__=='__main__':
    path=path1
    traverse1(path)
    list1=get_file(path)
    size1=len(list1)
    df=pd.DataFrame(list1)#columns=["list"]#)       #  df.to_csv('taxi2.csv',mode='a',header=None)
    df.to_csv('path1.csv',mode='w',header=None)
    path=path2
    traverse1(path)
    list2=get_file(path)
    
    size2=len(list2)
    df=pd.DataFrame(list2)#columns=["list"]#)       #  df.to_csv('taxi2.csv',mode='a',header=None)
    df.to_csv('path2.csv',mode='w',header=None)
    count =0
    list3=[]
    list4=[]
    list5=[]
    list6=[]
    list7=[]
    list8=[]
    num=int(size1+size2+1)
    print(num)
    print("all empty files removed ")
    difflist=(np.zeros((2,num),dtype=int)).tolist()
     
    for i in range (len(list1)):
        for j in range(len(list2)):
          file1=list1[i]
          file2=list2[j]
          key=folder_level(file1, path1, file2, path2)
          if key: #and second_file1[-2]==second_file2[-2]:
             if not os.path.isdir(file1 and file2):
                if errorjudge(file1, file2):
                  if cmp_file(file1,file2):
                     list3.append(file1)
                     list4.append(file2)
                  else:
                     difflist[0][count]=file1
                     difflist[1][count]=file2
                     count=count+1
                else:
                  list5.append(file1)
                  list6.append(file2)
             elif file_type(file1)==3 and file_type(file2)==3:# link to directory 
                if cmp_file(file1,file2):
                   list3.append(file1)
                   list4.append(file2)
                else:
                   difflist[0][count]=file1
                   difflist[1][count]=file2
                   count=count+1
             elif errorjudge(file1,file2)is False :
                list5.append(file1)
                list6.append(file2)
             else:     
                list7.append(file1)
                list8.append(file2)
          else:
           continue 
    datasame=list(zip(list3, list4))
    df=pd.DataFrame(datasame,columns=['path1','path2'])#columns=["list"]#)       #  df.to_csv('taxi2.csv',mode='a',header=None)
    df.to_csv('samefiles.csv',mode='w',header=None)
    data1=list(zip(list5, list6))
    df=pd.DataFrame(data1,columns=['path1','path2'])#columns=["list"]#)       #  df.to_csv('taxi2.csv',mode='a',header=None)
    df.to_csv('errorlink.csv',mode='w',header=None)
    data2=list(zip(list7, list8))
    df=pd.DataFrame(data2,columns=['path1','path2'])#columns=["list"]#)       #  df.to_csv('taxi2.csv',mode='a',header=None)
    df.to_csv('samedirectory.csv',mode='w',header=None)
    file_df1=[x for x in difflist[0] if x!=0]
    file_df2=[y for y in difflist[1] if y!=0]
    data3={"path1":file_df1,
       "path2":file_df2}
     
    df=pd.DataFrame.from_dict(data3,orient='index').T
    #df=pd.DataFrame(data3,columns=['path1','path2'])#columns=["list"]#)       #  df.to_csv('taxi2.csv',mode='a',header=None)
    df.to_csv('different_files.csv',mode='w',header=None)
  
    c1=set(difflist[0])
    c2=set(difflist[1])
    datadiff1=list(set(list1)-set(list3)-c1-set(list5)-set(list7))
     
    datadiff2=list(set(list2)-set(list4)-c2-set(list6)-set(list8))
    datadiff=[datadiff1,datadiff2]#.reshape(2,1)
    i=0
    j=0
    str1="MISS"
    flag=count
    for i in range(len(datadiff[0])):
        difflist[0][count+i]=datadiff[0][i]
        difflist[1][count+i]=str1
    count=count+i+1
    for j in range(len(datadiff[1])):
        difflist[0][count+j]=str1
        difflist[1][count+j]=datadiff[1][j] 
    sum_diff1=[x1 for x1 in difflist[0][flag:] if x1!=0]
    sum_diff2=[y1 for y1 in difflist[1][flag:] if y1!=0]
    c={"path1":sum_diff1,
       "path2":sum_diff2}
    df=pd.DataFrame.from_dict(c,orient='index').T #columns=['path1','path2'])
    df.to_csv('missfiles.csv',mode='w',header=None)
    #sys.exit()

    print("compare.py finish")
    filedir=os.getcwd()
    script=filedir+'/'+'diff.py'
    os.system(script)
