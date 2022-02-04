import win32com.client 

# 预装了屏蔽词的朗读

speak = win32com.client.Dispatch('SAPI.SPVOICE')
f1 = ["迷你", "mini", "MD", "cmn", "TMD", "他妈的", "马牛逼", "丁三石", "吊", "蛋蛋", "鸡鸡", "草",
      "智障", "NB", "牛逼", "大便", "屎", "尿", "你妈", "囸", "SB", "VIP", "vip", "MMP",
      "mmp", "屁", "仙人", "先人", "妈逼", "fuck", "FUCK", "Fuck", "王八蛋", "你奶奶的",
      "你妈死了", "逼", "傻逼", "煞笔", "沙比", "沙壁", "nmsl", "sb", "马化腾", "麻花疼",
      "丁三石", "作弊", "脑子有病", "操", "卧槽", "我操", "握草", "特么的", "你妈的",
      "妈蛋", "装逼", "nm", "jb", "操", "傻", "猪", "变态", "死", "歹","鸡巴","他娘的","shit"]
while True:
    f = input()
    for i in f1:
        f = f.replace(i, '*')
    print(f)
    speak.Speak(f)
    
