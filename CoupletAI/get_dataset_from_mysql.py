# 获取数据集
import pymysql
import os
import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

couplet_path = '/root/Couplet/couplet/temp/'

logger.info(" get train data from Mysql......")
logger.info(" get connected with Mysql...")
db = pymysql.connect(host='139.9.113.51', port=3306, user='chatbot', password='chatbot', db='chatbot', charset='utf8')
cursor = db.cursor()

couplet_ups = list()
couplet_downs = list()

cursor.execute('SELECT * from coupletchatbot_corpus')
fetchall = cursor.fetchall()

for value in fetchall:
    couplet_ups.append(' '.join([i for i in value[5]])+'\n')
    couplet_downs.append(' '.join([i for i in value[6]])+'\n')

cursor.close()
db.close()

with open(os.path.join(couplet_path, 'in.txt'), 'w') as f:
    f.writelines(couplet_ups)
with open(os.path.join(couplet_path, 'out.txt'), 'w') as f:
    f.writelines(couplet_downs)

logger.info(" get train data from Mysql.")
