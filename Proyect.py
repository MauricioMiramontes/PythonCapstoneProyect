#Hello friend tank you for picking my proyect to review
#Mauricio Miramontes 
#Ill try to comment everything so you can follow my code without problem 
#To Do: Use the NewsPaper variable as a global variable 
#This code needs to be excecuted in a Jupyter Notebook

#The imports
import zipfile
from PIL import Image
import pytesseract
import cv2 as cv
import numpy as np

# loading the face detection classifier
face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')

#The functions ill use in the code 

def getTextFromPage(NewsPaper, Page):
    #params: The NewsPaper as a ZipFile Object and the Page as a ZipFile.Infolist()
    #Output: A string called "text" with the text found in the image 
    
    #I create the PIL image to pass on to the pythesseract function 
    Page_pil = Image.open(NewsPaper.open(Page))
    Page_pil = Page_pil.convert('L')
    
    #Using the image_to_string function to get the text from the page
    text = pytesseract.image_to_string(Page_pil)
    return text

def getFacesFromPage(NewsPaper, Page):
    #params: The NewsPaper as a ZipFile Object and the Page as a ZipFile.Infolist()
    #Output: A list that contains the rectangle coordenates of every face the cv2 found
    
    faces = list()
    
    #I create the cv image from the .read() function in the ZipFile Object
    page_data = NewsPaper.read(Page)
    page_cv = cv.imdecode(np.frombuffer(page_data, np.uint8), 1)
    
    #After a lot of testing I found that converting the image to gray scale and using a 1.35 scale factor in the 
    #detectMultiScale() function gives me the best results
    gray = cv.cvtColor(page_cv, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.35)
    
    return faces

def cropFacesFromPage(NewsPaper, Page):
    #params: The NewsPaper as a ZipFile Object and the Page as a ZipFile.Infolist()
    #Output: A PIL image object with the faces found in the page                    
    
    FacesList = list()
    thumbnail_size = (100,100)
    
    #I call the previus function to get the list of the squares that contain the faces in the image 
    Faces_Squares = getFacesFromPage(NewsPaper, Page)
    
    #If it is an empty list then no faces where found and we return a null 
    if Faces_Squares == (): return None
    
    #I create a PIL Image object for the News Paper Page
    page_pil = Image.open(NewsPaper.open(Page))
    page_pil = page_pil.convert("RGB")
  
    #Using the info in the Faces_Squares list a make a Faces List with the croped faces 
    for x,y,w,h in Faces_Squares:
        # And remember this is width and height so we have to add those appropriately.
        Face = page_pil.crop((x,y,x+w,y+h))
        Face.thumbnail(thumbnail_size) 
        FacesList.append(Face)
        
    #I create a sheet to paste the Images in the FacesList
    contact_sheet=Image.new(page_pil.mode, (FacesList[0].width*5,
                                                int(
                                                    (len(FacesList)/5)+1)*FacesList[0].height
                                           ))
    
    
    x=0
    y=0
    
    for Face in FacesList:
        # Lets paste the current face into the contact sheet
        contact_sheet.paste(Face, (x, y) )
        # Now we update our X position. If it is going to be the width of the image, then we set it to 0
        # and update Y as well to point to the next "line" of the contact sheet.
        if x+FacesList[0].width == contact_sheet.width:
            x=0
            y=y+thumbnail_size[1]
        else:
            x=x+thumbnail_size[0]

    
    return contact_sheet


wordToSearch = input('Tell me what word do you want to search in the news paper ')

#I open the zip file and call it NewsPaper
NewsPaper = zipfile.ZipFile("readonly/images.zip")

for Page in NewsPaper.infolist():
    
    if wordToSearch not in getTextFromPage(NewsPaper, Page): continue
    else:
        Faces = cropFacesFromPage(NewsPaper, Page)
      
        print('Results found in file {}'.format(Page.filename))
        
        if Faces is None: print('But there were no faces in that file!')
        else: display(Faces)
