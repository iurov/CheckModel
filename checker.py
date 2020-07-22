from os import listdir
from os.path import isfile, join
import comare
import re
import transliterate

files= [f for f in listdir("izbs") if isfile(join("izbs", f))]
 
result = ""
scscs = 0
for f in files:
    scscs += 1
    print(f)
    try:
        my_file = open("izbs/"+f, "r", encoding="utf-8")
        lines = my_file.readlines()
        j = 0
        for st in lines:
            if re.search("[а-яА-я]", st):
                try:
                    result = transliterate.translit(st, reversed=True)
                except:
                    x = 1
                lines[j] = result
            j+=1
        my_file.close()
        my_file = open("izbs/"+f, "w")
        for line in lines:
            my_file.write(line)
    except:
        print("Hitlar file")

# my_file = open("izbs/2999126_OK_91.obj", "r", encoding="utf-8")
# j = 0
# lines = my_file.readlines()
# # print(transliterate.translit( lines[19393], reversed=True))
# for st in lines:
#     if re.search("[а-яА-я]", st):
#         print('true')
#     result=st
#     try:
#         result = transliterate.translit(st, reversed=True)
#     except:
#         x = 1
#     lines[j] = result
#     j+=1
# my_file.close()
# my_file = open("izbs/2999126_OK_91.obj", "w")
# for line in lines:
#     my_file.write(line)
# my_file.close()

# j=0
# lines = ["жопа", "xyi", "сися"]
# for st in lines:
#     len_st = len(st)
#     if re.match("""^[а-яА-ЯёЁ][а-яё0-9 !?:;"'.,]+$""", st):
#         print(st)
#         result=""
#         for i in range(0,len_st):
#             if st[i] in alphabet:
#                 simb = dic[st[i]]
#             else:
#                 simb = st[i]
#             result = result + simb
#         lines[j] = result
#     j+=1
# print(lines)