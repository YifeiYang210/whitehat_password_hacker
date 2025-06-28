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
import socket
import sys

PASSWORD = "qwerty"


def main():
    if len(sys.argv) != 4:
        print("Usage: python hack.py <IP address> <port> <message>")
        return

    ip_address = sys.argv[1]
    port = int(sys.argv[2])
    message = sys.argv[3]

    # 创建一个新的套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # 使用套接字连接到主机和端口
        sock.connect((ip_address, port))

        # 发送消息
        sock.sendall(message.encode('utf-8'))

        # 接收服务器的响应
        response = sock.recv(1024).decode('utf-8')

        if response.strip() == PASSWORD:
            print("Connection Success!")
        else:
            print("Wrong password!")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # 关闭套接字
        sock.close()

if __name__ == "__main__":
    main()

