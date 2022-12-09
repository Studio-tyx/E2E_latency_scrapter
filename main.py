
import hashlib
import sys

def main(args=None):
    md5encoder = hashlib.new("md5")
    body = 'temperature'
    # event = body.decode('utf-8')
    md5encoder.update(body.encode('utf-8'))
    fid = md5encoder.hexdigest()
    print(fid)
    # print("b67dc6cccbf6aeaeeeef8690bacd403c")
    # body = 'temperature'
    # event = body.decode('utf-8')
    # md5encoder.update(body.encode('utf-8'))
    # fid = md5encoder.hexdigest()
    #print(fid)

    md5encoder = hashlib.new("md5")
    body = 'temperature'
    # event = body.decode('utf-8')
    md5encoder.update(body.encode('utf-8'))
    fid = md5encoder.hexdigest()
    print(fid)



if __name__ == '__main__':
    sys.exit(main())