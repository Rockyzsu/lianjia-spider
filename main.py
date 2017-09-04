# coding: utf-8
import os,subprocess
root_folder=os.getcwd()

spider_m_sh_su=os.path.join(root_folder,'spider_m_sh.py')
spider_normal=os.path.join(root_folder,'spider_m.py')
cmd_list=[#'python '+spider_m_sh_su+' lianjia_m_sh su',
          #'python '+spider_m_sh_su+' lianjia_m_sh sh',
          ]
std_fp=open('spider.log','a')
err_fp=open('spder_err.log','a')
for cmd in cmd_list:
    print cmd
    p=subprocess.Popen(cmd,stdout=std_fp,stderr=err_fp,shell=True)
    p.communicate()
    p.wait()

std_fp.close()
err_fp.close()