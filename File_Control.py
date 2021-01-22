import time


class User:
    name = None
    user_file = None

    def __init__(self, name):
        self.name = name
        self.user_file = {}

    def show_file(self):
        if len(self.user_file) == 0:
            print('没有文件')
        else:
            for i in self.user_file.keys():
                print('file:' + i)


class File:
    # 文件名字
    name = None
    # 最近修改时间
    modify = None
    # 文件大小
    size = None
    # 文件所占块数量
    block_sum = None
    # 最近访问时间
    visit = None
    # 创建时间
    create_time = None
    # 起始数据块号
    first_block = None
    # 当前最后一个数据块号
    last_block = None
    # 文件复制个数
    backup_sum = None

    def __init__(self, creat_name):
        self.create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.visit = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.modify = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.name = creat_name
        self.size = 0
        self.block_sum = 1
        self.backup_sum = 1

    def show(self):
        print('File Name: ' + self.name)
        print('Create Time: ' + self.create_time)
        print('Visit Time: ' + self.visit)
        print('Modify Time: ' + self.modify)
        print('File Size: ' + str(self.size))
        print('Block Sum: ' + str(self.block_sum))
        print('Backup Sum: ' + str(self.backup_sum))


class Message_Block:
    # 数据块编号:
    num = None
    # 该数据块写入的数据
    message = None
    # 是否被使用
    sign = None
    # 块大小
    size = None
    # 块使用大小
    used_size = None
    # 该块连接的下一个块
    next_block = None
    # 该组的内存块
    group = None
    # 该块对应的一下组块的块索引编号：
    next_group = -1

    def __init__(self, block_num):
        self.num = block_num
        self.message = ''
        self.sign = False
        self.used_size = 0
        self.size = 2
        self.next_block = -1
        self.group = []

    def set_group(self, group):
        self.group = group

    def show(self):
        print(self.num, self.message, self.sign, self.size, self.used_size, self.next_block, self.group, self.next_group)