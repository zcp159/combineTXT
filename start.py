import re
import os
import fnmatch
import time
import configparser
import math


# --------------------配置文件-------------------------
# --------------------配置文件-------------------------
# --------------------配置文件-------------------------

# 导入配置文件章节,返回选项内容列表
def xuanxiang_read(cf, zhangjie):
    list = []
    # 遍历选项
    for k in cf.options(zhangjie):
        list.append(cf.get(zhangjie, k))
    return list


# 返回配置文件元组
def conf_read():
    list = []
    cf = configparser.ConfigParser(allow_no_value=False)
    cf.read("conf.ini")
    if cf.has_section('TXT文件夹路径') and cf.has_section('需要的关键字') and cf.has_section('文件大小限制,单位KB'):
        # 遍历章节
        for i in cf.sections():
            list.append(xuanxiang_read(cf, i))
    else:
        exit()
    return list


# --------------------找出符合后缀名及大小的文件-------------------------
# --------------------找出符合后缀名及大小的文件-------------------------
# --------------------找出符合后缀名及大小的文件-------------------------

# 获取目录及规则，返回生成器，生成器内容为
# 目录下所有满足规则的文件的绝对路径
def is_special_file(root, guizes=["*.txt"], liwaimulus=[]):
    # 遍历根目录
    for dangqianmulu, mulus, files in os.walk(os.path.abspath(root)):
        # 遍历返回的文件名
        for file in files:
            # 判定大小是否负责
            if size_fuhe(os.path.join(os.path.abspath(dangqianmulu), file)):
                # 判定文件名是否满足需要搜索的格式,如果符合则绝对路径放入生成器
                if is_file_math(file, guizes):
                    yield os.path.join(os.path.abspath(dangqianmulu), file)
                else:
                    print("后缀名不符:{}".format(os.path.splitext(os.path.basename(file))[0]))
            else:
                print("大小不合规:{}".format(os.path.splitext(os.path.basename(file))[0]))
        # 排除指定目录名的目录
        for d in liwaimulus:
            if d in mulus:
                mulus.remove(d)


# 传入文件绝对路径和需要多少KB以下，返回是否小于多少KB
def size_fuhe(file):
    filesize = os.path.getsize(file) / 1024
    # print(filesize)
    if min_size < filesize < max_size:
        return True
    return False


# 确定文内容件是否符合规则
def is_file_math(file, guizes):
    # 遍历规则，如果文件符合任何一条规则则返回真
    for guize in guizes:
        if fnmatch.fnmatch(file, guize):
            return True
    # 遍历完成后，返回假
    # 如果前面已经返回真了，由于只能返回一个值，则这个返回假就没用了
    return False


# --------------------找出符合内容关键字的文件-------------------------
# --------------------找出符合内容关键字的文件-------------------------
# --------------------找出符合内容关键字的文件-------------------------

# 传入文件绝对路径，满足需要规则且不满足排除规则，返回True
def file_OK(file, guize, guize_not):
    # 文件是否匹配需要的关键字，没匹配上返回Flase
    if file_pipei(file, guize, ">=",yuzhi):
        # 如果排除规则里有内容，则需要匹配，全部未匹配上，返回True，匹配上了返回False
        # 如果没内容，则直接返回True
        if guize_not:
            # 排除的关键字
            if file_pipei(file, guize_not, "<",yuzhi_pingbi):
                return True
            else:
                print("存在屏蔽字:{}".format(os.path.splitext(os.path.basename(wenjian))[0]))
                return False
        else:
            return True
    else:
        print("缺少关键字:{}".format(os.path.splitext(os.path.basename(wenjian))[0]))
        return False


# 传入文件绝对路径和需要规则列表，如果大于等于阈值，则返回True
def file_pipei(file, guize, fuhao,yuzhi):
    # 满足规则的次数
    count_manzu = 0
    # 文件大小
    filesize = os.path.getsize(file) / 1024
    # 读取文件对象
    for i in split_file(file):
        # 遍历配置文件选项
        l = -1
        for j in guize:
            l += 1
            # 计算需要的阈值
            count_xuyao = int(filesize / 50 * int(yuzhi[l]))
            # print("count_xuyao=",count_xuyao)
            # 配置文件选项内容按逗号分隔，生成列表
            guanjianzilist = j.split(",")
            # 遍历配置文件选项内容列表
            count_1 = 0
            for k in range(len(guanjianzilist)):
                # 计算文件中有多少文件选项内容列表中分词
                count_1 += guanjianci_count(i, guanjianzilist[k])
            # print("count_1=",count_1)
            if fuhao == ">=":
                if count_1 > count_xuyao:
                    count_manzu += 1
            # 屏蔽设置阈值0的，count_xuyao这里算到也是0，所以用<=
            elif fuhao == "<":
                if count_1 <= count_xuyao:
                    count_manzu += 1
        if not count_manzu == len(guize):
            return False
        return True


# 传入文件绝对路径和规则列表，计算文件中有多少关键字
def guanjianci_count(fileduixiang, fenguize):
    k = 0
    k += fileduixiang.count(fenguize)
    return k


# 传入字符串，正则匹配确认字符串中是否有关键字，有则返回True
def pipei(ziduan, guize):
    # 遍历正则,任何一个未匹配上返回False
    for i in guize:
        if not re.search(i, ziduan):
            return False
    return True


# --------------------找出即将重复写入文件-------------------------
# 传入字符串1和字符串2，如果1在2内重复，则返回True
def chongfujiancha(file_read, file_write):
    global chongfu_count
    chongfucanshu = 10
    if file_read[500:500 + chongfucanshu] in file_write:
        if file_read[300:300 + chongfucanshu] in file_write:
            # if file_read[400:400 + chongfucanshu] in file_write:
            chongfu_count += 1
            return True
    return False


# --------------------基本函数-------------------------
# --------------------基本函数-------------------------
# --------------------基本函数-------------------------
# 传入文件绝对路径，返回文件对象迭代器
def split_file(file):
    try:
        with open(file, encoding="gb18030")as f:
            yield f.read()
    except UnicodeDecodeError:
        print("编码不合规:{}".format(os.path.splitext(os.path.basename(file))[0]))


# 读取配置文件
peizhiwenjian = conf_read()
mulu = peizhiwenjian[0][0]
guanjianzi = peizhiwenjian[1]
guanjianzi_not = peizhiwenjian[2]
min_size = int(peizhiwenjian[3][0])
max_size = int(peizhiwenjian[3][1])
yuzhi = peizhiwenjian[4]
yuzhi_pingbi = peizhiwenjian[5]

# 数据统计
all_file = 0  # 一共有多少txt的文件
pipeidao_file = 0  # 一共有多少关键字文件
chongfu_count = 0  # 一共有多少重复文件

# 先找出所有txt文件，大小也要符合
wenjianlist = is_special_file(mulu, guizes=["*txt"])
# 遍历所有txt文件
with open("#合并.txt", "wb+") as w1:
    for wenjian in wenjianlist:
        # print(wenjian)
        all_file += 1
        # 判定文件内容是否符合关键字规则
        if file_OK(wenjian, guanjianzi, guanjianzi_not):
            # 判定准备录入的txt在合并txt内是否重复
            # 先打开匹配上的文件文件
            with open(wenjian, "rb") as r:
                # 读取内容
                neirong = r.read()
                # 合并大文件头开始查找，准备新写入的文件是否重复
                w1.seek(0, 0)
                if not chongfujiancha(neirong, w1.read()):
                    w1.seek(0, 2)
                    pipeidao_file += 1
                    # 准备新写入的文件先写入标题
                    w1.write(("第{}章 666 ".format(pipeidao_file) + os.path.splitext(os.path.basename(wenjian))[
                        0] + "\n\n").encode('gb18030'))
                    # 准备新写入的文件再写入内容
                    w1.write(neirong)
                    # 不同文件之间空10行
                    print("合并新文件:{}".format(os.path.splitext(os.path.basename(wenjian))[0]))
                    w1.write(
                        "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n".encode('gb18030'))
                else:
                    print("重复旧文件:{}".format(os.path.splitext(os.path.basename(wenjian))[0]))
print("\n一共{}个文件,匹配到{}个需要文件,{}个重复文件".format(all_file, pipeidao_file, chongfu_count))
time.sleep(999)
