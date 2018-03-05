import cv
import random
import math
from PIL import Image, ImageDraw 

def takePhoto():
	capture = cv.CaptureFromCAM(0)
	frame = cv.QueryFrame(capture)
	cv.SaveImage("capture.jpg", frame)



def editPhoto():
	image = Image.open("cam.jpg")  
	draw = ImageDraw.Draw(image)
	width = image.size[0]
	height = image.size[1]
	pix = image.load()
	imageMatrix= [[0] * height for i in range(width)]
	factor =50
	for i in range(width):

		for j in range(height):
			a = pix[i, j][0]
			b = pix[i, j][1]
			c = pix[i, j][2]
			S = a + b + c
			if (S > (((255 + factor) / 2) * 3)):
				imageMatrix[i][j]=1
				a, b, c = 255, 255, 255
			else:
				imageMatrix[i][j]=0
				a, b, c = 0, 0, 0
			draw.point((i, j), (a, b, c))
	image.save("ans.jpg", "JPEG")
	del draw
	return imageMatrix



def findLeftTop(mat):
	width=len(mat)
	height=len(mat[1])
	for i in range(height):
		for j in range(width):
			if mat[j][i]==1:
				if j+100<width:
					if mat[j+100][i]==1:
						if i+100<height:
							if mat[j][i+100]==1:
								if j-5>0:
									if mat[j-5][i+5]==1:
										next
									else:
										image = Image.open("ans.jpg")  
										draw = ImageDraw.Draw(image)
										for b in range(15):
											draw.point((j+b,i+b),(0,0,0))
										image.save("ans.jpg", "JPEG")
										del draw
										return j,i
def findRightTop(mat):
	width=len(mat)
	height=len(mat[1])
	for i in range(height):
		for j in range(width):
			if mat[width-j-1][i]==1:
				if width-j-51<width:
					if mat[width- j-51][i]==1:
						if i+50<height:
							if mat[width- j-1][i+50]==1:
								if j+5<width:
									if mat[width-j+4][i+5]==1:
										next 
									else:
										image = Image.open("ans.jpg")  
										draw = ImageDraw.Draw(image)
										for b in range(15):
											draw.point((width-j-b,i+b),(0,0,0))
										image.save("ans.jpg", "JPEG")
										del draw
										return width- j,i
def findBottomLeft(mat):
	width=len(mat)
	height=len(mat[1])
	for i in range(height):
		for j in range(width):
			if mat[j][height-1-i]==1:
				if j+50<width:
					if mat[j+50][height-1- i]==1:
						if height-i-51> 0:
							if mat[j][height-i- 51]==1:
								if j-5>0:
									if mat[j-5][height-i-5]==1:
										next
									else:
										image = Image.open("ans.jpg")  
										draw = ImageDraw.Draw(image)
										for b in range(15):
											draw.point((j+b,height- i-b),(0,0,0))
										image.save("ans.jpg", "JPEG")
										del draw
										return j,height- i


def findBottomRight(mat):
	width=len(mat)
	height=len(mat[1])
	for i in range(height):
		for j in range(width):
			if mat[width -j-1][height -1-i]==1 :
				if height -i -51>0:
					if mat[width-j-1][height-i-51]==1:
						if width- j-51>0:
							if mat[width -j-51][height-1-i]==1:
								if height-i+5<height:
									if width- j+5<width:
										if mat[width- j+5][height-i+5]==1:
											next
										else:
											image = Image.open("ans.jpg")  
											draw = ImageDraw.Draw(image)
											for b in range(15):
												draw.point((width- j-b,height- i-b),(0,0,0))
											image.save("ans.jpg", "JPEG")
											del draw
											return width- j,height- i

def readPoint(tli,tlj,tri,trj,bli,blj,bri,brj):
	lt=tri-tli
	ll=blj-tlj
	lb=bri-bli
	lr=brj-trj
	if math.fabs(lt - lb)>20:
		ideallentop=ll/1.41
		if math.fabs(lt- ideallentop)>30:
			if math.fabs(tli-bli)>20:
				return 1,bli
			else:
				return 2,bri

		else:
			if math.fabs(tri-bri)>20:
				print ('hdhd')
				return 3, tri
			else:
				return 4 , tli
	elif math.fabs(ll-lr)>20:
		ideallenbot=lt*1.41
		if math.fabs(ll- ideallenbot)>30:
			if math.fabs(tlj-trj)>20:
				return 5,trj
			else:
				return 8,brj

		else:
			if math.fabs(tlj-trj)>20:
				return 6, tlj
			else:
				return 7 , blj
	else:
		return 0,0


def printMat(mat):
	for i in range(len(mat)): 
		print(mat[i])


def cutPhoto(mat,st,sl,sb,sr):
	i=sb-st
	j=sr-sl
	print(len(mat))
	print(len(mat[0]))
	print i
	print j
	image = Image.open("cam.jpg")  
	draw = ImageDraw.Draw(image)
											
											
	page= [[0] * i for it in range(j)]
	for a in range(j):
		for b in range(i):
			page[a][b]=mat[a+sl][b+st]

	for a in range(j):
		for b in range(10):
			page[a][b]=1
			page[a][i-b-1]=1
	for a in range(i):
		for b in range(10):
			page[b][a]=1
			page[j-b-1][a]=1
	for a in range(j):
		for b in range(i):
			if(page[a][b]==1):
				draw.point((a,b),(255,255,255))
			else:
				draw.point((a,b),(0,0,0))


	image.save("capt.jpg", "JPEG")
	del draw

	return page


def findLine(page):
	maxW=0
	maxH=0
	for i in range(len(page[0])) :
		count=0
		for j in range(len(page)) :
			if page[j][i]==0:
				count+=1
				next
			else:
				if maxW<count:
					maxW=count
					break
	for i in range(len(page)):
		count=0
		for j in range(len(page[0])):
			if page[i][j]==0:
				count+=1
				next
			else:
				if maxH<count:
					maxH=count
					break
		
	print('maxH:'+str(maxH)+'  maxW'+str(maxW))
	if maxW>maxH:
		return 1,maxW
	else:
		return 2,maxH

def findTriangle(page):
	maxW=0
	maxH=0
	startfloat=0
	startW=0
	row=0
	endW=0
	startH=0
	endH=0
	column=0
	for i in range(len(page[0])) :
		count=0
		for j in range(len(page)) :
			if page[j][i]==0:
				if count==0:
					startfloat=j
				count+=1
				next
			else:
				if maxW<count:
					row=i
					startW=startfloat
					endW=j
					maxW=count
					break
	for i in range(len(page)):
		count=0
		for j in range(len(page[0])):
			if page[i][j]==0:
				if count==0:
					startfloat=j
				count+=1
				next
			else:
				if maxH<count:
					column=i
					startH=startfloat
					endH=j
					maxH=count
					break
		
	print('maxH:'+str(maxH)+'  maxW'+str(maxW))
	if maxW>maxH:
		midle=startW+((endW- startW)/2)
		print('start :'+str(startW)+'  end  :'+str(endW)+'  row:'+str(row))
		print('midle:'+str(midle))
		
		heightTriangle=5
		image = Image.open("capt.jpg")  
		draw = ImageDraw.Draw(image)
		height=len(page[0])
		for i in range(len(page)):
			draw.point((i,row),(0,0,0))
		for i in range(row):
			draw.point((midle,row-i),(0,0,0))
			heightTriangle+=1
			if page[midle+1][row-i-5]==0 and page[midle-1][row-i-5]==0 :
				break

		image.save("capt.jpg", "JPEG")
		del draw
		print('heightTriangle:'+str(heightTriangle))
		return 1,heightTriangle,endW-startW


	else:
		midle=startH+((endH- startH)/2)
		print('start :'+str(startH)+'  end  :'+str(endH)+'  row:'+str(column))
		print('midle:'+str(midle))
		
		heightTriangle=5
		image = Image.open("capt.jpg")  
		draw = ImageDraw.Draw(image)
		height=len(page[0])
		for i in range(len(page)):
			draw.point((i,row),(0,0,0))
		for i in range(row):
			draw.point((midle,row-i),(0,0,0))
			heightTriangle+=1
			if page[midle+1][row-i-5]==0 and page[midle-1][row-i-5]==0 :
				break

		image.save("capt.jpg", "JPEG")
		del draw
		print('heightTriangle:'+str(heightTriangle))
		return 1,heightTriangle,endW-startW

def lenght(max,page,WoH):
	width=len(page)
	height=len(page[0])
	if WoH==1:
		return float(float(21)*float(max)/float(width))
	else:
		return float(float(29.7)*float(max)/float(height))


def lenghtTr(page,WoH,heig,osn):
	width=len(page)
	height=len(page[0])
	if WoH==1:
		osnl=float(float(21)*float(osn)/float(width))
		heigl=float(float(29.7)*float(heig)/float(height))
		rebr=math.sqrt((osnl/2)**2+heigl**2)
		return osnl+2*rebr
	else:
		return float(float(29.7)*float(max)/float(height))





#takePhoto()
mat=editPhoto()
tli,tlj=findLeftTop(mat)
tri,trj=findRightTop(mat)
bli,blj=findBottomLeft(mat)
bri,brj=findBottomRight(mat)

eror,index=readPoint(tli,tlj,tri,trj,bli,blj,bri,brj)

if eror==1:
	tli=index
elif eror==2:
	tri=index
elif eror==3:
	bri=index
elif eror==4:
	bli=index
elif eror==5:
	tlj=index
elif eror==6:
	blj=index
elif eror==7:
	trj=index
elif eror==8:
	brj=index

print(str(tli)+'   '+str(tlj))
print(str(tri)+'   '+str(trj))
print(str(bli)+'   '+str(blj))
print(str(bri)+'   '+str(brj))
print(tli-tri)						
print(trj-brj)
st=(tlj+trj)/2
sl=(bli+tli)/2
sb=(brj+blj)/2
sr=(bri+tri)/2
print('st:  '+str(st)+'   sl:'+str(sl)+'   sb:'+str(sb)+'   sr:'+str(sr))



page=cutPhoto(mat,st,sl,sb,sr)
#printMat(page)

#WoH,max=findLine(page)

#print(lenght(max,page,WoH))
WoHT,trhei,osnov=findTriangle(page)
lenghtTr(page,WoHT,trhei,osnov)

