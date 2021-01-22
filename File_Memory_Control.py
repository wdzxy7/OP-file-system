import File_Control as Control
import time
import copy
import re


# 创建数据块，一个块存放8长度数据
def creat_memory():
    for i in range(1000):
        block = Control.Message_Block(i)
        memory.append(block)


# 获取栈中空闲内存块数量
def get_control_stack_free_size():
    return block_control_stack[0]


# 块进行分组
def grouping_memory():
    group_member = []
    count = 0
    for number in range(len(memory)):
        group_member.append(memory[number].num)
        count += 1
        # 100个一组
        if count == stack_size:
            # 索引块存入改组索引
            memory[number].set_group(group_member)
            memory[number].group = copy.copy(group_member)
            memory[number].group.reverse()
            memory_group_leader.append(memory[number].num)
            group_member.clear()
            count = 0


def get_next_block_group(last_block):
    next_num = last_block.next_group
    next_block = memory[next_num]
    next_group = next_block.group
    for block in next_group:
        block_control_stack.append(block)
    block_control_stack[0] = stack_size
    last_block.group.clear()
    del memory_group_leader[0]


def write_last_block(last_block, write_message, surplus_size):
    text = write_message
    textArr = re.findall('.{' + str(surplus_size) + '}', text)
    textArr.append(text[(len(textArr) * surplus_size):])
    last_message = textArr[0]
    del textArr[0]
    write_message = ''.join(textArr)
    last_block.message = last_block.message + last_message
    last_block.used_size = last_block.size
    textArr = re.findall('.{' + str(last_block.size) + '}', write_message)
    textArr.append(write_message[(len(textArr) * last_block.size):])
    if len(textArr[len(textArr) - 1]) == 0:
        del textArr[len(textArr) - 1]
    return textArr


def get_block():
    block_number = block_control_stack.pop()
    try:
        remove_index = memory[block_control_stack[1]].group.index(block_number)
        del memory[block_control_stack[1]].group[remove_index]
    except:
        remove_index = memory[block_number].group.index(block_number)
        del memory[block_number].group[remove_index]
    block = memory[block_number]
    return block


def get_file():
    user_name = input('输入用户名\n')
    if user_name not in user_dict.keys():
        print('没有该用户\n')
        return None
    user = user_dict[user_name]
    user_file_dict = user.user_file
    file_name = input('输入文件名\n')
    try:
        file = user_file_dict[file_name]
    except:
        print('没有该文件')
        return None
    return file


def write_block_message(message, front_block, file):
    if block_control_stack[0] > 1:
        block = get_block()
        block.sign = True
        block.message = message
        front_block.next_block = block.num
        if len(message) < block.size:
            block.used_size = len(message)
        else:
            block.used_size = block.size
        file.last_block = block.num
        block_control_stack[0] = block_control_stack[0] - 1
    else:
        block = get_block()
        get_next_block_group(block)
        block.sign = True
        block.message = message
        front_block.next_block = block.num
        if len(message) < block.size:
            block.used_size = len(message)
        else:
            block.used_size = block.size
        file.last_block = block.num
    return block


# 释放内存时修改组
def change_group_leader(block_num):
    # 栈还没有满
    if block_control_stack[0] < stack_size:
        block_control_stack.append(block_num)
        leader = block_control_stack[1]
        leader_block = memory[leader]
        leader_block.group.append(block_num)
        block_control_stack[0] += 1
    # 栈满了
    else:
        block = memory[block_num]
        leader = block_control_stack[1]
        while block_control_stack[0] != 0:
            block_control_stack.pop()
            block_control_stack[0] = block_control_stack[0] - 1
        block_control_stack.append(block_num)
        block.next_group = leader
        block.group.append(block_num)
        block_control_stack[0] = 1
        memory_group_leader.insert(0, block_num)


def show_each_block(file):
    block_num = file.first_block
    file_memory = {}
    # 把文件的所有内存块读入
    while block_num != -1:
        block = memory[block_num]
        file_memory[block_num] = block
        block_num = block.next_block
    for key in file_memory.keys():
        print('Block Number:{0}   Block Message:{1}'.format(key, file_memory[key].message))
    return file_memory


def create_file():
    user_name = input('输入用户名\n')
    if user_name not in user_dict.keys():
        print('没有该用户\n')
        return None
    user = user_dict[user_name]
    file_name = input('输入新建文件名字\n')
    if file_name in user.user_file:
        print('文件已存在创建失败')
        return None
    elif len(file_name) == 0:
        print('文件名不能为空')
        return None
    file = Control.File(file_name)
    # 弹出一个块给他存放信息
    # 可用块大于一个
    if block_control_stack[0] > 1:
        block = get_block()
        block.sign = True
        file.first_block = block.num
        file.last_block = block.num
        block_control_stack[0] = block_control_stack[0] - 1
        user.user_file[file_name] = file
    # 可用块只剩最后一个进行切换下一组块
    else:
        block = get_block()
        get_next_block_group(block)
        block.sign = True
        file.first_block = block.num
        file.last_block = block.num
        block_control_stack[0] = stack_size
        user.user_file[file_name] = file


def read_file():
    file = get_file()
    if file is None:
        return None
    block_num = file.first_block
    message = ''
    while block_num != -1:
        block = memory[block_num]
        message = message + block.message
        block_num = block.next_block
    file.visit = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(file.show())
    print('File Message:\n' + message)
    print('Block Detail Message:')
    show_each_block(file)


def write_file():
    file = get_file()
    if file is None:
        return None
    block_num = file.last_block
    last_block = memory[block_num]
    block_size = last_block.size
    surplus_size = block_size - last_block.used_size
    write_message = input('输入写入文件的数据\n')
    if len(write_message) > surplus_size:
        surplus_message = write_last_block(last_block, write_message, surplus_size)
        front_block = last_block
        for message in surplus_message:
            front_block = write_block_message(message, front_block, file)
            file.block_sum += 1
        file.modify = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    else:
        last_block.message = last_block.message + write_message
        file.modify = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        file.block_sum += 1
    file.size += len(write_message)


def freely_write():
    file = get_file()
    if file is None:
        return None
    file_memory = show_each_block(file)
    op = input('选择修改类型:\n'
               '1.change\n'
               '2.insert\n')
    if op == '1':
        modify_num = int(input('输入修改的盘块号\n'))
        modify_message = input('输入修改后的数据\n')
        modify_file(file, modify_num, modify_message)
        file.modify = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    else:
        insert_num = int(input('输入插入数据的盘块位置\n'))
        insert_message = input('输入插入的数据\n')
        insert_file(file, insert_num, insert_message)
        file.modify = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def freely_write_block(message, front_block):
    if block_control_stack[0] > 1:
        block = get_block()
        block.sign = True
        block.message = message
        front_block.next_block = block.num
        if len(message) < block.size:
            block.used_size = len(message)
        else:
            block.used_size = block.size
        block_control_stack[0] = block_control_stack[0] - 1
    else:
        block = get_block()
        get_next_block_group(block)
        block.sign = True
        block.message = message
        front_block.next_block = block.num
        if len(message) < block.size:
            block.used_size = len(message)
        else:
            block.used_size = block.size
    return block


def modify_file(file, block_num, message):
    block = memory[block_num]
    if len(message) > block.size:
        textArr = re.findall('.{' + str(block.size) + '}', message)
        textArr.append(message[(len(textArr) * block.size):])
        block.message = textArr[0]
        del textArr[0]
        message = ''.join(textArr)
        # 改为插入方式
        insert_file(file, block_num, message)
    else:
        block.message = message


def insert_file(file, block_num, message):
    file.size = file.size + len(message)
    block = memory[block_num]
    last = block.next_block
    textArr = re.findall('.{' + str(block.size) + '}', message)
    textArr.append(message[(len(textArr) * block.size):])
    front_block = block
    for mess in textArr:
        front_block = freely_write_block(mess, front_block)
        file.block_sum += 1
    front_block.next_block = last


def drop_file():
    user_name = input('输入用户名\n')
    if user_name not in user_dict.keys():
        print('没有该用户\n')
        return None
    user = user_dict[user_name]
    user_file_dict = user.user_file
    file_name = input('输入文件名\n')
    try:
        file = user_file_dict[file_name]
    except:
        print('没有该文件')
        return None
    if file.backup_sum == 1:
        block_num = file.first_block
        while block_num != -1:
            block = memory[block_num]
            block.used_size = 0
            block.message = ''
            block.sign = False
            change_group_leader(block_num)
            block_num = block.next_block
            block.next_block = -1
            file.block_sum -= 1
    else:
        file.backup_sum -= 1
    del user_file_dict[file_name]


def freely_drop():
    file = get_file()
    if file is None:
        return None
    file_memory = show_each_block(file)
    indexs = list(file_memory.keys())
    drop = input('输入要删除的块:\n')
    drop = drop.split(' ')
    for number in drop:
        ind = indexs.index(int(number))
        if int(number) == file.first_block:
            first = memory[int(number)]
            # 修改文件信息
            file.first_block = first.next_block
            file.block_sum -= 1
            file.size = file.size - first.used_size
            # 处理内存块
            first.used_size = 0
            first.message = ''
            first.sign = False
            change_group_leader(first.num)
        elif int(number) == file.last_block:
            last = memory[int(number)]
            # 修改文件信息
            front = memory[indexs[ind-1]]
            file.last_block = front.num
            file.block_sum -= 1
            file.size = file.size - last.used_size
            # 处理内存块
            last.used_size = 0
            last.message = ''
            last.sign = False
            change_group_leader(last.num)
        else:
            # 获取该块的前后两个块
            this = memory[indexs[ind]]
            front = memory[indexs[ind - 1]]
            back = memory[indexs[ind + 1]]
            # 修改文件信息
            file.block_sum -= 1
            file.size = file.size - this.used_size
            # 处理内存块
            this.used_size = 0
            this.message = ''
            this.sign = False
            front.next_block = back.num
            change_group_leader(this.num)


def creat_backup_file():
    user_name = input('输入用户名\n')
    if user_name not in user_dict.keys():
        print('没有该用户\n')
        return None
    user = user_dict[user_name]
    user_file_dict = user.user_file
    root_user_name = input('输入源文件用户名\n')
    if root_user_name not in user_dict.keys():
        print('没有该用户\n')
        return None
    root_user = user_dict[root_user_name]
    root_dict = root_user.user_file
    file_name = input('输入文件名\n')
    try:
        file = root_dict[file_name]
    except:
        print('没有该文件')
        return None
    user_file_dict[file_name] = file
    file.backup_sum += 1


def create_user():
    user_name = input('输入用户名称\n')
    user = Control.User(user_name)
    user_dict[user_name] = user


def show_users():
    if len(user_dict.keys()) == 0:
        print('没有用户')
    print(user_dict.keys())


def show_files():
    user_name = input('输入用户名\n')
    user = user_dict[user_name]
    user.show_file()


def show_stack():
    print('Group List: ', memory_group_leader)
    print('Block Control Stack:', block_control_stack)


if __name__ == '__main__':
    # 存放用户
    user_dict = {}
    stack_size = 3
    # 内存
    memory = []
    creat_memory()
    block_control_stack = [stack_size]
    # 存放每个组组员的那个块的编号
    memory_group_leader = []
    grouping_memory()
    for num in range(len(memory_group_leader)):
        try:
            memory[memory_group_leader[num]].next_group = memory[memory_group_leader[num + 1]].num
        except:
            memory[memory_group_leader[num]].next_group = 0
    # 初始化栈
    for member in memory[memory_group_leader[0]].group:
        block_control_stack.append(member)
    while True:
        print('输入操作:\n'
              '1.create file\n'
              '2.read file\n'
              '3.write file\n'
              '4.freely write\n'
              '5.drop file\n'
              '6.freely drop\n'
              '7.creat backup file\n'
              '8.create user\n'
              '9.show users\n'
              '10.show user`s files\n'
              '11.show stack\n')
        op = input('输入操作编号\n')
        if op == '1':
            create_file()
        elif op == '2':
            read_file()
        elif op == '3':
            write_file()
        elif op == '4':
            freely_write()
        elif op == '5':
            drop_file()
        elif op == '6':
            freely_drop()
        elif op == '7':
            creat_backup_file()
        elif op == '8':
            create_user()
        elif op == '9':
            show_users()
        elif op == '10':
            show_files()
        elif op == '11':
            show_stack()
        else:
            print('输入操作有误')
