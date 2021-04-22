<p style="color: #000000;"><span>See <a href="https://maxvanleeuwen.com/setloop" target="_blank">my website</a> for more information and examples!</span></p>
<p style="color: #000000;"> </p>
<p style="color: #000000;"><span style="color: #000000;"><br /><br /><br /><img src="https://maxvanleeuwen.com/wp-content/uploads/ReactionDiffusion.gif" alt="reaction diffusion in Nuke setloop" width="314" height="166" /><em><img src="https://maxvanleeuwen.com/wp-content/uploads/MotionGraphics.gif" alt="motion graphics nuke setloop loop nodes" width="215" height="165" /></em></span></p>
<p style="color: #000000;"><img src="https://maxvanleeuwen.com/wp-content/uploads/geo.gif" alt="setloop geo" width="275" height="240" /></p>
<p style="color: #000000;"> </p>
<p style="color: #000000;"><img src="https://maxvanleeuwen.com/wp-content/uploads/STILL_1-1.jpg" alt="example_1" width="292" height="292" /><img src="https://maxvanleeuwen.com/wp-content/uploads/JuliaSet.jpg" alt="julia set nuke feedback iterator" width="291" height="291" /></p>
<p style="color: #000000;"> </p>
<p><em>(Examples of looped geo, a Mandelbrot and a Julia set, and Reaction Diffusion - all done with SetLoop)</em></p>
<p> </p>
<p><span style="color: #000000;"> </span></p>
<p> </p>
<p> </p>
<p><span style="color: #000000;"><strong>SetLoop</strong></span></p>
<p> </p>
<p><span style="color: #000000;">SetLoop is a toolset for Nuke that can loop a set of nodes.</span><br /><span style="color: #000000;">It copies the nodes you place between StartLoop and EndLoop inside EndLoop (which is a group), and reconnects them properly.</span></p>
<p><span style="color: #000000;">But there are many more features to it which, combined, make this an actually functional node iterator that can render fractals (like the Julia set) and animated reaction diffusion entirely in Nuke.</span></p>
<p><span style="color: #000000;"> </span></p>
<p> </p>
<p style="color: #000000;"><img src="https://maxvanleeuwen.com/wp-content/uploads/SetLoop_01.png" alt="nuke setloop" /><img src="https://maxvanleeuwen.com/wp-content/uploads/SetLoop_02.png" alt="nuke setloop max van leeuwen" width="344" height="616" /></p>
<p style="color: #000000;"> </p>
<p style="color: #000000;"> </p>
<p style="color: #000000;"><span style="color: #000000;"> </span></p>
<p style="color: #000000;"> </p>
<p style="color: #000000;"> </p>
<p style="color: #000000;"><span>See my website (</span><a href="https://maxvanleeuwen.com/setloop">maxvanleeuwen.com/setloop</a><span>) for more information/examples!</span></p>
<p style="color: #000000;"> </p>
<p> </p>
<p> </p>
<p> </p>
<p> </p>
<p><span style="color: #000000;"><strong>Installation:</strong></span></p>
<p> </p>
<p><span style="color: #000000;">1. Place the SetLoop folder in your .nuke folder (or somewhere else on your computer).</span></p>
<p><span style="color: #000000;">2. Go to your .nuke folder, and create a file called 'init.py'. If such a file already exists, open it.</span></p>
<p><span style="color: #000000;">3. In the init.py file, add this line of text to the end and save it:</span></p>
<p> </p>
<p style="margin-left: 30px;"><span style="color: #000000;">nuke.pluginAddPath('./SetLoop')</span></p>
<p><span style="color: #000000;"> </span></p>
<p> </p>
<p><span style="color: #000000;">If you want to place the folder somewhere else than in the .nuke folder, make sure to change the path in the init.py file so that it points to that other path instead!</span></p>
<p> </p>
<p> </p>
<p> </p>
<p><span style="color: #000000;"><strong>Installation using NukeShared:</strong></span></p>
<p> </p>
<p><span style="color: #000000;">1. Place the SetLoop folder in the '_AutoInstaller' repository.</span></p>
<p> </p>
<p><span style="color: #000000;">NukeShared is a way of installing plugins by dragging/dropping them in folders, </span><a href="https://maxvanleeuwen.com/nukeshared" target="_blank">see my website (maxvanleeuwen.com/nukeshared)</a><span style="color: #000000;"> for more information.</span></p>
<p> </p>
<p> </p>
<p><span style="color: #000000;"> </span></p>
<p> </p>
<p><span style="color: #000000;"><strong>Updates</strong></span></p>
<p><span style="color: #000000;"> </span></p>
<p><span style="color: #000000;">v1.9</span></p>
<p style="margin-left: 30px;"><span style="color: #000000;">Nuke 13 (Python 3) compatibility</span></p>
<p><span style="color: #000000;">v1.8</span></p>
<p style="margin-left: 30px;"><span style="color: #000000;">added geo looping method</span><br /><span style="color: #000000;">added feedback writing option (writing exr sequence, instead of copying nodes)</span><br /><span style="color: #000000;">added custom offset to iteration after loop has been set</span></p>
<p><span style="color: #000000;">v1.7</span></p>
<p style="margin-left: 30px;"><span style="color: #000000;">Fixed error in Julia Set example</span><br /><span style="color: #000000;">Added extra Julia Set example</span></p>
<p><span style="color: #000000;">v1.6</span></p>
<p style="margin-left: 30px;"><span style="color: #000000;">Exluded backdrops from loops<br />Improved Mandelbrot examples, added Julia Set examples</span></p>
<p><span style="color: #000000;">v1.5</span></p>
<p style="margin-left: 30px;"><span style="color: #000000;">Fixed a bug in expression relinking</span><br /><span style="color: #000000;">Added 'remove '.parent'' option to help with expression relinking, if there are still issues</span><br /><span style="color: #000000;">Expression relinking now only applies to expressions in the Loop_End group (the invisible part of the loop)</span><br /><span style="color: #000000;">Loopcount offset can now be changed after the loop has been set</span><br /><span style="color: #000000;">Added 'operation' knob to set the merge operation in Parallel looping mode</span><br /><span style="color: #000000;">Added 'Motion Graphics' example template</span></p>
<p><span style="color: #000000;">v1.4</span></p>
<p style="margin-left: 30px;"><span style="color: #000000;">Fixed nodes connecting to other invisible nodes</span><br /><span style="color: #000000;">When installed, examples are included in the ToolSets menu</span><br /><span style="color: #000000;">Improved installation</span></p>
<p><span style="color: #000000;">v1.3</span></p>
<p style="margin-left: 30px;"><span style="color: #000000;">Fixed expression relinking issue<br />Added warning when backdrop is not found, removed Nuke version check<br />Tested on Linux<br />Added more types of variables to the 'Constants' tab<br /></span></p>
<p><span style="color: #000000;">v1.2</span></p>
<p style="margin-left: 30px;"><span style="color: #000000;">Added new method for looping ('parallel'), fixed compatibility with Nuke 11 (pyside2), added stats.</span></p>
<p><span style="color: #000000;">v1.1</span></p>
<p style="margin-left: 30px;"><span style="color: #000000;">Fixed a bug, cleaned UI, better tooltips.</span></p>