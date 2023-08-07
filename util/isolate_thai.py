import re
filename = "word_list.txt"
output_filename = "output.txt"
fi = open(filename, mode='r', encoding="utf8")

line_list = fi.readlines()
for i in range(len(line_list)):
    line_list[i] = re.sub('[a-zA-Z]+', '', line_list[i]).strip() + "\n"
fi.close()

fo = open(output_filename, mode='w', encoding="utf8")
fo.writelines(line_list)
fo.close()