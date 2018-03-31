import numpy as np
import cv2
from PIL import Image, ImageDraw 



def takePhoto():
    cap = cv2.VideoCapture(1)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame
        cv2.imshow('frame',gray)
        if cv2.waitKey(1) & 0xFF == ord('e'):
            cv2.imwrite('capture.jpg',gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

def editPhoto():
    image = Image.open("capture.jpg")  
    width = image.size[0] 
    height = image.size[1] 
    pix = image.load()
    
    min_height=int(height-(height/2+height*0.05))
    height=int(height/2+height*0.05)
    min_width=int(width-(width/2+width*0.05))
    width=int(width/2+width*0.05)
    #print ( width , height)

    new_image=Image.new('L',(width,height))
    draw = ImageDraw.Draw(new_image)
    
    
    imageMatrix= [[0] * height for i in range(width)]
    mat=[[0] * height for i in range(width)]
    factor =110
    for i in range(min_width,width+min_width-1):

        for j in range(int(height)):
            a = pix[i,j]
            if (factor >a):
                imageMatrix[i-min_width][j]=1
                a=255
            else:
                imageMatrix[i-min_width][j]=0
                a=0
            draw.point((i-min_width, j), a)
    new_image.save("ans.jpg", "JPEG")
    del draw
    f = open('out.txt', 'wt')

    for i in range(1,width):
            for j in range(1,height):
                if imageMatrix[i][j]+imageMatrix[i][j-1]==1 or imageMatrix[i][j]+imageMatrix[i-1][j]==1  :
                    mat[i][j]=1
                    f.write('*')
                else:
                    mat[i][j]=0
                    f.write(' ')
            f.write('\n')
    f.flush()
    f.close()
    return mat

def cut_Photo(mat):
    step_width=len(mat)/5
    step_height=len(mat[0])/5
    aver0=0
    #print( len(mat) , len(mat[0]))
    for i in range(4):
        for j in range (len(mat[0])):
            if mat[(i+1)*step_width][j]==1:
                aver0+=j
                break
    #print(aver0/4)
    aver1=0
    for i in range(4):
        for j in range (len(mat[0])):
            if mat[(i+1)*step_width][len(mat[0])-1-j]==1:
                aver1+=len(mat[0])-1-j
                break
    height=(aver1-aver0)/4
    #print(aver1/4)
    aver2=0
    for i in range(4):
        for j in range (len(mat)):
            if mat[j][(i+1)*step_height]==1:
                aver2+=j
                break
    #print(aver2/4)
    aver3=0
    for i in range(4):
        for j in range (len(mat)):
            if mat[len(mat)-j-2][(i+1)*step_height]==1:
                aver3+=len(mat)-1-j
                break
    #print('errr:'+str(aver3/4))
    width=(aver3-aver2)/4
    #print(height  , width)



    a=0
    ma=[[0] * height for i in range(width)]
    for i in range(aver2/4, aver3/4-1):
        b=0
        for j in range(aver0/4,aver1/4-1):
            if mat[i][j]==1:
                ma[a][b]=1
            else:
                ma[a][b]=0
            b+=1
        a+=1



    cut=Image.new('L',(width,height))
    draw = ImageDraw.Draw(cut)
    for i in range(len(ma)):
        for j in range(len(ma[0])):
            if ma[i][j]==1 and i>5 and j>5 and i<(len(ma)-5) and j<(len(ma[0])-5):
                ma[i][j]=1
                draw.point((i, j), 0)
            else:
                ma[i][j]=0
                draw.point((i ,j), 255)

    cut.save("cut.jpg", "JPEG")
    del draw
                

    
    return ma
    
    
                

def line_H(ma):
    width=len(ma)
    height=len(ma[0])
    print(width, height)
    poz_line=0
    for i in range(width):
        if ma[i][len(ma[0])/2]==1:
            poz_line=i
            break
    #print('sdsdsd'+str(poz_line))
    maximal=0
    for i in range(poz_line-5,poz_line+5):
        count=0
        for j in range(height):
            if ma[i][j]==1 or ma[i+1][j]==1 or ma[i-1][j]==1 :
                #print( i,j)
                count +=1
        if maximal<count:
            maximal=count
           # print(maximal)
        

    print(float(maximal)/float(height)*21.0)


def line_W(ma):
    width=len(ma)
    height=len(ma[0])
    print(width, height)
    poz_line=0
    for i in range(height):
        if ma[len(ma)/2][i]==1:
            poz_line=i
            break
    #print('sdsdsd'+str(poz_line))
    maximal=0
    for i in range(poz_line-5,poz_line+5):
        count=0
        for j in range(width):
            if ma[j][i]==1 or ma[j+1][i]==1 or ma[j-1][i]==1 :
                #print( i,j)
                count +=1
        if maximal<count:
            maximal=count
           # print(maximal)
        

    print(float(maximal)/float(height)*29.7)
            
        
    
                       
            
        

#takePhoto()
mat=editPhoto()

                      
ma=cut_Photo(mat)
f = open('out.txt', 'wt')
for i in range(1,len(ma)):
    for j in range(1,len(ma[0])):
        if ma[i][j]==1:
            f.write('*')
        else:
            f.write(' ')
    f.write('\n')
f.flush()
f.close()
line_W(ma)


