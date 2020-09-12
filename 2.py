import requests
import json
from jsonpath import jsonpath
import os
import urllib


#定义生成文件方法
def get_pic_by_url(dir_name,url):
    #print(os.getlogin())
    #p1 = 'C:\\Users\\'
    #p2 = os.getlogin()
    #p3 = '\\Desktop\\'
    #p4='\\'
    
    #folder_path=p1+p2+p3+str(f_name)
    folder_path=('C:\\Users\\'+os.getlogin()+'\\Desktop\\'+str(dir_name))
    #folder_path=(r"C:\Users\ "+ os.getlogin() +"\\Desktop\\ " + f_name)
    #print(folder_path)
    if not os.path.exists(folder_path):
        print("Selected folder not exist, try to create it.")
        os.makedirs(folder_path) 
    filename = url.split('/')[-1]
    filepath = folder_path + '\ ' + filename
    #print(filepath)
    if os.path.exists(filepath):
        print("File has already exist. skip")
    else:
        try:

           urllib.request.urlretrieve(url, filename=filepath)
        except Exception as e:
           print("Error occurred when downloading files, error message:")
           print(e)
           
#获取UP主名字
def get_dir_name(number,headers):
    name_url='https://api.bilibili.com/x/space/acc/info?'
    p={
        'mid':number,
        'jsonp':'jsonp'
        
        }
    r=requests.get(url=name_url,params=p,headers=headers)
    name=r.text
    name=json.loads(name)
    name=jsonpath(name,'$.[data].name')
    name=name[0]+'-p'
    
    return name

# 指定ajax-get请求的url（通过抓包进行获取）
url = 'https://api.vc.bilibili.com/link_draw/v1/doc/doc_list?'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.44',
                }


number=input("请输入up主页号:")
page=input("请输入要抓取的页数:")
dirname= get_dir_name(number,headers)
print("将生成文件在："+str(dirname))
# 封装ajax的get请求携带的参数(从抓包工具中获取) 封装到字典

for i in range(int(page)):
                param = {
                 'uid':number,
                 'page_num':i,
                 'page_size':'30',
                 'biz':'all'
  
                }
                
# 定制请求头信息，相关的头信息必须封装在字典结构中
               
                
# 发起ajax的get请求还是用get方法
                response = requests.get(url=url,params=param,headers=headers)

 
# 获取响应内容：响应内容为json字符串
                data = response.text
                data2 = json.loads(data)

#print(data2)
#print("============================================================")
#for data2_dict in data2:
                
                data3=jsonpath(data2,'$..items[*].doc_id')
  
                print (data3)
                print('---------------------------------------------')

                url2='https://api.vc.bilibili.com/link_draw/v1/doc/detail?'
                for index in range(len(data3)):
                               print ('当前动态id :', data3[index])
                               param2={
                                 "doc_id":data3[index]
                                               }
                               
                               #headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.44',}

                               response2 = requests.get(url=url2,params=param2,headers=headers)
                               data4=response2.text
                               data5=json.loads(data4)
                               data5=jsonpath(data5,'$..pictures[*].img_src')
                               for index2 in range(len(data5)):
                                               print('图片链接:',data5[index2])
                                               get_pic_by_url(dirname,data5[index2])
                               print('```````````````````````````````````````````````````````')
                               
                   
 
print ("Good bye!")




  
