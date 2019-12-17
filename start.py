import re
import os
import fnmatch
import time
import configparser

chongfu_count = 0


# 导入章节,返回选项内容列表
def xuanxiang_read(cf, zhangjie):
    list = []
    # 遍历选项
    for k in cf.options(zhangjie):
        list.append(cf.get(zhangjie, k))
    return list


# 返回元组
def conf_read():
    list = []
    cf = configparser.ConfigParser(allow_no_value=False)
    cf.read("conf.ini")
    if cf.has_section('TXT文件夹路径') and cf.has_section('需要的关键字') and cf.has_section('屏蔽的关键字'):
        # 遍历章节
        for i in cf.sections():
            list.append(xuanxiang_read(cf, i))
    return list


# 传入文件绝对路径，返回迭代器
def split_file(file):
    try:
        # with open(file)as f:
        with open(file, encoding="gb18030")as f:
            yield f.read()
    except:
        pass


# 传入字符串，正则匹配确认字符串中是否有关键字，有则返回True
def pipei(ziduan, guize):
    # 遍历正则,任何一个未匹配上返回False
    for i in guize:
        if not re.search(i, ziduan):
            return False
    return True


# 传入字符串1和字符串2，如果重复返回True
def chongfujiancha(file_read, file_write):
    global chongfu_count
    chongfucanshu = 10
    if file_read[500:500 + chongfucanshu] in file_write:
        if file_read[300:300 + chongfucanshu] in file_write:
            if file_read[400:400 + chongfucanshu] in file_write:
                chongfu_count += 1
                return True
    return False


# 传入绝对路径，正则匹配确认文件中是否有关键字，有则返回True
def file_pipei(file, guize):
    for i in split_file(file):
        if pipei(i, guize):
            return True
    # 一个文件整个遍历完，没有匹配上，则返回Flase
    return False


# 传入绝对路径，满足规则，且不满足规则not，返回True
def file_OK(file, guize, guize_not):
    # 文件是否匹配需要的关键字，没匹配上返回Flase
    if file_pipei(file, guize):
        # 如果排除规则里有内容，则需要匹配，全部未匹配上，返回True，匹配上了返回False
        # 如果没内容，则直接返回True
        if guize_not:
            # 规则匹配上，则返回True
            if not file_pipei(file, guize_not):
                return True
            else:
                return False
        else:
            return True
    else:
        return False


# 确定文件是否符合规则
def is_file_math(file, guizes):
    # 遍历规则，如果文件符合任何一条规则则返回真
    for guize in guizes:
        if fnmatch.fnmatch(file, guize):
            return True
    # 遍历完成后，返回假
    # 如果前面已经返回真了，由于只能返回一个值，则这个返回假就没用了
    return False


# 获取目录及规则，返回生成器，生成器内容为
# 目录下所有满足规则的文件的绝对路径
def is_special_file(root, guizes=["*"], liwaimulus=[]):
    # 遍历根目录
    for dangqianmulu, mulus, files in os.walk(os.path.abspath(root)):
        # 遍历返回的文件名
        for file in files:
            # 判定文件名是否满足需要搜索的格式,如果符合则绝对路径放入生成器
            if is_file_math(file, guizes):
                yield os.path.join(os.path.abspath(dangqianmulu), file)
        for d in liwaimulus:
            if d in mulus:
                mulus.remove(d)


def main():
    peizhiwenjian = conf_read()
    mulu = peizhiwenjian[0][0]
    guanjianzi = peizhiwenjian[1]
    guanjianzi_not = peizhiwenjian[2]

    all_file = 0  # 一共有多少符合txt的文件
    pipeidao_file = 0  # 一共有多少关键字文件
    # 1:输出匹配上的文件
    # 2:输出匹配上的文件并合并
    gongneng = 2

    wenjianlist = is_special_file(mulu)
    with open("#合并.txt", "wb+") as w1:
        for wenjian in wenjianlist:
            all_file += 1
            if file_OK(wenjian, guanjianzi, guanjianzi_not):
                if gongneng == 2:
                    # 判定准备录入的txt在合并txt内是否重复
                    # 打开匹配上的文件文件
                    with open(wenjian, "rb") as r:
                        # 读取内容
                        neirong = r.read()
                        w1.seek(0, 0)
                        if not chongfujiancha(neirong, w1.read()):
                            w1.seek(0, 2)
                            pipeidao_file += 1
                            # 写入标题
                            w1.write(("第{}章 666 ".format(pipeidao_file) + os.path.splitext(os.path.basename(wenjian))[
                                0] + "\n\n").encode('gb18030'))
                            # 内容写入合并TXT
                            w1.write(neirong)
                            # 不同文件之间空10行
                            print("合并文章:{}".format(os.path.splitext(os.path.basename(wenjian))[0]))
                            w1.write(
                                "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n".encode('gb18030'))
                        else:
                            print("重复文件:{}".format(os.path.splitext(os.path.basename(wenjian))[0]))
                            pass
    print("\n一共{}个文件,匹配到{}个需要文件,{}个重复文件".format(all_file, pipeidao_file, chongfu_count))
    time.sleep(9999)


if __name__ == '__main__':
    main()
