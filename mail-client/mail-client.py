import smtplib
import imaplib
from email.mime.text import MIMEText
from email.header import Header
import email
import getpass


class mail_client:
    def login(self):
        # self.username = input("请输入帐号:")
        # self.password = getpass.getpass()
        self.username = "2424311278@qq.com"
        self.password = "lqwjvmepqtiwecgb"
        self.path = "downloads/"

    def start(self):
        self.login()
        while True:
            x = input(
                """         ------------------
        ----------------------
        --                  --
        --    1-发送邮件    --
        --    2-查看邮件    --
        --    q-退出程序    --
        --                  --
请输入指令："""
            )
            if x == "1":
                self.sendMail()
            elif x == "2":
                self.selectMail()
            elif x == "q":
                print("程序已结束")
                break
            else:
                print("请选择正确的指令！\n")
                continue

    # 发送邮件
    def sendMail(self):
        print("-----邮件内容请编辑本程序同目录下 mail.txt文件-----")
        receiver = input("收件人:")
        subject = input("主题:")
        with open("mail.txt", "r") as f:
            content = f.read()
        msg = MIMEText(content, "plain", "utf-8")

        msg["Subject"] = subject
        msg["From"] = self.username
        msg["To"] = receiver

        try:
            client = smtplib.SMTP_SSL("smtp.qq.com", smtplib.SMTP_SSL_PORT)
            print("连接到 smtp 服务器成功")
            client.login(self.username, self.password)
            print("登录成功")
            client.sendmail(self.username, receiver, msg.as_string())
            print("发送成功")
        except smtplib.SMTPException as e:
            print("发送失败: %s" % (e.strerror))
        finally:
            client.quit()

    # 接收邮件
    def selectMail(self):
        M = imaplib.IMAP4_SSL("imap.qq.com")
        M.login(self.username, self.password)
        # 选择邮箱
        M.select(mailbox="INBOX")
        # 查找所有邮件
        typ, data = M.search(None, "ALL")
        ynum = 1
        for num in data[0].split():
            typ, data = M.fetch(num, "(RFC822)")
            msg = email.message_from_string(data[0][1].decode())
            subject = msg.get("subject")
            sender = msg.get("from")
            receiver = msg.get("to")
            text_a = email.header.decode_header(subject)
            text_b = email.header.decode_header(sender)
            # text_c = email.header.decode_header(receiver)

            if text_a[0]:
                detail_a = tuple2str(text_a[0])

            detail_b = ""
            for i in range(len(text_b)):
                detail_b = detail_b + tuple2str(text_b[i])

            # detail_c = ""
            # for i in range(len(text_c)):
            # detail_c = detail_c + __tuple2str(text_c[i])
            print("{:<8}{:^30}{}".format(ynum, detail_b, detail_a))
            ynum += 1

        # 查看某一个邮件
        znum = input("请输入要查看的邮件序号：")
        typ, data = M.fetch(znum, "(RFC822)")
        msg = email.message_from_string(data[0][1].decode())
        subject = msg.get("subject")
        sender = msg.get("from")
        receiver = msg.get("to")
        text_a = email.header.decode_header(subject)
        text_b = email.header.decode_header(sender)
        text_c = email.header.decode_header(receiver)
        if text_a[0]:
            detail_a = tuple2str(text_a[0])
        detail_b = ""
        for i in range(len(text_b)):
            detail_b = detail_b + tuple2str(text_b[i])
        detail_c = ""
        for i in range(len(text_c)):
            detail_c = detail_c + tuple2str(text_c[i])
        print("主题：%s\n发件人：%s\n收件人：%s" % (detail_a, detail_b, detail_c))

        # 通过walk 遍历
        for part in msg.walk():
            if not part.is_multipart():
                content_type = part.get_content_type()
                name = part.get_filename()
                if name:
                    trans_name = email.header.decode_header(name)
                    if trans_name[0][1]:
                        file_name = trans_name[0][0].decode(trans_name[0][1])
                    else:
                        file_name = trans_name[0][0]
                    print("开始下载附件:", file_name)
                    # 解码存储数据
                    attach_data = part.get_payload(decode=True)
                    try:
                        f = open(ROOT_DIR + file_name, "wb")
                    except Exception as e:
                        print(e)
                        f = open(ROOT_DIR + "tmp", "wb")
                    f.write(attach_data)
                    f.close()
                    print("附件下载成功:", file_name)
                else:
                    # 文本内容
                    txt = part.get_payload(decode=True)
                    if txt == None:
                        print("None")
                        continue
                    if content_type == "text/html":
                        print("文件格式为html, 请使用浏览器查看文件")
                        htmlfile = open("./html_content.html", "w")
                        try:
                            txt = txt.decode()
                        except UnicodeDecodeError:
                            txt = txt.decode("gbk")
                        htmlfile.write(txt)
                        htmlfile.close()
                    elif content_type == "text/plain":
                        print("邮件正文:")
                        try:
                            txt = txt.decode()
                        except UnicodeDecodeError:
                            txt = txt.decode("gbk")
                        print(txt)
        M.close()
        M.logout()


# 将元组（内容，编码）按编码进行解码
def tuple2str(tuple_):
    if tuple_[1]:
        out_str = tuple_[0].decode(tuple_[1])
    else:
        if isinstance(tuple_[0], bytes):
            out_str = tuple_[0].decode("gbk")
        else:
            out_str = tuple_[0]
    return out_str


if __name__ == "__main__":
    client = mail_client()
    client.start()
