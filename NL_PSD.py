%PowerSpectralDensity
%!!!CHANGE the path of the files you need to analyze!!!
filestoanalyze= "C:\Users\jbroussard5\Desktop\NOVELLOCATION\NOVELLOCATION - Nex files\NOL*.nex"
numfiles=GetFileCount(filestoanalyze)

for iterations = 1 to numfiles
	name = GetFileName(iterations)
	doc=OpenDocument(name)
	Trace(name)

% Power Spectrum for Continuous Analysis for Running versus Resting

DeselectAll(doc)
SelectVar(doc,Down1,Continuous)
SelectVar(doc,Down2,Continuous)
SelectVar(doc,Down3,Continuous)
SelectVar(doc,Down4,Continuous)
SelectVar(doc,Down5,Continuous)
SelectVar(doc,Down6,Continuous)
SelectVar(doc,Down7,Continuous)
SelectVar(doc,Down8,Continuous)
SelectVar(doc,Down9,Continuous)
SelectVar(doc,Down10,Continuous)
SelectVar(doc,Down11,Continuous)
SelectVar(doc,Down12,Continuous)
SelectVar(doc,Down13,Continuous)
SelectVar(doc,Down14,Continuous)
SelectVar(doc,Down15,Continuous)
SelectVar(doc,Down16,Continuous)
SelectVar(doc,Down17,Continuous)
SelectVar(doc,Down18,Continuous)
SelectVar(doc,Down19,Continuous)
SelectVar(doc,Down20,Continuous)
SelectVar(doc,Down21,Continuous)
SelectVar(doc,Down22,Continuous)
SelectVar(doc,Down23,Continuous)
SelectVar(doc,Down24,Continuous)
SelectVar(doc,Down25,Continuous)
SelectVar(doc,Down26,Continuous)
SelectVar(doc,Down27,Continuous)
SelectVar(doc,Down28,Continuous)
SelectVar(doc,Down29,Continuous)
SelectVar(doc,Down30,Continuous)
SelectVar(doc,Down31,Continuous)
SelectVar(doc,Down32,Continuous)



%ModifyTemplate(doc, "Power
%ModifyTemplate(doc, "PerieventRasters", "XMax (sec)", "1")
%ModifyTemplate(doc, "PerieventRasters", "Bin (sec)", "0.1")
%ModifyTemplate(doc, "PerieventRasters", "Normalization", "Spikes/Sec")
%ModifyTemplate(doc, "PerieventRasters", "Reference", GetName(doc.NL))

%Early Contextual fear tone respose (first 18min) from min 2 to 20 min
%ModifyTemplate(doc, "PerieventRasters", "Select Data", "All")

ApplyTemplate(doc,"PowerSpectralDensity")

%this will open an excel file with early tone response
%ALWAYS RENAME THE FILE  in the line below, if not you will overwrite or merge with previous file.
SendResultsToExcel(doc,"C:\Users\jbroussard5\Desktop\NOVELLOCATION\NL", "NL", 1, "CellNameStuff",1,1)

end