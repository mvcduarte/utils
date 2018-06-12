"""

   This routine reads the SPLUS ASCII catalogues and
   save it into FITS format. 

                    Costa-Duarte, M. V. - 08/06/2018

"""

from __future__ import print_function
from astropy.io import fits, ascii
import numpy as np
import sys
import glob

if __name__ == '__main__':

    # List of catalogue files at ./
      
    list_cat = glob.glob('SPLUS_STRIPE82-000*.cat')

    for i in range(len(list_cat)): # loop over all catalogue files

        # Define output file (FITS)
        outfile_fits = list_cat[i].replace('.cat', '.fits')
    	
        # Loading ASCII catalogue
        print("Loading...%s" % list_cat[i])
        data = ascii.read(list_cat[i])

        # Saving FITS file
        print("Saving...%s" % outfile_fits)
        data.write(outfile_fits, format = 'fits', overwrite = True)
