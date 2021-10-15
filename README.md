# compare
1. purpose :compare two similar Folder,  for example : we have Folder A1 and Folder A2
2. A1 contains  B1 , B2 , C1 ,C2 files , A2 contains B1,C1, C2, D1 files.  there are some different contents between B1 files in A1 and B1files in A2. The summary.html will shows  table as below
         A1    A2
         B1    B1
         B2    Missed
        C1    C1
        C2    C2
        missed     D1
      the  different content between B1 files in A1 and B1files in A2 will underline with differen color background
3. the code is written by python3  in linux system .
4. please make sure that you have installed python3 and related libraries.(please modify the python3 path with the path which  you have install : +#!/grid/common/pkgsData/pypy3.6-v7.3.1/Linux/RHEL6.0-2013-x86_64/bin/pypy3) 

5 . please add the two folder path in compare.py script, run the compare.py directly . 
6. when the program were finished , please open the summary.html with browser.

