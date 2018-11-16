import uuid
import re
import os
import urllib
import pymysql
import configparser
import logging

class MethodWarehouse():
    def __init__(self):

        self.config = configparser.ConfigParser()
        self.config.read(os.getcwd()+"/policycrawler/config.ini")
        self.host = self.config.get("database", "host")
        self.user = self.config.get("database", "user")
        self.password = self.config.get("database", "password")
        self.db = self.config.get("database", "db")
        self.logger = logging.getLogger()

    def uuid(self):
        id = uuid.uuid1()
        return id


    #图片下载
    #
    #

    def imgDownload(self,item):
        imgs=re.findall("<img.*?>",item['content'])
        picktime=item['pick_time']
        year=picktime[0:4]
        month=picktime[5:7]
        date=picktime[8:10]
        date=date
        imgpathslist=[]
        imgurllist=[]
        if len(imgs)>0:
            for img in imgs:

                imguid=uuid.uuid1()
                imguid=str(imguid).replace('-','')
                src_list=re.findall('src="(.*?)"',img)
                for src in src_list:
                    if src[0:4]=="http":
                        imgurl=src
                    elif src[0:2]=='./':
                        imgurl=item["url"].split('/')
                        imgurl.pop(-1)
                        imgurl='/'.join(imgurl)+src
                    elif src[0:3] == '../':
                        imgurl = item["url"].split('/')
                        imgurl = '/'.join(imgurl[:-2]) + src


                        #########

                    dir_name=self.read_config('imgDownloadPath','2')
                    dir_name = os.path.join(dir_name, "image")
                    dir_name=os.path.join(dir_name,year)
                    dir_name=os.path.join(dir_name,month)
                    dir_name=os.path.join(dir_name,date)
                    if not os.path.exists(dir_name):
                        os.makedirs(dir_name)

                    if len(re.findall("png",src))>0:
                        filename=os.path.join(dir_name,imguid+'.png')
                        serverimgpath1=os.path.join(imguid+'.png')
                    elif len(re.findall("PNG",src))>0:
                        filename=os.path.join(dir_name,imguid+'.PNG')
                        serverimgpath1=os.path.join(imguid+'.PNG')
                    elif len(re.findall("jpg",src))>0:
                        filename=os.path.join(dir_name,imguid+'.jpg')
                        serverimgpath1=os.path.join(imguid+'.jpg')
                    elif len(re.findall("JPG",src))>0:
                        filename=os.path.join(dir_name,imguid+'.JPG')
                        serverimgpath1=os.path.join(imguid+'.JPG')
                    elif len(re.findall("gif",src))>0:
                        filename=os.path.join(dir_name,imguid+'.gif')
                        serverimgpath1=os.path.join(imguid+'.gif')
                    elif len(re.findall("GIF",src))>0:
                        filename=os.path.join(dir_name,imguid+'.GIF')
                        serverimgpath1=os.path.join(imguid+'.GIF')
                    elif len(re.findall("jpeg",src))>0:
                        filename=os.path.join(dir_name,imguid+'.jpeg')
                        serverimgpath1=os.path.join(imguid+'.jpeg')
                    elif len(re.findall("JPEG",src))>0:
                        filename=os.path.join(dir_name,imguid+'.JPEG')
                        serverimgpath1=os.path.join(imguid+'.JPEG')

                    elif len(re.findall("bmp",src))>0:
                        filename=os.path.join(dir_name,imguid+'.bmp')
                        serverimgpath1=os.path.join(imguid+'.bmp')
                    elif len(re.findall("BMP",src))>0:
                        filename=os.path.join(dir_name,imguid+'.BMP')
                        serverimgpath1=os.path.join(imguid+'.BMP')


                    opener=urllib.request.build_opener()
                    opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36')]
                    urllib.request.install_opener(opener)

                    try:
                        urllib.request.urlretrieve(imgurl,filename)
                        item["content"]=item["content"].replace(src,filename)
                        item["img_path"]=filename
                    except:
                        filename="无效的图片路径"
                        print("无效的图片路径："+imgurl)
                        self.logger.info("无效的图片路径：%s",imgurl)
                    imgpathslist.append(serverimgpath1)
                return item
        else:
            return item

#下面两个方法是将body中的jpg或png地址替换为图片在本地的地址
    def rep_body_img(self,bodytext):

        pat=re.compile("\s{1}src=\".*?\"")

        return pat.sub(self.replace,bodytext)


    def replace(self,match):
         #print("l:"+str(self.l))
         path=self.imgpathslist[self.l]
         rep=' src="'+path.split('\\')[-1]+'"'
         self.l=self.l+1
         return  rep
    #删除body中所有读不到图片的标签
    def delete_body_img(self,text):
        replacedStr = re.sub("<[iI][mM][gG].*?无效的图片路径.*?>", "", text)

        return replacedStr


    #读数据库中的配置文件

    def read_config(self,basic_type,basic_value):
        db = pymysql.connect(host=self.host, user=self.user,
                             password=self.password, db=self.db, port=3306)

        cur = db.cursor()

        sql = "select basic_name from sys_basic_data where basic_type= "+"'"+"%s"+"'"+" and basic_value="+"'"+"%s"+"'"
        try:
            cur.execute(sql % (basic_type,basic_value))
            results = cur.fetchall()
            return results[0][0]
        except Exception:
            raise Exception
        finally:
            db.close()

