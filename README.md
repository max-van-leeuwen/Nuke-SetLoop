# SetLoop

![reaction diffusion in Nuke setloop](https://maxvanleeuwen.com/wp-content/uploads/ReactionDiffusion.gif) ![motion graphics nuke setloop loop nodes](https://maxvanleeuwen.com/wp-content/uploads/MotionGraphics.gif) ![setloop geo](https://maxvanleeuwen.com/wp-content/uploads/geo.gif)

![example_1](https://maxvanleeuwen.com/wp-content/uploads/STILL_1-1.jpg) ![julia set nuke feedback iterator](https://maxvanleeuwen.com/wp-content/uploads/JuliaSet.jpg)

*Examples of looped geo, a Mandelbrot and a Julia set, and Reaction Diffusion - all done with SetLoop*

See [my website](https://maxvanleeuwen.com/setloop) for more information and examples!

<br> 

SetLoop is a toolset for Nuke that can loop a set of nodes.
<br>It copies the nodes you place between StartLoop and EndLoop inside EndLoop (which is a group), and reconnects them properly.
<br>But there are many more features to it which, combined, make this an actually functional node iterator that can render fractals (like the Julia set) and animated reaction diffusion entirely from within Nuke.

![nuke setloop](https://maxvanleeuwen.com/wp-content/uploads/SetLoop_01.png)
![nuke setloop max van leeuwen](https://maxvanleeuwen.com/wp-content/uploads/SetLoop_02.png)

See [my website](https://maxvanleeuwen.com/setloop) for more information/examples!

<br> 

## Installation

1. Place the SetLoop folder in your .nuke folder (or somewhere else on your computer).
2. Go to your .nuke folder, and create a file called 'init.py'. If such a file already exists, open it.
3. In the init.py file, add this line of text to the end and save it:
   ```python
   nuke.pluginAddPath('./SetLoop')
   ```

If you want to place the folder somewhere else than in the .nuke folder, make sure to change the path in the init.py file so that it points to that other path instead!

<br> 

## Installation using NukeShared

1. Place the SetLoop folder in the '_AutoInstaller' repository.

NukeShared is a way of installing plugins by dragging/dropping them in folders, [see my website (maxvanleeuwen.com/nukeshared)](https://maxvanleeuwen.com/nukeshared) for more information.

<br> 

## Updates

### v1.9
- Nuke 13 (Python 3) compatibility

### v1.8
- Added geo looping method
- Added feedback writing option (writing exr sequence, instead of copying nodes)
- Added custom offset to iteration after loop has been set

### v1.7
- Fixed error in Julia Set example
- Added extra Julia Set example

### v1.6
- Excluded backdrops from loops
- Improved Mandelbrot examples, added Julia Set examples

### v1.5
- Fixed a bug in expression relinking
- Added 'remove '.parent'' option to help with expression relinking, if there are still issues
- Expression relinking now only applies to expressions in the Loop_End group (the invisible part of the loop)
- Loopcount offset can now be changed after the loop has been set
- Added 'operation' knob to set the merge operation in Parallel looping mode
- Added 'Motion Graphics' example template

### v1.4
- Fixed nodes connecting to other invisible nodes
- When installed, examples are included in the ToolSets menu
- Improved installation

### v1.3
- Fixed expression relinking issue
- Added warning when backdrop is not found, removed Nuke version check
- Tested on Linux
- Added more types of variables to the 'Constants' tab

### v1.2
- Added new method for looping ('parallel'), fixed compatibility with Nuke 11 (pyside2), added stats.

### v1.1
- Fixed a bug, cleaned UI, better tooltips.
