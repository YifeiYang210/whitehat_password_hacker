import socket
import sys
import itertools
import string


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

        length = 1  # 初始密码长度
        while True:
            g = generate_passwords(length)

            for password in g:
                # print(password)
                # 发送消息
                sock.sendall(password.encode('utf-8'))

                # 接收服务器的响应
                reply = sock.recv(1024).decode('utf-8').strip()

                if reply == "Connection success!":
                    print(password)
                    return

                elif reply == "Too many attempts":
                    print("服务器拒绝继续尝试，退出")
                    return

            length += 1


if __name__ == "__main__":
    main()

