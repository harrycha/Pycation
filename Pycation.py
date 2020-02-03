import re
from time import sleep
import fileinput

# pat = "pyth_dir = string.joinfields(dir_parts, '\\')"
# pattern = re.compile(r'string[.]joinfields[(](\w+)[,][\s](\'?\.+\'?)[)]')
# print(pattern)
# answer = pattern.sub(r'\2.join(\1)', pat)
# # answer -> '\\'.join(dir_parts)
# print(answer)


pat = r"""string.joinfields(dir_parts, '\\')"""
pattern = re.compile(r"string(\.)joinfields(\()(\w+)(,)(\s+)")
# pattern = re.compile(r'string\.joinfields((\w+),\s(\'?\w+\'?))'
print(pattern)
answer = pattern.sub(r'join(\3)', pat)
# answer = pattern.sub(r'\2.join(\1)', pat)
# answer -> '\\'.join(dir_parts)
pattern = re.compile(r"join(\()(\w+)(\))(.+)")
answer = pattern.sub(r'\4join(\2)', answer)
answer = answer.replace(')', '', 1)

print(answer)

with open("Testfile.py", 'r+') as f:
    for word in f:
        pattern = re.compile(r'string.joinfields[(](\w+)[,]\s(\'?\.+\'?)[)]')
        answer = pattern.sub(r'\2.join(\1)', word)
        # f.write(line)
        # print(answer)
    f.close()
