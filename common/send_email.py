import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def send(file_path):
    #第一步：连接到smtp服务器
    #创建smtp对象
    smtp=smtplib.SMTP_SSL("smtp.qq.com",465)
    #登录smtp服务器
    smtp.login("1543316854@qq.com","pxbnbhmqkbwybadc")

    #第二步：构建邮件
    #创建邮件对象
    smg=MIMEMultipart()
    #邮件文本内容
    text_msg=MIMEText("这是邮件文本内容","plain","utf8")
    # 这种是把报告内容直接放在邮件内容里
    # text_msg = MIMEText(open(file_path,"rb").read(), "html","utf8")
    #将文本内容添加到邮箱里
    smg.attach(text_msg)

    #添加附件,读取附件内容
    file_msg=MIMEApplication(open(file_path,"rb").read())
    #给附件添加信息，filename：邮件里看到的附件的标题
    file_msg.add_header('content-disposition', 'attachment', filename='report.html')
    #把附件添加到邮件里
    smg.attach(file_msg)

    #添加邮件主题
    smg["Subject"]="24期报告"
    #发件人
    smg["From"]="1543316854@qq.com"
    #收件人
    smg["To"]="1543316854@qq.com"

    #第三步：发送邮件
    smtp.send_message(smg,from_addr="1543316854@qq.com",to_addrs="1543316854@qq.com")
