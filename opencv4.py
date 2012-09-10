import cv

cv.NamedWindow("ColorMap", cv.CV_WINDOW_AUTOSIZE)
camera_index = 0
capture = cv.CaptureFromCAM(camera_index)

def repeat():
    global capture #declare as globals since we are assigning to them now
    global camera_index
    frame = cv.QueryFrame(capture)
   
    Frame32F = cv.CreateImage((frame.width, frame.height), cv.IPL_DEPTH_32F, 3)
    cv.ConvertScale(frame,Frame32F)

    FrameGS_32F = cv.CreateImage ((frame.width,frame.height), cv.IPL_DEPTH_32F, 1)
    cv.CvtColor(Frame32F,FrameGS_32F,cv.CV_RGB2GRAY)

    FrameGS = cv.CreateImage ((frame.width,frame.height), cv.IPL_DEPTH_8U, 1)
    cv.ConvertScale(FrameGS_32F,FrameGS)
   
   
   
   
    #create the image arrays we require for the processing
    hue=cv.CreateImage((frame.width,frame.height), cv.IPL_DEPTH_8U, 1)
    sat=cv.CreateImage((frame.width,frame.height), cv.IPL_DEPTH_8U, 1)
    val=cv.CreateImage((frame.width,frame.height), cv.IPL_DEPTH_8U, 1)
    mask_1=cv.CreateImage((frame.width,frame.height), cv.IPL_DEPTH_8U, 1)
    mask_2=cv.CreateImage((frame.width,frame.height), cv.IPL_DEPTH_8U, 1)

    #convert to cylindrical HSV color space
    cv.CvtColor(frame,frame,cv.CV_RGB2HSV)
    #split image into component channels
    cv.Split(frame,hue,sat,val,None)
    #rescale image_bw to degrees
    cv.ConvertScale(FrameGS, FrameGS, 180 / 256.0)
    #set the hue channel to the greyscale image
    cv.Copy(FrameGS,hue)
    #set sat and val to maximum
    cv.Set(sat, 255)
    cv.Set(val, 255)

    #adjust the pseudo color scaling offset, 120 matches the image you      displayed
    offset=120
    cv.CmpS(hue,180-offset, mask_1, cv.CV_CMP_GE)
    cv.CmpS(hue,180-offset, mask_2, cv.CV_CMP_LT)
    cv.AddS(hue,offset-180,hue,mask_1)
    cv.AddS(hue,offset,hue,mask_2)

    #merge the channels back
    cv.Merge(hue,sat,val,None,frame)
    #convert back to RGB color space, for correct display
    cv.CvtColor(frame,frame,cv.CV_HSV2RGB)
    
    
    
    
    
    cv.ShowImage("w1", frame)
    c = cv.WaitKey(10)
    if(c=="n"): #in "n" key is pressed while the popup window is in focus
        camera_index += 1 #try the next camera index
        capture = cv.CaptureFromCAM(camera_index)
        if not capture: #if the next camera index didn't work, reset to 0.
            camera_index = 0
            capture = cv.CaptureFromCAM(camera_index)

while True:
    repeat()