#coding:utf-8  
import os,sys
import jieba.analyse
from getKeytag import terminology

def cut_sentence(content):
	indx = 0
	cutlist = "。，,！……!\"':：？\?、\|”’；：？！。，;、~——+％%`:”＂'\n\r".decode('utf8') #》>]}）}】)｝）
	prefix = "[《<“‘{（【{(｛（“‘".decode('utf8')
	sentences = []
	for i in range(len(content)):
		if content[i] in cutlist:
			if content[indx:i+1][0] not in prefix:
				sentences.append(content[indx:i+1])
			indx = i+1
	return sentences

def long_Gener(intro,length = 5,f="example_.txt"):
	rule =  ("，,：;、”》>\":：、\|”’；]}）}】)｝）~——+％%`:”＂").decode('utf8')
	content = intro
	if intro[-1] == '）'.decode('utf8'):
		content = ''.join(intro.split()[:-1])
	# words = jieba.cut(content, cut_all=False)
	# print(", ".join(words))
	sentences = cut_sentence(content)
	# keyWords = jieba.analyse.extract_tags(content,length)
	keyWords = terminology(f, topK = 10, span = 2, threshold = 5, mode = 1)
	output = '<p class="p1"><b>%s</b></p><br><br>'%sentences[0]
	output += "Key Words:  "+", ".join(keyWords)+"<br><br>"
	output += "\n"
	summary = []
	del sentences[0]
	for sentence in sentences:
		flag2=0
		if "第一部分".decode('utf8') in sentence:
			summary +=["<h3>"]
			flag2=1
		flag = 1
		for keyWord in keyWords:
			if keyWord in sentence:
				# summary += ['<span class="s1">'+sentence+'</span>']
				summary += [sentence.replace(keyWord,'<span class="s1">'+keyWord+'</span>')]
				flag = 0
				break
		if flag == 1:
			summary += [sentence]
		if flag2 == 1:
			summary +=["</h3>"]
		# sentence.replace(keyWord,'<span class="s1">'+keyWord+'</span>')
		# if len(summary) >= length:
			# break
                
	end = 0
	for i in range(len(summary)-1,-1,-1):
		if summary[i][-1] not in rule:
			end = i
			break
	summary = "".join(summary[:end+1])
	return output+summary.strip()
	# for sentence in sentences:
	# 	for keyWord in keyWords:
	# 		sentence.replace(keyWord,'<span class="s1">'+keyWord+'</span>')
	# 	output += sentence
	# print output
	# return output




if __name__ == '__main__':
    html = open('content.html', 'w')
    html.write("""
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <meta http-equiv="Content-Style-Type" content="text/css">
  <title></title>
  <meta name="Generator" content="Cocoa HTML Writer">
  <meta name="CocoaVersion" content="1344.72">
  <style type="text/css">
    p.p1 {margin: 0.0px 0.0px 0.0px 0.0px; text-align: center; font: 26.0px 'Heiti SC Light'}
    p.p2 {margin: 0.0px 0.0px 0.0px 0.0px; text-align: justify; font: 14.0px 'Heiti SC Light'}
    span.s1 {color: #ff4013}
    span.s2 {font: 14.0px Helvetica}
  </style>
</head>
<body>
""")

    files = os.listdir('.')
    # 首先处理文本
    for f in files:
        if f.lower().endswith('_.txt'):
            print(f)
            fp = open(f)
            intro = fp.read().decode('utf8')
            content=long_Gener(intro,10,f)
            fp.close()
            #print content
            html.write("<p>%s</p>" % content.encode("utf8"))
    # 然后处理图片
    for f in files:
        if f.lower().endswith('.jpg') or f.lower().endswith('.png'):
            html.write("<img src='%s' />" % f)

    html.write('</body></html>')
    html.close()
