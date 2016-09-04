import imapy
import mail_config
from imapy.query_builder import Q



# 连接邮箱服务器所调用的通用函数
def mail_connect():
    box = imapy.connect(host=mail_config.HOST, username=mail_config.USERNAME, password=mail_config.PASSWORD, ssl=True)
    return box




# 获取全部的邮件列表
def list_all(request):
    # 连接邮箱服务器
    box=mail_connect()
    # names = box.folders()
    # logger.info(names)

    # 实例化query_builder
    q=Q()
    emails = box.folder('INBOX').emails(
        q.unseen()  #所有的未读邮件
    )

    # logger.info(emails)
    for email in emails:
        logger.info(email['from'])
        logger.info(email['subject'])
        email.mark(['seen'])

    box.logout()
    return HttpResponse('success', content_type="text/plain")



# 把所有未读的邮件标记为已读
def mark_seen(request):
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
    return HttpResponse('success', content_type="text/plain")