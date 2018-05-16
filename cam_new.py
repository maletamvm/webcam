import numpy as np
import cv2
from PIL import Image, ImageDraw 




def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"





def editPhoto():
    image = Image.open("capture.jpg")
    
    width = image.size[0] 
    height = image.size[1]
    print(width,height)
    pix = image.load()
    
    min_height=int(height-(height/2+height*0.1))
    height=int(height/2+height*0.1)
    min_width=int(width-(width/2+width*0.1))
    width=int(width/2+width*0.1)
    print ( width , height)

    new_image=Image.new('L',(width,height))
    draw = ImageDraw.Draw(new_image)
    
    
    imageMatrix= [[0] * height for i in range(width)]
    mat=[[0] * height for i in range(width)]
    factor =150
    for i in range(min_width,width+min_width):
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
                    f.write('.')
            f.write('\n')
    f.flush()
    f.close()
    return mat

def cut_Photo(mat):
    width=len(mat)-1
    height=len(mat[0])
    step_width=int(width/9)
    step_height=int(height/9)
    print(len(mat[0]),len(mat))
    print(step_width)
    print(step_height)



    aver0=0
    count=0
    for i  in range(8):
        for j in range(height):
            if mat[(i+1)*step_width][j]==1:
                print(count,j)
                count+=1
                aver0+=j
                break
    aver0s=aver0/count
    print(aver0s)



    aver1=0
    count=0
    print("aver1")
    for i in range(8):
        for j in range(height):
            if mat[(i+1)*step_width][height-j-1]==1 and mat[(i+1)*step_width+1][height-j-1]==1 :
                print(count,height-j)
                count+=1
                aver1+=height-j
                break
    aver1s=aver1/count


    aver2=0
    count=0
    print("aver2")
    for i in range(8):
        for j in range(width):
            if mat[j][step_height*(i+1)]==1 and mat[j][step_height*(i+1)+1]==1 :
                print(count,j,step_height*(i+1))
                count+=1
                aver2+=j
                break
    aver2s=aver2/count


    aver3=0
    count=0
    print("aver3")
    for i in range(8):
        for j in range(width):
            if mat[width-j-1][step_height*(i+1)]==1 :
                print(count,j,step_height*(i+1))
                count+=1
                aver3+=width - 1 -j
                break
    aver3s=aver3/count
   

    height=int(aver1s-aver0s)
    width=int(aver3s-aver2s)
    print(width,height)

    a=0
    ma=[[0] * height for i in range(width)]
    for i in range(int(aver2s), int(aver3s-1)):
        b=0
        for j in range(int(aver0s),int(aver1s-1)):
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
    
    
                

def LH(ma):
    width=len(ma)
    height=len(ma[0])
    print(width, height)
    maximal=0
    for i in range(width-1):
        count=0
        for j in range(height-1):
            if ma[i][j]==1 or ma[i+1][j]==1 or ma[i-1][j]==1 :
                #print( i,j)
                count +=1
        if maximal<count:
            maximal=count
           # print(maximal)
        

    print(float(maximal)/float(height)*21.0)
    res=float(maximal)/float(height)*21.0
    return toFixed(res,2)


def LW(ma):
    width=len(ma)-1
    height=len(ma[0])
    print(width, height)
    maximal=0
    for i in range(height-1):
        count=0
        for j in range(width-1):
            if ma[j][i]==1 or ma[j+1][i]==1 or ma[j-1][i]==1 :
                #print( i,j)
                count +=1
        if maximal<count:
            maximal=count
           # print(maximal)
        

    print(maximal)
    res=float(maximal)/float(width)*29.7
    return toFixed(res,2)
    
            
        
def TRW(ma):
    width=len(ma)-1
    height=len(ma[0])
    print(width, height)
    count=0
    poz_count=0
    maxi=0
    poz_maxi=0
    line_start=0
    line_end=0
    midl=0

    
    for i in range(height-1):
        count=0
        poz_count=i
        count_line_start=0
        count_line_end=0
        swith=0
        for j in range( width-1):
            if ma[j][i]==1 or ma[j-1][i+1]==1 or ma[j-1][i+1]==1:
                if swith==0:
                    count_line_start=j
                    swith=1
                count_line_end=j
                count+=1
        if maxi<count:
            maxi=count
            poz_maxi=poz_count
            line_start= count_line_start
            line_end=count_line_end
            midl=int((line_start+line_end)/2)
            print('poz')
            print(line_start,line_end)
            print('max')
            print(maxi,poz_maxi)


    print(midl)
    poz_height=0
    for i in range(height):
        for j in range(midl-5,midl+5):
            if ma[j][i]==1:
                print(i)
                poz_height=i
                break
        if poz_height!=0:
            break
    print(width, height)
    print(poz_height,poz_maxi)
    len_height=float(poz_maxi-poz_height)/float(width)*29.7
    osn=float(maxi)/float(width)*29.7
    print(osn,len_height)
    P=((len_height**2+(osn/2)**2)**(1/2))*2+osn
    print(P)
        

    return toFixed(P,2)




def TRH(ma):
    width=len(ma)-1
    height=len(ma[0])
    print(width, height)
    count=0
    poz_count=0
    maxi=0
    poz_maxi=0
    line_start=0
    line_end=0
    midl=0

    
    for i in range(width-1):
        count=0
        poz_count=i
        count_line_start=0
        count_line_end=0
        swith=0
        for j in range( height-1):
            if ma[i][j]==1 or ma[i+1][j+1]==1 or ma[i+1][j-1]==1:
                if swith==0:
                    count_line_start=j
                    swith=1
                count_line_end=j
                count+=1
        if maxi<count:
            maxi=count
            poz_maxi=poz_count
            line_start= count_line_start
            line_end=count_line_end
            midl=int((line_start+line_end)/2)
            print(line_start,line_end)
            print(maxi,poz_maxi)


    print(midl)
    poz_height=0
    for i in range(width):
        for j in range(midl-5,midl+5):
            if ma[i][j]==1:
                print(i)
                poz_height=i
                break
        if poz_height!=0:
            break
    print(poz_height,poz_maxi)
    print(width, height)
    print(maxi)
    len_height=float(poz_maxi-poz_height)/float(width)*29.7
    osn=float(maxi)/float(height)*21.0
    print(osn,len_height)
    P=((len_height**2+(osn/2)**2)**(1/2))*2+osn
    print(P)
        

    print(float(maxi)/float(height)*21.0)
    return toFixed(P,2)
    
                       
            
def doe():
    mat=editPhoto()                     
    ma=cut_Photo(mat)
    return ma



