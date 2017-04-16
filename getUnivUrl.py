import searchUrl

csv_file = open('univ2016.csv', 'rt')
lines = csv_file.readlines()
csv_file.close()

i = 0
err_times = 0
while i < len(lines):
    line=lines[i].strip('\n')
    li = line.split(',')
    print('[+]No.{} 正在搜索 {} 的URL ...'.format(i+1, li[1]))
    try:
        url = searchUrl.search(li[1])
        if not url:
            raise Exception('Empty Url')
        url_file = open('univUrl2016.csv', 'a+')
        url_file.write('{},{},{},{},{}\n'.format(li[0], li[1], li[2], li[3], url))
        url_file.close()
        i += 1
        err_times = 0
    except Exception as ex:
        print('[-]ERROR: ' + str(ex))
        err_times += 1
        if(err_times > 10):				#连续十次未获取成功就令URL为None，并跳过
            print('[-]跳过')
            url_file = open('univUrl2016.csv', 'a+')
            url_file.write('{},{},{},{},{}\n'.format(li[0], li[1], li[2], li[3], 'None'))
            url_file.close()
            i += 1


