"""

   This routine reads the SPLUS ASCII catalogues and
   save it into FITS format. 

                    Costa-Duarte, M. V. - 08/06/2018

"""
from astropy.io import fits, ascii
import numpy as np
import sys
# Input file (ASCII)
infile_cat = str(sys.argv[1]) #'SPLUS_STRIPE82-0003_photo_BPZ.cat'
# Output file (FITS)
outfile_fits = infile_cat.replace('.cat', '.fits')

if __name__ == '__main__':

    
	# Loading ASCII catalogue
    
    print("Loading...%s" % infile_cat)
    data = ascii.read(infile_cat)

    # Saving FITS file

    print("Saving...%s" % outfile_fits)
    data.write(outfile_fits, format = 'fits', overwrite = True)
