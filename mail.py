import imapy
import mail_config
from imapy.query_builder import Q



# 连接邮箱服务器所调用的通用函数
def mail_connect():
    box = imapy.connect(host=mail_config.HOST, username=mail_config.USERNAME, password=mail_config.PASSWORD, ssl=True)
    return box




# 获取全部的邮件列表
def count():
    # 连接邮箱服务器
    box=mail_connect()
    # names = box.folders()

    # 实例化query_builder
    q=Q()
    emails = box.folder('INBOX').emails(
        q.unseen()  #所有的未读邮件
    )

    box.logout()
    return len(emails)



# 把所有未读的邮件标记为已读
def mark_seen():
    # 连接邮箱服务器
    box=mail_connect()
    q = Q()
    emails=box.folder('INBOX').emails(
        q.unseen()  #所有的未读邮件
    )
    # 遍历，标为已读
    for email in emails:
        email.mark(['seen'])
    box.logout()
    return "success"