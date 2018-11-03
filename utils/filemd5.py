import hashlib


def get_file_md5(path):
    md5obj = hashlib.md5()
    buf_size = 1024 * 8
    file = open(path, 'rb')
    while True:
        buf = file.read(buf_size)
        if not buf:
            break
        md5obj.update(buf)
    file.close()
    return str(md5obj.hexdigest()).upper()
