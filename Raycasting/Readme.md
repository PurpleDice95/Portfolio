# Raycaster  

A Raycasting engine used to place the player in a map that can be designed

# Run instructions  
  - Requires modules *numpy*, *pillow*, and *pygame*  
  - Desired *fov*, *in-game mouse sensitivity*, and *player movement speed* can be set in main.py
  - ***Map.png*** can be edited:
    * the size of the image is the size of the in-game map
    * all *white* pixels translate to empty space in-game
    * all other colored pixels translate to a obstucted space colored likewise
  - Run *main.py*  
  - Controls are as follows:  
    * **W** - moves the player forward with reference to the camera view
    * **S** - moves the player backward with reference to the camera view
    * **A** - moves the player left with reference to the camera view
    * **S** - moves the player right with reference to the camera view
    * ***Mouse*** - moving the mouse left and right shifts the camera view left and right respectively
  - *TopView.py* is a top down view of the raycaster with the same controls, used during development to give insight on functionality


