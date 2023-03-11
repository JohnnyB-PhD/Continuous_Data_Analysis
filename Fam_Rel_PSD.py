%PowerSpectralDensity
%!!!CHANGE the path of the files you need to analyze!!!
filestoanalyze= "C:\Users\jbroussard5\Desktop\NOVELLOCATION\NOVEL_LOCATION_NEX\NOL*.nex5"
numfiles=GetFileCount(filestoanalyze)

for iterations = 1 to numfiles
	name = GetFileName(iterations)
	doc=OpenDocument(name)
	Trace(name)

% Power Spectrum for Continuous Analysis for Running versus Resting

DeselectAll(doc)
SelectVar(doc,1,"continuous")
SelectVar(doc,2,"continuous")
SelectVar(doc,3,"continuous")
SelectVar(doc,4,"continuous")
SelectVar(doc,5,"continuous")
SelectVar(doc,6,"continuous")
SelectVar(doc,7,"continuous")
SelectVar(doc,8, "continuous")
SelectVar(doc,9, "continuous")
SelectVar(doc,10, "continuous")
SelectVar(doc,11, "continuous")
SelectVar(doc,12, "continuous")
SelectVar(doc,13, "continuous")
SelectVar(doc,14, "continuous")
SelectVar(doc,15, "continuous")
SelectVar(doc,16, "continuous")
SelectVar(doc,17, "continuous")
SelectVar(doc,18, "continuous")
SelectVar(doc,19, "continuous")
SelectVar(doc,20, "continuous")
SelectVar(doc,21, "continuous")
SelectVar(doc,22, "continuous")
SelectVar(doc,23, "continuous")
SelectVar(doc,24, "continuous")
SelectVar(doc,25, "continuous")
SelectVar(doc,26, "continuous")
SelectVar(doc,27, "continuous")
SelectVar(doc,28, "continuous")
SelectVar(doc,29, "continuous")
SelectVar(doc,30, "continuous")
SelectVar(doc,31, "continuous")
SelectVar(doc,32, "continuous")
SelectVar(doc,33, "continuous")
SelectVar(doc,34, "continuous")

%ModifyTemplate(doc, "PowerSpectralDensity", "Interval Filter", "Running,Resting") 
%ModifyTemplate(doc, "PerieventRasters", "XMax (sec)", "1")
%ModifyTemplate(doc, "PerieventRasters", "Bin (sec)", "0.1")
%ModifyTemplate(doc, "PerieventRasters", "Normalization", "Spikes/Sec")
%ModifyTemplate(doc, "PerieventRasters", "Reference", GetName(doc.NL))

%Early Contextual fear tone respose (first 18min) from min 2 to 20 min
%ModifyTemplate(doc, "PerieventRasters", "Select Data", "All")

ApplyTemplate(doc,"Fam_Rel_PSD")

%this will open an excel file with early tone response
%ALWAYS RENAME THE FILE  in the line below, if not you will overwrite or merge with previous file.
SendResultsToExcel(doc,"C:\Users\jbroussard5\Desktop\NOVELLOCATION\NL", "Filename", 1, "CellNameStuff",1,1)

end
%ModifyTemplate(doc, "PowerSpectralDensity", "Interval Filter", "Running,Resting") 