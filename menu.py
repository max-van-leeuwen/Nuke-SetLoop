# this menu.py only installs the SetLoop toolset. To remove the SetLoop examples, remove the menu.py in the Examples folder.


# get script location (necessary for loading toolsets)
dirName = os.path.dirname( os.path.abspath(__file__)).replace('\\', '/')

# get node toolbar
nodes = nuke.menu('Nodes')

# load toolset
nodes.addCommand('Merge/SetLoop', "nuke.loadToolset('" + dirName + "/SetLoop.nk')", icon='Retime.png')