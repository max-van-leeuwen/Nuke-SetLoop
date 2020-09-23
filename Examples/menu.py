# this menu.py only installs the SetLoop examples.




# get script location (necessaary for loading toolsets)
dirName = os.path.dirname( os.path.abspath(__file__)).replace('\\', '/')

# get node toolbar
nodes = nuke.menu('Nodes')

# make group entry for examples in toolsets menu
group = nodes.addMenu('ToolSets/SetLoop Examples', index=2)



# make adding examples a function
def addExample(fileName, toolSetName):

	# add individual examples
	group.addCommand('(' + toolSetName + ') ' + fileName, "nuke.loadToolset('" + dirName + '/' + fileName + ".nk')", icon = fileName + '.png')



# add each  example
addExample('Geo Loop', 'SetLoop')
addExample('Motion Graphics', 'SetLoop')
addExample('Julia Set 1', 'SetLoop')
addExample('Julia Set 2', 'SetLoop')
addExample('Julia Set 3', 'SetLoop')
addExample('Mandelbrot 1', 'SetLoop')
addExample('Mandelbrot 2', 'SetLoop')
addExample('Reaction Diffusion 1', 'SetLoop')
addExample('Reaction Diffusion 2', 'SetLoop')
addExample('Reaction Diffusion 3', 'SetLoop')