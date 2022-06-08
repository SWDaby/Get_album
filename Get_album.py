import requests
import json
from jsonpath import jsonpath
import os
import urllib
from fake_useragent import UserAgent



#获取游客cookie
def getCookie():
  url = "https://www.bilibili.com/"
  Hostreferer = {
    #'Host':'***',
    'User-Agent': UserAgent().random,
  }
  #urllib或requests在打开https站点是会验证证书。 简单的处理办法是在get方法中加入verify参数，并设为False
  html = requests.get(url, headers=Hostreferer,verify=True)
  #获取cookie:DZSW_WSYYT_SESSIONID
  if html.status_code == 200:
    #print(html.cookies)

    cookies_dict = requests.utils.dict_from_cookiejar(html.cookies)
    cookies_str = json.dumps(cookies_dict)
    #print(cookies_str)
    return  cookies_str


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


if __name__ == '__main__':

    # 指定ajax-get请求的url（通过抓包进行获取）
    url = 'https://api.vc.bilibili.com/link_draw/v1/doc/doc_list?'
    headers = {'User-Agent': UserAgent().random,
               "cookie":getCookie()
               #'cookie':'buvid3=22B20D8F-B1D1-7026-28C3-CF45B43F6B1E18520infoc; i-wanna-go-back=-1; b_ut=7; CURRENT_BLACKGAP=0; CURRENT_FNVAL=80; innersign=0'
                    }

    id_number=input("请输入up主页号:")
    page=input("请输入要抓取的页数:")
    dirname= get_dir_name(id_number, headers)
    print("将生成文件在："+str(dirname))
    # 封装ajax的get请求携带的参数(从抓包工具中获取) 封装到字典

    for i in range(int(page)):
                    param = {
                     'uid':id_number,
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

                    print(data3)
                    print('---------------------------------------------')

                    url2='https://api.vc.bilibili.com/link_draw/v1/doc/detail?'
                    for index in range(len(data3)):
                                   print ('当前动态id :', data3[index])
                                   param2={
                                     "doc_id":data3[index]
                                                   }


                                   response2 = requests.get(url=url2,params=param2,headers=headers)
                                   data4=response2.text
                                   data5=json.loads(data4)
                                   data5=jsonpath(data5,'$..pictures[*].img_src')
                                   for index2 in range(len(data5)):
                                                   print('图片链接:',data5[index2])
                                                   get_pic_by_url(dirname,data5[index2])
                                   print('```````````````````````````````````````````````````````')



    print ("Good bye!")




  
