from email import policy
from email.parser import BytesParser
import glob, re

# 辨識是否包含關鍵字。
def isInArray (array, line):
    for item in array:
        if item in line:
            return True
    return False

# 列入需要移除的關鍵字
del_array = [
"############ MultiConfigPart END",
"________________________________",
"TSMC PROPERTY",
"This email communication (and any attachments) is proprietary information for the sole use of its intended recipient. Any unauthorized review, use or distribution by anyone other than the intended recipient is strictly prohibited. If you are not the intended recipient, please notify the sender by replying to this email, and then delete this email and any copies of it immediately. Thank you.",
"############ MultiConfigPart Running configuration",
]

# 匹配 Hostname 的關鍵字
pattern = "sysname"

# 設定匹配本目錄下的檔案
path = './'  # set this to "./" if in current directory

# 匹配 *.eml
eml_files = glob.glob(path + '*.eml')  # get all .eml files in a list
for eml_file in eml_files:
    with open(eml_file, 'rb') as fp:  # select a specific email file from the list
        name = fp.name  # Get file name
        msg = BytesParser(policy=policy.default).parse(fp)
    text = msg.get_body(preferencelist=('plain')).get_content()
    fp.close()

# 將解析出來的Config 以 \r\n 作為分行
    sptext = text.split("\r\n")

# 分離出 Hostname 做為等等命名使用。
    for line in sptext:
        if re.search(pattern, line):
            sysname = line.split(" ")[2]

# 單純將 Mail 中文字析出
    #path = sysname +'O-RIG.txt'
    #f = open(path, 'w')
    #f.write(text)
    #f.close()

# 將Mail Config 析出 並移除掉關鍵字。
    path = sysname + '.cfg'
    f = open(path, 'w')
    for line in sptext:
        if not isInArray(del_array, line):
            if line != "":
                #print(line)
                f.write(line + "\n")
    f.close()

    #print(name)  # Get name of eml file
    #print(text)  # Get list of all text in email
