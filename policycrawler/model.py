from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime,Text,TIMESTAMP
from sqlalchemy.orm import sessionmaker
import configparser
import os

from policycrawler.MethodWarehouse import MethodWarehouse



config=configparser.ConfigParser()
config.read(os.getcwd()+"/policycrawler/config.ini")

user=config.get("database","user")
password=config.get("database","password")
host=config.get("database","host")
db=config.get("database","db")
engine = create_engine('mysql+pymysql://'+user+':'+password+'@'+host+'/'+db+'?charset=utf8')

Base = declarative_base()

class Policy_Table_Url(Base):
    __tablename__ = 'crawler_demo_mid'
    id = Column(Integer, primary_key=True)
    title= Column(String(255))
    url = Column(String(255))
    state=Column(Integer,default=0)

    def sele_state(self):
        try:
            DBSession = sessionmaker(bind=engine)
            session = DBSession()
            user = session.query(Policy_Table_Url).filter(Policy_Table_Url.state == "0").all()
            return user
        except:
            print("提取采集状态出错")

    def sele_by_url(self, url):
        try:
            DBSession = sessionmaker(bind=engine)
            session = DBSession()
            user = session.query(Policy_Table_Url).filter(Policy_Table_Url.url == url, Policy_Table_Url.state==1).first()

            session.close()
            return user
        except:
            print(url+"网站采集异常")

class Policy_Table(Base):
    __tablename__ = 'crawler_demo_last'
    id = Column(String(32), primary_key=True)
    current_task_id=Column(String(255))
    title = Column(String(255))
    url = Column(String(255))
    content = Column(Text)
    pub_time = Column(String(255))
    pick_time = Column(String(255)) 
    img_path=Column(String(255))
    attachment_path=Column(String(255))
    front_name=Column(String(50))
    front_id=Column(String(32))
    modified=Column(TIMESTAMP(3),nullable=False)
    state = Column(Integer, default=0)


#任务统计表
class Policy_statistics(Base):
    __tablename__='busi_tasks_flow_statistics'
    id=Column(String(32), primary_key=True)
    task_id=Column(Integer)
    start_time=Column(DateTime)
    stop_time=Column(DateTime)
    #写入字节数total_dat
    data_total=Column(Integer)
    data_count=Column(Integer)
    task_state=Column(Integer)
    remark=Column(String(250))
    created_by=Column(String(50))
    create_time=Column(String(23))
    updated_by=Column(String(50))
    update_time=Column(String(23))
    is_deleted=Column(String(1))

# if __name__ == '__main__':
#     Base.metadata.create_all(engine)
    # DBSession = sessionmaker(bind=engine)
    # session = DBSession()
    # policy_statistics =session.query(Policy_statistics).filter_by(id="40288aa864b63e240164b63eecf20000").update({Policy_statistics.data_total:22222})
    # #policy_statistics =session.query(Policy_statistics).filter_by(id="40288aa864b63e240164b63eecf20000").update({Policy_statistics.data_total:22234})
    # session.commit()
    # # user = session.query(Policy_Table_Url).filter(Policy_Table_Url.url == "333").first()
    # # print(user)