icture = np.array(picture)
    n = len(picture)
    m = len(picture[0])
    # print(picture[0:5,0:5,:])
    # input()
    for i in range(n-5):
        for j in range(m-5):
            red = np.multiply(np.reshape(picture[i:i+5,j:j+5,0:1],(5,5)),kernel).sum()
            green = np.multiply(np.reshape(picture[i:i+5,j:j+5,1:2],(5,5)),kernel).sum()
            blue = np.multiply(np.reshape(picture[i:i+5,j:j+5,2:3],(5,5)),kernel).sum()
            picture[i][j] = [red,green, blue]