import numpy as np
import h5py

def save_structure_hdf5(f, members, path_out):

    for i in range(len(members)):
        if isinstance(f[members[i]], h5py.Dataset) == True:
            outfile = members[i].replace('/', '.')    
            np.savetxt(path_out + outfile + '.dat', np.array(f[members[i]]), delimiter=' ') 
            print i, 'dataset=', members[i], 'saving file...', outfile
    return    
##############################################################

infile = 'file.hdf5'

path_out = './'

##############################################################

if __name__ == '__main__':

    # Generate some data

    x = np.arange(100).reshape(10, 10)
    y = np.random.normal(0., 1., 10)
    z = np.random.uniform(0., 1., 10)

    # Save HDF5 file

    f = h5py.File(infile, 'w')
    grp1 = f.create_group('group1')
    grp1.create_dataset('x', data = x)
    grp1.create_dataset('z', data = z)
    grp2 = f.create_group('group2')
    grp2.create_dataset('y', data = y)
    f.close()

    # Open HDF5 file and check hierarchy

    f = h5py.File(infile,'r')
    members = []
    f.visit(members.append)
    for i in range(len(members)):
        print i, members[i]

    # Save datasets into different files

    save_structure_hdf5(f, members, path_out)
