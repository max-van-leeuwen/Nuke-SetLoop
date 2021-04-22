# Max van Leeuwen - maxvanleeuwen.com/setloop
# twitter @maksvanleeuwen
# SetLoop 1.9




#imports
import re
import time
import nuke
import os




# console
SetLoopPrint = '[SetLoop] '


# placeholders
nodestolink = None
loopbegin = None

SetLoopWriterPrint = 0
iterationCount = 0
digitCount = 0
dirPath = 0
fname = 0




# reusables
liveModeText = 'in this group node (live)'
noBdMessage = "Backdrop not found! Make sure it is big enough to fit the whole loop!\nIf this is already the case, please make the backdrop slightly bigger to be sure."




# get current node
n = nuke.thisNode()




def updateWriterData():

	global iterationCount
	global digitCount
	global dirPath
	global fname


	# custom iteration count
	iterationCount = int(n['loops'].getValue())

	# make digit count (4 at least) (+1 because first frame should be 1, so iteration count stays the same - this is purely for file name purposes)
	digitCount = len( str( iterationCount+1))
	digitCount = 4 if digitCount < 4 else digitCount

	# folder to save files (/##...##.exr) to
	dirPath = os.path.dirname(n['dirPath'].getValue())

	# stand-in user name (##...##.exr)
	fname = ''
	for i in range(digitCount):
		fname += '#'
	fname = fname + '.exr'




# get node start
def getNodeStart():

	global loopbegin

	# create variable for future backdrop node
	bd = None
	loopbegin = None

	# make list of nodes in main graph
	n.end()
	allExistingNodes = nuke.allNodes()

	for i in allExistingNodes:
		
		if i.knob('SetLoop_bd'):

			# define a possible backdrop
			pbd = i
			left = pbd['xpos'].value()
			top = pbd['ypos'].value() + 20
			pbd_Width = pbd['bdwidth'].value()
			pbd_Height = pbd['bdheight'].value()
			right = left + pbd_Width - 80

			# get backdrop dimensions
			bottom = top - 20 + pbd_Height - 40

			# if this node is within dimensions of pbd
			if n['xpos'].value() > left and n['xpos'].value() < right and n['ypos'].value() > top and n['ypos'].value() < bottom:
				bd = pbd


	if bd is None:
		nuke.message(noBdMessage)

	# if backdrop was found
	else:
		for i in allExistingNodes:

			left = bd['xpos'].value()
			top = bd['ypos'].value() + 20
			bd_Width = bd['bdwidth'].value()
			bd_Height = bd['bdheight'].value()
			right = left + bd_Width - 80

			# get backdrop dimensions
			bottom = top - 20 + bd_Height - 40

			for i in nuke.allNodes():

				# get all nodes in backdrop
				if i['xpos'].value() > left and i['xpos'].value() < right and i['ypos'].value() > top and i['ypos'].value() < bottom and i != n:
					if i.knob('loopbegin'):
						loopbegin = i

	return loopbegin



# function that enables/disables and hides/unhides knobs associated with feedback writing
def feedbackWriterKnobs(n, onOff):

	n['relinkextinputs'].setVisible(not onOff)
	n['relinkextexpressions'].setVisible(not onOff)
	n['removeexprparent'].setVisible(not onOff)
	n['addIterationKnob'].setVisible(not onOff)
	n['datatype'].setVisible(onOff)
	n['dirPath'].setVisible(onOff)
	n['onFrame'].setVisible(onOff)
	n['iteration'].setVisible(onOff)
	n['startFeedback'].setVisible(onOff)
	n['readFeedback'].setVisible(onOff)
	n['set'].setVisible(not onOff)
	n['stats'].setVisible(not onOff)
	n['lineScroll'].setVisible(not onOff)
	n['scroll'].setVisible(not onOff)
	n['empty2'].setVisible(not onOff)
	n['invert'].setVisible(not onOff)
	n['empty3'].setVisible(not onOff)
	n['blend'].setVisible(not onOff)
	n['spread'].setVisible(not onOff)
	n['parallelOperation'].setVisible(not onOff)
	n['offset'].setVisible(not onOff)




def startFeedback(EndLoopNode):

	# set current node
	global n
	n = EndLoopNode
	
	# make vars
	updateWriterData()


	q = nuke.ask("Start feedback write? Writing " + str(iterationCount) + " file(s) to\n" + dirPath + '/' + fname)


	if q:
		
		# get the loop start node
		nodeStart = getNodeStart()
		
		nodeStart.begin()

		# switch that switches from 0 to 1 after the first iteration (for base image)
		switchNode = nuke.toNode('FeedbackSwitch')

		# sread node that updates with latest iteration
		readNode = nuke.toNode('FeedbackReader')

		nodeStart.end()


		# custom frame to render
		onFrame = int(n['onFrame'].getValue())

		# make task
		t = nuke.ProgressTask("feedback write")

		# go into group
		n.begin()

		# empty
		for i in nuke.allNodes():
			nuke.delete(i)

		# make input, output
		inp = nuke.nodes.Input()
		outp = nuke.nodes.Output()

		# make write
		writeNode = nuke.nodes.Write()
		writeNode.setInput(0, inp)
		outp.setInput(0, writeNode)
		writeNode['channels'].setValue('all')
		writeNode['file_type'].setValue('exr')
		writeNode['datatype'].setValue(n['datatype'].value())
		writeNode['raw'].setValue(True)
		writeNode['name'].setValue('FeedbackWriter')
		writeNode['tile_color'].setValue(0xa50000ff)


		# for each iteration
		for i in range(iterationCount):

			# user cancellation
			if t.isCancelled():
				nuke.message('Cancelled')
				break
				

			# set progress
			p = int((i / iterationCount) * 100)
			t.setProgress(p)
			t.setMessage("iteration " + str(i) + '/' + str(iterationCount-1))


			# switch
			if(i == 0):

				switchNode['which'].setValue(0)
			else:

				switchNode['which'].setValue(1)


			# iteration knob
			n['iteration'].setValue(i)


			# convert write path to string, append extension
			newV = dirPath + '/' + str(i+1).zfill(digitCount) + '.exr'

			# update write file path
			writeNode['file'].setValue(newV)

			# execute write node for one frame (at frame)
			nuke.execute(writeNode, onFrame, onFrame, 1)

			# print log
			print(SetLoopPrint + 'written iteration ' + str(i) + '/' + str(iterationCount-1) + ':')
			print(SetLoopPrint + newV)
			print('')

			# update read node
			readNode['file'].setValue(newV)


			# end task
			if(i==iterationCount-1):
				t.setProgress(100)



		# reset write node, leave exr in file name to keep datatype knob
		writeNode['file'].setValue('.exr')

		# reset switch and read path
		readNode['file'].setValue('')
		switchNode['which'].setValue(0)

		# reset iteration count
		n['iteration'].setValue(0)

		# stop group
		n.end()

		# read files
		getFeedback(n)

		# set label
		n['label'].setValue('baked iterations: ' + str(iterationCount))




def getFeedback(n):

	# make vars
	updateWriterData()

	# if still in the group, end
	n.end()

	# make read node when finished
	newRead = nuke.nodes.Read(file=(dirPath + '/' + fname), first=1, last=(iterationCount))
	newRead.setXpos(n.xpos())
	newRead.setYpos(n.ypos() + 100)
	newRead['selected'].setValue(True)
	newRead['raw'].setValue(True)




# on knob change
def onKnobChanged(n, k):

	if k.name() == 'spread':

		# do not allow spread to go under 1
		if n['spread'].value() < 1:
			n['spread'].setValue(1)


	if k.name() == 'blend':

		# disable spread if not relevant
		n['spread'].setEnabled( n['blend'].value() and n['method_storage'].value() == 'parallel')


	if k.name() == 'method':

		# disable buildMethod if not in sequential method
		if(n['method'].value() == 'sequential'):

			n['buildMethod'].setEnabled(True)

		else:

			n['buildMethod'].setEnabled(False)
			n['buildMethod'].setValue(liveModeText)
			feedbackWriterKnobs(n, False)


	if k.name() == 'buildMethod':

		# show regular knobs
		if(n['buildMethod'].value() == liveModeText):

			feedbackWriterKnobs(n, False)

		# show feedback writer knobs
		else:

			feedbackWriterKnobs(n, True)




# main function for building loops (live mode)
def set(EndLoopNode):

	# set current node
	global n
	n = EndLoopNode


	# PySide for nuke 10 and earlier
	try:

		from PySide import QtGui

		# get clipboard functions
		clipboard = QtGui.QApplication.clipboard()

	#PySide 2 compatibility
	except:

		from PySide2 import QtWidgets

		# get clipboard functions
		clipboard = QtWidgets.QApplication.clipboard()


	
	global nodestolink
	global loopbegin



	def ask_TakesTooLong(totalNodeCount):
		
		# >1000 nodes may take a minute, ask confirmation and show estimate of amount of nodes to be made
		return nuke.ask('This might take a little longer (about ' + str(totalNodeCount) + ' nodes are to be created!)')



	def ask_YouSure():

		# general confirmation
		return nuke.ask('Are you sure you want to create a new loop?')



	def ask_Clear():

		# remove existing loop
		return nuke.ask('No nodes are to be looped, this will only clear the existing loop. Are you sure?')



	def updateKnobs():

		maxscroll = loops_int
		if maxscroll < 1:
			maxscroll == 1
			
		if loopmethod == 'sequential':

			n['scroll'].setEnabled(True)
			n['invert'].setEnabled(False)
			n['spread'].setEnabled(False)
			n['blend'].setEnabled(True)
			n['parallelOperation'].setEnabled(False)
		

		elif loopmethod == 'parallel':

			n['blend'].setEnabled(True)
			n['scroll'].setEnabled(True)
			n['invert'].setEnabled(True)
			n['parallelOperation'].setEnabled(True)


		elif loopmethod == 'geometry':

			n['scroll'].setEnabled(True)
			n['invert'].setEnabled(False)
			n['spread'].setEnabled(False)
			n['blend'].setEnabled(False)
			n['parallelOperation'].setEnabled(False)


		n['scroll'].setRange(0, maxscroll)


		if n['scroll'].getValue() > n['scroll'].max():
			n['scroll'].setValue( n['scroll'].max() )


		# enable offset knob and set range when iteration is enabled
		if(n['addIterationKnob'].value()):
			n['offset'].setEnabled(True)
			n['offset'].setRange(-loops, loops)
		else:
			n['offset'].setEnabled(False)




	def setloop():

		global nodestolink
		global loopbegin


		# TCL expression for multiply node in parallel loop
		parallelMultExpr = """clamp(
								parent.scroll > (parent.invert ? loops - (iteration - parent.offset) : (iteration - parent.offset)) ?
									((parent.blend ? parent.scroll : floor(parent.scroll)) - (parent.invert ? loops - (iteration - parent.offset) : (iteration - parent.offset))) / (parent.blend ? parent.spread : 1) : 0 > 1)
						   """


		# get name of node directly after Loop_Begin
		nameoffirstnode = ''
		for a in loopbegin.dependent():
			nameoffirstnode = a.name()

		# check if it worked
		if nameoffirstnode == '': 
			for a in loopbegin.dependent():
				# if not, just try this again, somehow this may fail the first time
				nameoffirstnode = a.name()

			# let's try again some other time if it's not working
			if nameoffirstnode == '':
				nuke.message('something went wrong - please try one more time!')
				return
		

		# create input node in group
		nuke.nodes.Input()

		# create input for original in parallel
		parallelInp = None
		parallelInpIndex = 0
		if loopmethod == 'parallel' or loopmethod == 'geometry':
			parallelInp = nuke.nodes.Input()
			parallelInp['name'].setValue('bypass')
			parallelInpIndex = 1
		

		if loopmethod == 'sequential':
			# create first dot and link to input
			newdot = nuke.nodes.Dot()
			newdot['name'].setValue('LoopAnchor_0')
			newdot.setInput(0, nuke.toNode('Input1'))
			
			# deselect input1
			nuke.toNode('Input1')['selected'].setValue(False)

			# select first dot
			newdot['selected'].setValue(True)
			

		# there's always one input already, except if bypass is also there
		newinputs = []
		count = 1 + parallelInpIndex
		previnputs = []


		# get all nodes to relink after creating the loop
		for anode in nodestolink:
			if anode in previnputs:
				newinputs.append(anode + ' ' + str(count))
			else:
				previnputs.append(anode)
				newinput = nuke.nodes.Input()
				newinput['name'].setValue(anode)
				newinputs.append(anode + ' ' + str(count))
				count+=1


		for i in range(loops_int - 1 if loopmethod == 'parallel' or loopmethod == 'geometry' else loops_int):

			# paste nodes in loop once
			nuke.nodePaste('%clipboard%')


			# relink externally referencing expressions from inside the loop
			if n['relinkextexpressions'].value():

				# for each node in the loop
				for selNode in nuke.selectedNodes():

					# list each knob
					for k in selNode.knobs().keys():

						# get expression count in knob
						exprList = selNode[k].getValue()
						if not (type(exprList) == type([])):
							exprList = [exprList]

						count = len(exprList)


						for c in range(count):

							# for each knob with an expression at index c
							if selNode[k].hasExpression(c):

								# example expression
								# '(parent.Blur1.size)/2 + root.Blur1.size/Merge1.mix*16'


								oExpression = selNode[k].animation(c).expression()

								# new expression placeholder
								nExpression = oExpression



								# filter by inverse of [a-z, A-Z, 0-9, _, .]
								chars = r"[^a-zA-Z0-9_.]"
								string = nExpression

								# make list of splits by chars
								# ['', 'parent.Blur1.size', '', '2', '', '', 'root.Blur1.size', 'Merge1.mix', '16']
								NodeKnobCombo = re.split(chars, string)

								# make list of indexes of splits
								# [0, 18, 19, 21, 22, 23, 39, 50, 53]
								indexes = []
								for m in re.finditer(chars, string):
									indexes.append(m.start())
								indexes.append(len(string))
									

								# make list of items and their starting indexes
								# [['', 0], ['parent.Blur1.size', 1], ['', 19], ['2', 20], ['', 22], ['', 23], ['root.Blur1.size', 24], ['Merge1.mix', 40], ['16', 51]]
								ItemIndexes = []
								count = 0
								for nkC in NodeKnobCombo:
									ItemIndexes.append([nkC, indexes[count] - len(nkC)])
									count += 1


								# make list of supposed nodes and their indexes
								# [['parent', 1], ['root', 24], ['Merge1', 40]]
								NodesIndexes = []
								for item in ItemIndexes:
									nodeName = item[0].split('.')

									# only if a knob is called for this supposed node (by checking if a dot is splitting the string)
									if len(nodeName) > 1:
										NodesIndexes.append([nodeName[0], item[1]])


								# make list of indexes to add 'root.'
								# [1, 24, 40]
								indexList = []
								for eachIndex in NodesIndexes:
									# add it to the list
									indexList.append(eachIndex[1])
								# add last character to list
								indexList.append( len(nExpression) )


								# make list of original expression, split by indexes
								# ['(', 'parent.Blur1.size)/2 + ', 'root.Blur1.size/', 'Merge1.mix*16']
								parts = []
								previndex = 0
								for eachIndex in indexList:
									parts.append( nExpression[previndex:eachIndex] )
									previndex = eachIndex


								# make new list of 'root.' items, same count as len(parts) (so they can be zipped together later)
								# ['', '', '', '']
								items = []
								curritem = 0
								for part in parts:

									# item to add in front of each split
									item = ''

									# skip entirely if it starts with 'root.'
									if not part.startswith('root.'):

										# remove 'parent.' if the following node is in the main graph, or if the following node is the EndLoop node
										if part.split('.')[0] == 'parent':
											if (part.split('.')[1] in nodesoutsidebd) or (part.split('.')[1] == thisnode):
												parts[curritem] = parts[curritem].replace('parent.', '')
												part = parts[curritem]

										# skip if node does not exist outside of backdrop
										if part.split('.')[0] in nodesoutsidebd:
											item = 'root.'
									

									items.append(item)
									curritem += 1


								# zip together
								# [('', '('), ('', 'parent.Blur1.size)/2 + '), ('', 'root.Blur1.size/'), ('', 'Merge1.mix*16')]
								finalExpressionList = zip(items, parts)
								finalExpression = ''


								# join all together for final string
								# '(parent.Blur1.size)/2 + root.Blur1.size/Merge1.mix*16'
								for eachItem in finalExpressionList:
									finalExpression += eachItem[0] + eachItem[1]

								# pass on to nExpression
								nExpression = finalExpression



								# set new expression at index c
								selNode[k].setExpression(nExpression, c)


								# on first iteration, print expression relinks
								if (i == 0) and not (oExpression == nExpression):
									print('')
									print(SetLoopPrint + 'Re-wrote expression in loop for ' + selNode.name() + '.' + k + '[' + str(c) + '], from/to:')
									print(SetLoopPrint + '-')
									print(SetLoopPrint + oExpression)
									print(SetLoopPrint + nExpression)
									print('')



			# for each node in the loop
			for selNode in nuke.selectedNodes():

				# if relinkextinputs
				if len(nodestolink) > 0:
					# check if this knob is present
					if selNode.knob(nodename_input):

						# check every knob for value
						for aknob in selNode.knobs():
							if aknob == nodename_input:

								# sometimes the string is empty, ignore those
								try:
									# link to correct input-node, read from knob
									selNode.setInput(int(selNode[aknob].value().split()[1]), nuke.toNode(selNode[aknob].value().split()[0]))
								except:
									pass

								# remove knob
								selNode.removeKnob(selNode[nodename_input])



				if selNode.knob(connectedtofirst):

					if loopmethod=='sequential':
						# connect the right node to the anchor dot
						selNode.setInput(int(selNode[connectedtofirst].value()), nuke.toNode('LoopAnchor_' + str(i)))

					if loopmethod=='parallel':
						# connect to parallelInp
						selNode.setInput(int(selNode[connectedtofirst].value()), parallelInp)

					if loopmethod=='geometry':
						# connect to parallelInp
						selNode.setInput(int(selNode[connectedtofirst].value()), parallelInp)

					# remove the knob for first input
					selNode.removeKnob(selNode[connectedtofirst])

					# remove the entire tab if no other useful knobs are there anymore
					if selNode.knob(customtabname) and not selNode.knob(iterationKnob):
						selNode.removeKnob(selNode[customtabname])
			
			
			# add dots (anchors) inbetween loops for extra control  
			newdot = nuke.nodes.Dot()    

			if n['addIterationKnob'].value():
				for j in nuke.selectedNodes():
					# set iteration values on knobs, +1 because the original tree in the main graph is also part of the loop
					j[iterationKnob].setExpression(str(i + 1) + ' + parent.offset')

			newdot['name'].setValue('LoopAnchor_' + str(i + 1))

			
			# make list of all nodes in group
			listofnodes = []
			for k in nuke.allNodes():
				listofnodes.append(k.name())

			# connect the new dot to the newest node
			newdot.setInput(0, nuke.toNode(listofnodes[1])) 
			newdot['selected'].setValue(True)


			# if parallel, make a grade node to blend iterations
			if loopmethod == 'parallel':

				fadeout = nuke.nodes.Grade(name='SetLoop_FadeOut_LoopAnchor_' + str(i), channels='all')
				fadeout.setInput(0, nuke.toNode('LoopAnchor_' + str(i)) if i > 0 else nuke.toNode('Input1'))
				fadeout.addKnob(nuke.Tab_Knob(customtabname,customtabname))
				fadeout.addKnob(nuke.Double_Knob(iterationKnob))
				fadeout[iterationKnob].setExpression(str(i) + ' + parent.offset')

				# set the blending expression
				fadeout['multiply'].setExpression(parallelMultExpr)


			# if geometry, make a switch node to remove iterations through scroll
			if loopmethod == 'geometry':

				switchgeo = nuke.nodes.Switch(name='SetLoop_Switch_LoopAnchor_' + str(i))
				switchgeo.setInput(0, nuke.toNode('LoopAnchor_' + str(i)) if i > 0 else nuke.toNode('Input1'))
				switchgeo['which'].setExpression('parent.scroll > ' + str(i) + ' ? 0 : 1')


		# grade node for blending needs to be made one more time after the loop
		if loopmethod == 'parallel':

			fadeout = nuke.nodes.Grade(name='SetLoop_FadeOut_LoopAnchor_' + str(i + 1), channels='all')
			fadeout.setInput(0, nuke.toNode('LoopAnchor_' + str(i + 1)))
			fadeout.addKnob(nuke.Tab_Knob(customtabname,customtabname))
			fadeout.addKnob(nuke.Double_Knob(iterationKnob))
			fadeout[iterationKnob].setExpression(str(i + 1) + ' + parent.offset')

			fadeout['multiply'].setExpression(parallelMultExpr)


		# switch node for geo needs to be made one more time after the loop
		if loopmethod == 'geometry':

			switchgeo = nuke.nodes.Switch(name='SetLoop_Switch_LoopAnchor_' + str(i + 1))
			switchgeo.setInput(0, nuke.toNode('LoopAnchor_' + str(i + 1)))
			switchgeo['which'].setExpression('parent.scroll > ' + str(i + 1) + ' ? 0 : 1')



		toswitch = []
		for j in nuke.allNodes():

			if loopmethod == 'parallel':
				if j.name().find('SetLoop_FadeOut_LoopAnchor_') != -1:

					# get all grades
					toswitch.append(j.name())


			elif loopmethod == 'sequential':
				if j.name().find('LoopAnchor_') != -1:

					# get all dots
					toswitch.append(j.name())


			elif loopmethod == 'geometry':
				if j.name().find('SetLoop_Switch_LoopAnchor_') != -1:

					# get all grades
					toswitch.append(j.name())

		

		if loopmethod == 'sequential':   

			lookat=nuke.nodes.Dissolve()

			counter=0
			for k in toswitch:

				# connect to the dissolve, but skip its mask input
				lookat.setInput(counter if counter < 2 else counter + 1, nuke.toNode(k))
				counter+=1   
				

			# create the switch and link all dots
			lookat['which'].setExpression('parent.loops - (parent.blend ? parent.scroll : floor(parent.scroll))')

			firstnode = nuke.toNode(nameoffirstnode)

			# dot connected
			firstnode.setInput(0, nuke.toNode('LoopAnchor_1'))

			# make output in group
			nuke.nodes.Output()

			# Output1 to switch
			nuke.toNode('Output1').setInput(0, nuke.toNode('Dissolve1'))


		elif loopmethod=='parallel':

			lookat=nuke.nodes.Merge2()
			lookat['operation'].setExpression('parallelOperation',0)
			
			toswitch.reverse()
			counter=0
			for k in toswitch:

				# connect the merge, but skip its mask input
				inputnum = counter if counter < 2 else counter + 1
				lookat.setInput(inputnum, nuke.toNode(k))
				counter+=1

			# make output in group
			nuke.nodes.Output()

			# Output1 to Merge
			nuke.toNode('Output1').setInput(0, lookat)


		elif loopmethod=='geometry':

			lookat=nuke.nodes.Scene()

			toswitch.reverse()
			counter = 0
			for k in toswitch:

				# connect to scene inputs
				lookat.setInput(counter, nuke.toNode(k))
				counter+=1

			# make output in group
			nuke.nodes.Output()

			# Output1 to Merge
			nuke.toNode('Output1').setInput(0, lookat)
		

		# stats
		nodecount = len(nuke.allNodes())
		statstext = 'method:\t\t' + str(loopmethod) + '\nnodes in total:\t' + str(nodecount) + '\nnodes per loop:\t' + str(nodestoloop) + '\nloops:\t\t' + str(loops_int)
		n['stats'].setValue(statstext)


		# exit group
		n.end()


		# connect bypass of in parallel
		if loopmethod == 'parallel' or loopmethod == 'geometry':
			n.setInput(parallelInpIndex, loopbegin)


		if n['relinkextinputs'].value():

			for i in range(0, len(newinputs)):

				newinputsstr = newinputs[i].split()
				n.setInput(int(newinputsstr[1]), nuke.toNode(newinputsstr[0]))


			for j in nodesinbd:
				if j.knob(connectedtofirst):

					# remove connectedtofirst knob on original node in main graph
					j.removeKnob(j[connectedtofirst])


		# restore clipboard
		clipboard.setText(clipb)


		for i in nuke.selectedNodes():

			if i.knob(nodename_input):
				i.removeKnob(i[nodename_input])


			if i.knob(connectedtofirst):
				i.removeKnob(i[connectedtofirst])


			if i.knob(customtabname) and not i.knob(iterationKnob):
				# remove custom made tab if no other knobs are there anymore
				i.removeKnob(i[customtabname])



	def makeprogress(removeOnly):

		# make writable
		global nodestolink
		global loopbegin


		for i in nodesinbd:

			# get Loop_Begin
			if i.knob('loopbegin'):
				loopbegin = i
				i['selected'].setValue(False)

			# remove original iterationKnob
			if i.knob(iterationKnob):
				i.removeKnob(i[iterationKnob])


		# if 'parent.' should be removed from expressions in backdrop in the main graph
		if n['removeexprparent'].value():

			# for each node in the backdrop
			for selNode in nodesinbd:

				# list each knob
				for k in selNode.knobs().keys():

					# get expression count in knob
					exprList = selNode[k].getValue()
					if not (type(exprList) == type([])):
						exprList = [exprList]

					count = len(exprList)


					for c in range(count):

						# for each knob with an expression at index c
						if selNode[k].hasExpression(c):

							oExpression = selNode[k].animation(c).expression()

							# new expression placeholder
							nExpression = oExpression

							nExpression = nExpression.replace('parent.', '')


							# set new expression at index c
							selNode[k].setExpression(nExpression, c)


							# on first iteration, print expression relinks
							if not (oExpression == nExpression):
								print('')
								print(SetLoopPrint + 'Removed \'.parent\' in expression for ' + selNode.name() + '.' + k + '[' + str(c) + '], from/to:')
								print(SetLoopPrint + '-')
								print(SetLoopPrint + oExpression)
								print(SetLoopPrint + nExpression)
								print('')


		# make new knobs
		if n['relinkextinputs'].value():

			for node in nodesinbd:

				if node.name() != loopbegin.name():
					for i in range(0, node.inputs()):

						try:

							if (node.input(i) not in nodesinbd) and (nuke.exists(node.input(i).name())):

								# make tab
								if not node.knob(customtabname):
									node.addKnob(nuke.Tab_Knob(customtabname, customtabname))

								# make knob
								node.addKnob(nuke.String_Knob(nodename_input))
								# set knob value
								node[nodename_input].setValue(node.input(i).name() + ' ' + str(i))
								nodestolink.append(node.input(i).name())

						except:
							pass


		task = nuke.ProgressTask("SetLoop")
		if n['relinkextexpressions'].value():

			for eachN in nuke.allNodes(recurseGroups = False):
				allnodesinmaingraph.append(eachN.name())

		for i in range(0, 2):

			if i==0:
				task.setProgress(1)
				task.setMessage("removing old loop")

				if not removeOnly:

					if n['relinkextexpressions'].value():

						# add each node in the main graph that's not in bd, nor is it called thisNode.name() or bd.name()
						for h in allnodesinmaingraph:
							if (nuke.toNode(h) not in nodesinbd) and (h != thisnode) and (h != bd.name()):
								nodesoutsidebd.append(h)


					if n['addIterationKnob'].value():

						for i in nuke.selectedNodes():
							if not i.knob(iterationKnob):

								if not i.knob(customtabname):
									# make sure we're working in the custom tab
									i.addKnob(nuke.Tab_Knob(customtabname, customtabname))

								if not i.knob(iterationKnob):
									i.addKnob(nuke.Double_Knob(iterationKnob))

							i.knob(iterationKnob).setExpression(n.name() + '.offset')


					for selectednode in nuke.selectedNodes():

						for i in range(0,selectednode.inputs()):
							try:

								if selectednode.input(i).name() == loopbegin.name():

									if not selectednode.knob(customtabname) and not selectednode == n:
										# make sure we're working in the custom tab
										selectednode.addKnob(nuke.Tab_Knob(customtabname,customtabname))

									selectednode.addKnob(nuke.Int_Knob(connectedtofirst))

									# set value of knob on node that's connected to Loop_Begin to the input it is connected with
									selectednode[connectedtofirst].setValue(i)

							except:
								pass


					# set new clipboard
					nuke.nodeCopy('%clipboard%')


				else:

					# remove all inputs from EndLoop
					for j in range(0, n.inputs()):
						n.setInput(j, None)

					# reconnect to StartLoop
					n.setInput(0, loopbegin)


				# get all variable inputs
				for k in range(1, n.inputs()):

					# and remove them
					n.setInput(k, None)


				# dive into group
				n.begin()

				# delete previous contents
				for j in nuke.allNodes():
					nuke.delete(j)

				if removeOnly:
					inp = nuke.nodes.Input()
					outp = nuke.nodes.Output()
					outp.setInput(0, inp)


			elif i == 1:

				if not removeOnly:
					task.setProgress(50)
					task.setMessage("creating new loop")
					setloop()
				break;

			if task.isCancelled():

				nuke.message('Looping cancelled!')
				task.setProgress(100)
				break;

			time.sleep(.5)
			
			# store the newest baked method
			n['method_storage'].setValue(loopmethod)

			# update the knobs in the UI
			updateKnobs()

			# set label
			n['label'].setValue('iteration: [value scroll]')



	def cleargroup():

		# dive into group
		n.begin()

		# delete previous contents
		for i in nuke.allNodes():
			nuke.delete(i)



	n.end()

	thisnode = n.name()

	# get the method for looping nodes
	loopmethod = n['method'].value()

	# get amount of loops
	loops = float(n['loops'].value())
	loops_int = int(loops)

	maxscroll = loops + 1 if loopmethod == 2 else loops
	if maxscroll < 1:
		maxscroll == 1

	# save the original clipboard
	clipb = clipboard.text()

	# global variable for all nodes
	allnodesinmaingraph = []

	# make list of all nodes with expressions that should be relinked
	nodesoutsidebd = []

	connectedtofirst = 'SETLOOP_TEMP_CONNECTEDTOFIRST'
	nodename_input = 'SETLOOP_TEMP_NODENAMEINPUT'
	customtabname = 'setloop_tab'
	nodestolink = []

	# Set variable name
	iterationKnob = 'iteration'
	offset = int(n['offset'].value() if n['addIterationKnob'].value() else 0)

	# Set custom connector node for parallel method
	customlookat = 'Merge2'

	# create variable for future backdrop node
	bd = n 
	FoundOne = False

	# make list of nodes in main graph
	allExistingNodes = nuke.allNodes()

	for i in allExistingNodes:
		
		# deselect all
		i['selected'].setValue(False)

		if i.knob('SetLoop_bd'):

			# define a possible backdrop
			pbd = i
			left = pbd['xpos'].value()
			top = pbd['ypos'].value() + 20
			pbd_Width = pbd['bdwidth'].value()
			pbd_Height = pbd['bdheight'].value()
			right = left + pbd_Width - 80

			# get backdrop dimensions
			bottom = top - 20 + pbd_Height - 40

			# if this node is within dimensions of pbd
			if n['xpos'].value() > left and n['xpos'].value() < right and n['ypos'].value() > top and n['ypos'].value() < bottom:
				bd = pbd
				FoundOne = True

	# sometimes the backdrop is not big enough
	if not FoundOne:
		nuke.message(noBdMessage)

	else:

		left = bd['xpos'].value()
		top = bd['ypos'].value() + 20
		bd_Width = bd['bdwidth'].value()
		bd_Height = bd['bdheight'].value()
		right = left + bd_Width - 80

		# get backdrop dimensions
		bottom = top - 20 + bd_Height - 40

		# get first node
		loopbegin = n


		nodesinbd = []
		for i in nuke.allNodes():

			# get all nodes in backdrop
			if i['xpos'].value() > left and i['xpos'].value() < right and i['ypos'].value() > top and i['ypos'].value() < bottom and i != n:

				# do not loop Viewer nodes or StickyNote nodes
				if not i.Class() == 'Viewer' and not i.Class() == 'StickyNote' and not i.Class() == 'BackdropNode':
					i['selected'].setValue(True)
					nodesinbd.append(i)



		# for the stats
		nodestoloop = len(nuke.selectedNodes()) - 1
		totalNodeCount = nodestoloop * loops_int + (loops_int if loopmethod=='parallel' else 0)

		# when things could get heavy
		if totalNodeCount > 1000:
			if ask_TakesTooLong(totalNodeCount):
				makeprogress(False)


		elif nodestoloop > 0:
			if ask_YouSure():
				makeprogress(False)


		else:
			if ask_Clear():
				makeprogress(True)
				statstext = 'method:\t\t-\nnodes in total:\t0\nnodes per loop:\t0\nloops:\t\t0'
				n['stats'].setValue(statstext)
				n['method_storage'].setValue('')