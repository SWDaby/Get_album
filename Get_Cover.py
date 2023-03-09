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
    name=name[0]+'-cover'
    
    return name


if __name__ == '__main__':

    # 指定ajax-get请求的url（通过抓包进行获取）
    url = 'https://api.bilibili.com/x/space/wbi/arc/search?'
    headers = {'User-Agent': UserAgent().random,
               "cookie":getCookie()
                    }

    id_number=input("请输入up主页号:")
    page=input("请输入要抓取的页数:")
    dirname= get_dir_name(id_number, headers)
    print("将生成文件在："+str(dirname))

    # 封装ajax的get请求携带的参数(从抓包工具中获取) 封装到字典
    for i in range(1,int(page)+1):
                    param = {
                        'mid':id_number,
                        'ps':'30',
                        'pn': i,

                    }

    # 定制请求头信息，相关的头信息必须封装在字典结构中


    # 发起ajax的get请求还是用get方法
                    response = requests.get(url=url,params=param,headers=headers)

    # 获取响应内容：响应内容为json字符串

                    data = json.loads(response.text)

                    #print(data)
                    bvid=jsonpath(data, '$..bvid')
                    pic=jsonpath(data, '$..pic')
                    Targetdata=[bvid, pic]

                    #print(Targetdata)
                    print('---------------------------------------------')


                    for index in range(len(Targetdata[1])):
                        print ('当前视频id :', Targetdata[0][index])
                        print('封面链接:', Targetdata[1][index])
                        get_pic_by_url(dirname, Targetdata[1][index])
                        print('```````````````````````````````````````````````````````')



    print ("Good bye!")



  
