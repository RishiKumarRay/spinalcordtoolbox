#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Crop atlas from the MNI-Poly-AMU template


import commands
import os
import getopt
import sys
status, path_sct = commands.getstatusoutput('echo $SCT_DIR')
sys.path.append(path_sct + '/scripts')
import sct_utils as sct

# params
# Old atlas created from the registration of all slices to the reference slice
# path_atlas = '/home/django/cnaaman/data/data_marc/WMtracts_outputstest/final_results/' # path of atlas
# New atlas created from the registration of all slices to the adjacent slice
folder_atlas = '/home/django/cnaaman/data/data_marc/WMtracts_outputsc_julien/final_results/'
folder_out = '/home/django/cnaaman/code/stage/cropped_atlas/'
verbose = 1
zind = 10,110,210,310,410
try:
    opts, args = getopt.getopt(sys.argv[1:], 'f:o:z:') # define flag
except getopt.GetoptError as err: # check if the arguments are defined
    print str(err) # error

for opt, arg in opts:
    if opt == '-f':
        folder_atlas = str(arg)
    if opt == '-o':
        folder_out = str(arg)
    if opt == '-z':
        zind = arg
        zind = zind.split(',')

def crop_file(fname_data, folder_out):
    # extract file name
    path_list, file_list, ext_list = sct.extract_fname(fname_data)
   
   # crop file with fsl, and then merge back
    cmd = 'fslmerge -z '+folder_out+file_list
    for i in zind:
        sct.run('fslroi '+fname_data+' z'+str(zind.index(i))+'_'+file_list+' 0 -1 0 -1 '+str(i)+' 1')
        cmd = cmd+' z'+str(zind.index(i))+'_'+file_list
    sct.run(cmd)
#    sct.run('fslroi '+fname_data+' z1_'+file_list+' 0 -1 0 -1 10 1')
#    sct.run('fslroi '+fname_data+' z2_'+file_list+' 0 -1 0 -1 110 1')
#    sct.run('fslroi '+fname_data+' z3_'+file_list+' 0 -1 0 -1 210 1')
#    sct.run('fslroi '+fname_data+' z4_'+file_list+' 0 -1 0 -1 310 1')
#    sct.run('fslroi '+fname_data+' z5_'+file_list+' 0 -1 0 -1 410 1')
#    sct.run('fslmerge -z '+folder_out+file_list+' '+'z1_'+file_list+' z2_'+file_list+' z3_'+file_list+' z4_'+file_list+' z5_'+file_list)
    # sct.run('fslroi '+fname_data+' z1_'+file_list+' 0 -1 0 -1 10 1')
    #  sct.run('fslroi '+fname_data+' z2_'+file_list+' 0 -1 0 -1 60 1')
    #  sct.run('fslroi '+fname_data+' z3_'+file_list+' 0 -1 0 -1 110 1')
    #  sct.run('fslroi '+fname_data+' z4_'+file_list+' 0 -1 0 -1 160 1')
    #  sct.run('fslroi '+fname_data+' z5_'+file_list+' 0 -1 0 -1 210 1')
    #  sct.run('fslroi '+fname_data+' z6_'+file_list+' 0 -1 0 -1 260 1')
    #  sct.run('fslroi '+fname_data+' z7_'+file_list+' 0 -1 0 -1 310 1')
    #  sct.run('fslroi '+fname_data+' z8_'+file_list+' 0 -1 0 -1 360 1')
    #  sct.run('fslroi '+fname_data+' z9_'+file_list+' 0 -1 0 -1 410 1')
    #  sct.run('fslroi '+fname_data+' z10_'+file_list+' 0 -1 0 -1 460 1')
    # sct.run('fslmerge -z '+folder_out+file_list+' '+'z1_'+file_list+' z2_'+file_list+' z3_'+file_list+' z4_'+file_list+' z5_'+file_list+' z6_'+file_list+' z7_'+file_list+' z8_'+file_list+' z9_'+file_list+' z10_'+file_list)
    
# create output folder
if os.path.exists(folder_out):
    sct.printv('WARNING: Output folder already exists. Deleting it...', verbose)
    sct.run('rm -rf '+folder_out)
sct.run('mkdir '+folder_out)

# get atlas files
status, output = sct.run('ls '+folder_atlas+'*.nii.gz', verbose)
fname_list = output.split()

# loop across atlas
for i in xrange(0, len(fname_list)):
    path_list, file_list, ext_list = sct.extract_fname(fname_list[i])
    crop_file(fname_list[i], folder_out)

