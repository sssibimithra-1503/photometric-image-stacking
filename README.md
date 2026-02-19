# photometric-image-stacking
Contains the pipeline for astronomical image stacking of JCBT photometric data.

Dependencies: tkinter,pyraf,re

This pipeline will match the coordinates, geometrically align them and then will statck the photometric data for the selected files. Able to select multiple files in a respective order and process them at once(ctrl+select files)

xyxy match(.coo extension files): 

Reference file - it reperesent the reference file to be selected from the list, it has to be constant for data observed on a particular day (able to select one file at once)

input file- it represent the input file to be selected from the list,have to match coordinates for all the files in the list with the reference file 

                                  
geomap(.coo extension files): input file- To select the output matched coordinate files, will give database file as output


geotran: 

fits file(.fits)- to select the preprocessed fits files

matched file(.coo)- to select the matched coordinate file
         
database file(.dat)- to select the datbase file
         
will create the aligned.fits file

         
imcombine: input file(.fits)- select the aligned fits file and the respective preprocessed fits file of the selected refernce file
