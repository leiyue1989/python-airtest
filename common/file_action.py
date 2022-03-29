def readFile(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except:
        content = ""
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    return content


def writeFile(path, content):
    with open(path, "a+", encoding="utf-8") as f:
        f.write(str(content)+"\n")
        print("写入成功！")
    return "写入成功!"


def clearFile(path):
    f = open(path, "r+")
    f.truncate()