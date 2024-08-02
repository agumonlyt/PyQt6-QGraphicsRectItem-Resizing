# PyQt6-QGraphicsRectItem-Resizing
example code for QGraphicsRectItem resizing. 


# Usage: 
- ```python example.py```


<br>

I dont find any good example online that show how to resize QGraphicsRectItem. 

Hopefully this will help someone out there who need it. 

Mostly just the mouseMoveEvent() function. 

Might not be correct or the most perfect implementation, but this is what I can achieve so far. 

Basically using `self.pos()` `self.rect()` `self.scene().sceneRect()` and manipulating and checking boundaries. 

Note that in pyqt the coordinate system is complicated. 

`self.pos()` - return rect pos on the scene. <br>
`self.rect()` - return rect object itself, note that `.left()` `.top()` can be negative value. Not sure about `.right()` and `.bottom`. <br>
`self.scene().sceneRect()` - not sure, maybe return scene dimension. <br>

To check whether a rect is outside its scene, you need to check both `self.pos()` and `self.rect()` value. One tells where the rect object is on the scene, another tells the rect attribute (left top right bottom) even after resizing. 

<br> 


https://github.com/user-attachments/assets/a921c618-2c52-4280-8a63-731dc702b638


<br>

