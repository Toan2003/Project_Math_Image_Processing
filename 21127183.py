import numpy as np
import matplotlib.pyplot as plt
import PIL as P


def Input(path):
    picture = P.Image.open(path)
    picture = np.array(picture)
    return picture

def Output(picture):
    plt.imshow(np.array(picture))
    plt.show()

def saveFile(fileSave, array):
    plt.imsave(fileSave, np.array(array,dtype= 'uint8'))

def increaseBrightness(picture):
    picture = np.array(picture,int) + 100
    picture = np.clip(picture,0,255)
    return picture 

def increaseConstrast(picture, constrast = 50):
    factor = (259*(255+constrast))/(255*(259-constrast))
    picture = np.array(picture,int)
    picture = factor*(picture-128) +128    
    picture = np.clip(picture,0,255)
    return np.array(picture,int)

#dọc
def flipImageVertically(picture):
    picture = np.array(picture)
    return np.flip(picture,0)

#ngang
def flipImageHorizontally(picture):
    picture = np.array(picture)
    return np.flip(picture,1)

def convertToGrayScale(picture):
    picture = np.array(picture)
    for pixels in picture:
        for pixel in pixels:
            pixel[0] = pixel[1] = pixel[2] = pixel[0]* 0.3 +pixel[1]*0.59 +pixel[2]*0.11
    return np.array(picture,int)

def convertToSepia(picture):
    picture = np.array(picture)
    for pixels in picture:
        for pixel in pixels:
            tr = 0.393*pixel[0] + 0.769*pixel[1] + 0.189*pixel[2]
            tg = 0.349*pixel[0] + 0.686*pixel[1] + 0.168*pixel[2]
            tb = 0.272*pixel[0] + 0.534*pixel[1] + 0.131*pixel[2]
            if tr > 255: pixel[0] = 255
            else: pixel[0] = tr

            if tg > 255: pixel[1] = 255
            else: pixel[1] = tg

            if tb > 255: pixel[2] = 255 
            else: pixel[2] = tb
    return np.array(picture,int)

def gaussianBlur(picture):
    kernel = [[1,4,6,4,1],
            [4,16,24,16,4],
            [6,24,36,24,6],
            [4,16,24,16,4],
            [1,4,6,4,1]]
    kernel = np.array(kernel) * (1/256)
    # print('herre')
    # print(np.multiply(kernel,test))
    # input()
    picture = np.array(picture)
    temp = np.array(picture)
    n = len(picture)
    m = len(picture[0])
    # print(picture[0:5,0:5,:])
    # input()
    for i in range(2,n-2):
        for j in range(2,m-2):
            red = (np.reshape(temp[i-2:i+3,j-2:j+3,0:1],(5,5))*kernel).sum()
            green = (np.reshape(temp[i-2:i+3,j-2:j+3,1:2],(5,5))*kernel).sum()
            blue = (np.reshape(temp[i-2:i+3,j-2:j+3,2:3],(5,5))*kernel).sum()

            picture[i][j][0] = red
            picture[i][j][1] = green
            picture[i][j][2] = blue
    
    return np.array(picture,int)

def sharpen(picture):
    kernel = [[1,4,6,4,1],
            [4,16,24,16,4],
            [6,24,-476,24,6],
            [4,16,24,16,4],
            [1,4,6,4,1]]
    kernel = np.array(kernel) * (-1/256)
    picture = np.array(picture)
    temp = np.array(picture)
    n = len(picture)
    m = len(picture[0])
    # print(picture[0:5,0:5,:])
    # input()
    for i in range(2,n-2):
        for j in range(2,m-2):
            red = (np.reshape(temp[i-2:i+3,j-2:j+3,0:1],(5,5))*kernel).sum()
            green = (np.reshape(temp[i-2:i+3,j-2:j+3,1:2],(5,5))*kernel).sum()
            blue = (np.reshape(temp[i-2:i+3,j-2:j+3,2:3],(5,5))*kernel).sum()

            picture[i][j][0] = red
            picture[i][j][1] = green
            picture[i][j][2] = blue
    
    return np.array(picture,int)
    
def cropImageInCenter(picture):
    picture = np.array(picture)
    n = len(picture)
    m = len(picture[0])
    n1 = int(n/4)
    m1 = int(m/4)
    picture = picture[n1:n1*3,m1:m1*3,:]
    return picture

def cropSquareImageInCircle(picture):
    picture = np.array(picture)
    n = len(picture)
    r = int(n/2)
    a,b = r,r
    for x in range(n):
        for y in range(n):
            x1 = np.power((x-a),2)
            x2 = np.power((y-b),2)
            if (x1+x2 > np.power(r,2)):
                picture[x][y] = [0,0,0]
    return picture

def cropEllipseImage(picture):
    picture =np.array(picture)
    n = len(picture)
    m = len(picture[0])
    a = np.sqrt(np.power(n,2) + np.power(m,2))/2 *6/7
    b = n/2 *2/3
    # b = np.sqrt(np.power(n/4,2) + np.power(m/4,2))/2
    # a = np.sqrt(np.power(n,2) + np.power(m,2))
    alpha = np.arctan((n/2)/(m/2))
    beta = np.pi - alpha
    a2 = np.power(a,2)
    b2 = np.power(b,2)

    # eclipse 1
    cos1 = np.cos(alpha)
    sin1 = np.sin(alpha)
    cos21 = np.power(cos1,2)
    sin21 = np.power(sin1,2)
    coso11 = cos21/a2 + sin21/b2
    coso21 = cos21/b2 + sin21/a2
    cosoXY1 = 2*cos1*sin1*(1/a2 - 1/b2)

    # eclipse 2
    cos2 = np.cos(beta)
    sin2 = np.sin(beta)
    cos22 = np.power(cos2,2)
    sin22 = np.power(sin2,2)
    coso12 = cos22/a2 + sin22/b2
    coso22 = cos22/b2 + sin22/a2
    cosoXY2 = 2*cos2*sin2*(1/a2 - 1/b2)

    for x in range(n):
        for y in range(m):
            if (coso11*np.power(x-n/2,2) + cosoXY1*(x-n/2)*(y-m/2) + coso21*np.power(y-m/2,2) >= 1) and (coso12*np.power(x-n/2,2) + cosoXY2*(x-n/2)*(y-m/2) + coso22*np.power(y-m/2,2) >= 1):
                picture[x][y] = [0,0,0]
    return picture

def Interact():
    picture = input('Nhập tên ảnh (example.png/example.jpg): ')
    name = picture[:len(picture) - 4]
    type = picture[len(picture)-4:]
    print("0: làm tất cả")
    print("1: tăng độ sáng")
    print("2: tăng tương phản")
    print("3: lật ảnh dọc")
    print("4: lật ảnh ngang")
    print("5: chuyển ảnh sang xám")
    print("6: chuyển ảnh sang sepia")
    print("7: làm mờ ảnh")
    print("8: làm sắc nét ảnh")
    print("9: cắt ảnh ở trung tâm")
    print("10: cắt ảnh theo khuôn hình tròn")
    print("11: cắt ảnh theo khuon hình ellipse")
    action = int(input("Nhap thao tac muon xu ly: "))
    return picture, name,type,action

def doAction(action,array,name,type):
    if action == 1:
        picture = increaseBrightness(array)
        newname = name +"_increaseBright"+type
    elif action == 2:
        picture = increaseConstrast(array)
        newname = name +"_increaseConstrast"+type
    elif action ==3:
        picture = flipImageVertically(array)
        newname = name +"_flipVertical"+type
    elif action == 4:
        picture = flipImageHorizontally(array)
        newname = name +"_flipHorizontal"+type
    elif action == 5:
        picture = convertToGrayScale(array)
        newname = name +"_gray"+type
    elif action ==6:
        picture = convertToSepia(array)
        newname = name +"_speia"+type
    elif action == 7:
        picture = gaussianBlur(array)
        newname = name +"_blur"+type
    elif action == 8:
        picture = sharpen(array)
        newname = name +"_sharp"+type
    elif action == 9:
        picture = cropImageInCenter(array)
        newname = name +"_cropCenter"+type
    elif action == 10:
        picture = cropSquareImageInCircle(array)
        newname = name +"_cropCircle"+type
    elif action == 11:
        picture = cropEllipseImage(array)
        newname = name +"_cropEllipse"+type
    saveFile(newname,picture)

if __name__ == "__main__":
    picture, name,type,action = Interact()
    array = Input(picture)
    if action == 0:
        for i in range(1,12):
            doAction(i,array,name,type)
    else:
        doAction(action,array,name,type)