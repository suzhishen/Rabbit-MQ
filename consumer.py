import pika
import json

from config.config_parser import rabbitmq_config

# 导入工具类
import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname('../apps/frappe')))
sys.path.append(parent_dir)
import frappe

if __name__ == "__main__":
    # """
    # 消费者, 非持久化数据
    # """
    # credentials = pika.PlainCredentials('admin', 'admin')

    # parameters = pika.ConnectionParameters(
    #     host='zxy.lsun.net',
    #     port=611,
    #     virtual_host='my_vhost',
    #     credentials=credentials
    # )

    # connection = pika.BlockingConnection(parameters)
    # channel = connection.channel()

    # channel.queue_declare(queue='my_queue')

    # def callback(ch, method, properties, body):
    #     ch.basic_ack(delivery_tag=method.delivery_tag)
    #     print(f"Received message: {body.decode()}")

    # channel.basic_consume(queue='my_queue', on_message_callback=callback, auto_ack=False)

    # print('Waiting for messages. To exit press CTRL+C')
    # channel.start_consuming()

    
    """
    消费者, 持久化数据
    """
    credentials = pika.PlainCredentials(rabbitmq_config['username'], rabbitmq_config['password'])

    parameters = pika.ConnectionParameters(
        host=rabbitmq_config['host'],
        port=rabbitmq_config['port'],
        virtual_host=rabbitmq_config['virtual_host'],
        credentials=credentials
    )

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    result = channel.queue_declare(queue='my_queue1', durable=True, exclusive=False)
    channel.exchange_declare(exchange='exchange_my_queue1', durable=True, exchange_type='direct')
    channel.queue_bind(exchange='exchange_my_queue1', queue=result.method.queue, routing_key='my_queue1')
        

    def callback(ch, method, properties, body):
        # print(body.decode())
        # return
        # raise ValueError("获取值{}".format(body.decode()))
        # 消费者收到成功消费的消息后才从消息队列删除
        # article1 = frappe.get_all("Article", filters={})
        # print(article1)
        
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(json.loads(body.decode()))
        print(f"Received message: {body.decode()}")

    channel.basic_consume(result.method.queue,callback, auto_ack=False)

    print('等待消息，退出按 CTRL+C')
    channel.start_consuming()






# from sqlalchemy import create_engine, inspect
# from sqlalchemy.ext.automap import automap_base
# from sqlalchemy.orm import Session


# if __name__ == "__main__":
#     # 创建数据库引擎，连接到 MariaDB
#     engine = create_engine('mysql+pymysql://root:root@127.0.0.1:3306/erpnext15_db')

#     # 使用 automap_base 自动映射数据库表
#     Base = automap_base()
#     Base.prepare(engine, reflect=True)

#     # 检查数据库中的表名
#     inspector = inspect(engine)
#     table_names = inspector.get_table_names()

#     # 假设你想获取名为 'your_table_name' 的表的模型
#     tabNote = Base.classes.get('tabLibrary Member')

#     if tabNote:
#         session = Session(engine)
#         # 查询表中的数据
#         results = session.query(tabNote).all()
#         print("1111111111111")
#         for item in results:
#             print(item.__dict__)
#     else:
#         print("Table not found.")