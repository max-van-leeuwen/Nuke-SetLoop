try:

	import os

	# nodes toolbar
	nodes = nuke.menu('Nodes')

	# get python script location
	dirName = os.path.dirname( os.path.abspath(__file__) ).replace('\\', '/')

	# load SetLoop
	nodes.addCommand('Merge/SetLoop', "nuke.loadToolset('" + dirName + "/SetLoop.nk')", icon='Retime.png')

	# find all files in examples folder
	examplePath = dirName + '/Examples'
	for f in os.listdir(examplePath):
		if os.path.isfile(examplePath + '/' + f):

			# make examples group in toolsets
			group = nodes.addMenu('ToolSets/SetLoop Examples')

			# get name and extension
			nameSplit = f.split('.')

			# only look for nk
			if nameSplit[1] == 'nk':

				# get paths
				nkPath = examplePath + '/' + f
				pngPath = nkPath[:-3] + '.png'

				# add examples to node list
				group.addCommand(nameSplit[0] + ' (SetLoop example)', "nuke.loadToolset('" + nkPath + "')", icon=pngPath)

except Exception, e:
	print('SetLoop ToolSets failed to load. Error: \n' + str(e))