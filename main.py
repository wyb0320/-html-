# coding=utf-8

import time
import re
import os
from lxml import etree


def save_pre(speaker,meeting_name,context):
    try:
        with open('./Pre/'+speaker.split(',')[0]+'_'+meeting_name+'_'+'Pre' + '.txt' , 'a') as f:
            # f.write(speaker)
            f.write(context+'\n')
    except:
        print(speaker+'中有错误字符')
def save_Post(speaker,meeting_name,context):
    try:
        with open('./Q&A/'+speaker.split(',')[0]+'_'+meeting_name+'_'+'Post' + '.txt' , 'a') as f:
            # f.write(speaker)
            f.write(context+'\n')
    except:
        print(speaker+'中有错误字符')
def preparation(file_dir):
    filelist = os.listdir(file_dir)
    for filename in filelist:
        with open(file_dir+'/'+filename, 'r') as f:
            res = f.read()
            data_tree = etree.HTML(res)
            f_titles = data_tree.xpath('//body/div/p/span/a/b/i/span/text()')  # 会议名称
            titles = []
            for title in f_titles:
                if 'Q' in title:
                    titles.append(title)
            context =data_tree.xpath('//body/div/p/span/text()')
            # 保存文本文件
            with open('./middle_text/' + filename + '.txt', 'w', encoding='utf-8') as file1:
                # file1.write(titles[0] + '\n' * 2)
                # file1.write('--------------------------------------------------------------------' + '\n')
                for line in context:
                    file1.write(line + '\n' * 2)
                file1.close()
                print(filename+'html已转成文本存放在middle_text中')
            #会议文本：
            text = '\n'.join(context)
            meets = text.split('Disclosure') # 注：会遇到FD不仅在会议开头的情况
            # meets = text.split('Fair')
            for i in range(len(titles)):
                with open('./meetings/' + titles[i] +'.txt', 'w', encoding='utf-8') as f1:
                    f1.write(meets[i+1])
                    f1.close()
            print('各会议保存成功，在meetings中')
            # remove('./meetsings', './All_meetings')
def remove(old_path ,new_path):
    path = old_path # 需要修改的文件的储存位置
    new_path = new_path
    filelist = os.listdir(path)
    for filename in filelist:
        Olddir=os.path.join(path,filename)
        Newdir=os.path.join(new_path,filename)
        os.rename(Olddir,Newdir)
def remove_first(old_path ,new_path):
    path = old_path # 需要修改的文件的储存位置
    new_path = new_path
    filelist = os.listdir(path)
    Olddir=os.path.join(path,filelist[0])
    Newdir=os.path.join(new_path,filelist[0])
    os.rename(Olddir,Newdir)

def find_Participants(file_dir1):
    # 提取参会人员信息
    filelist1 = os.listdir(file_dir1)
    for filename in filelist1[1:]:
        with open("./meetings/"+filename, 'r',encoding='utf-8') as f:
            print('正在处理' + filename)
            meet = f.read()
            participants = re.findall('Corporate Participants(.*?)Presentation', meet ,re.S)
            participant = participants[0].split('*')
        with open('./Corporate Participants/' + filename[:-4] + 'Corporate Participants' + '.txt', 'w', encoding='utf-8') as file1:
            file1.write('Corporate Participants:')
            for i in range(len(participant)):
                file1.write(participant[i] + '\n')
                file1.write('***************************************\n')
            file1.close()
    print('与会人员信息储存到Corporate Participants文件中')

def find_pre_post(file_dir1):
    #presentation发言
    filelist1 = os.listdir(file_dir1)
    for filename in filelist1:
        filename = filename[:-4]
        with open('./meetings/'+filename + '.txt' , 'r') as f:
            print('正在处理'+filename)
            meeting = f.read()
            pre = re.findall('Presentation\n(.*?)Questions and Answers',meeting,re.S)
            if pre == []:
                print('未知原因造成'+filename+'提取失败')
            else :
                pre = re.sub('\n',' ',pre[0])
                sentences = pre.split('. ')
                pre_speakers = []
                for i in range(len(sentences)):
                    if ':' in sentences[i] and sentences[i][:3].isupper():
                        pre_speakers.append(sentences[i].split(':')[0])
                # 提取pre_speaker的话：
                index = 0
                while index < len(pre_speakers)-1:
                    context = pre.split(pre_speakers[index+1])[0]
                    save_pre(pre_speakers[index], filename, context)
                    pre = pre_speakers[index+1].join(pre.split(pre_speakers[index+1])[1:])
                    index += 1
                save_pre(pre_speakers[index], filename, pre)

            post = meeting.split('Questions and Answers\n')[-1]
            post = re.sub('\n', ' ', post)
            sentences = post.split('. ')

        post_speakers = []
        for i in range(len(sentences)):
            if ':' in sentences[i] and sentences[i][:3].isupper():
                post_speakers.append(sentences[i].split(':')[0])

        index = 0
        while index < len(post_speakers) - 1:
            context = post.split(post_speakers[index + 1])[0]
            save_Post(post_speakers[index], filename, context)
            post = post_speakers[index + 1].join(post.split(post_speakers[index + 1])[1:])

            index += 1
        save_Post(post_speakers[index], filename, post)
    print('对话储存到Pre和Q&A文件中')

if __name__ == '__main__':

    # file_dir = "./raw_text"
    # file_dir1 = "./meetings"
    # filelist = os.listdir()
    # remove()
    # preparation(file_dir)
    filelist = os.listdir('./待处理')
    print(filelist)
    for filename in filelist:
        remove_first('./待处理','./raw_text')
        file_dir = "./raw_text"
        file_dir1 = "./meetings"
        preparation(file_dir)
        find_Participants(file_dir1)
        find_pre_post(file_dir1)
        remove('./Corporate Participants','./结果/'+filename[:-4]+'/Corporate Participants')
        remove('./meetings', './结果/' + filename[:-4] + './meetings')
        remove('./Q&A', './结果/' + filename[:-4] + '/Q&A')
        remove('./Pre', './结果/' + filename[:-4] + '/Pre')
        remove_first('./raw_text', './已处理')
    print('完成！请在结果中查看')


