"""A library that contains functions for creating the BSDS test set."""

import numpy
import os
import pickle

import tools.tools as tls

def create_bsds(source_url, path_to_folder_rgbs, path_to_bsds, path_to_list_rotation, path_to_tar=''):
    """Creates the BSDS test set.
    
    100 BSDS RGB images are converted into luminance. The
    1st row and the 1st column of each luminance image are
    removed. Then, sideways luminance images are rotated.
    Finally, the BSDS test set is filled with the luminance
    images and it is saved.
    
    Parameters
    ----------
    source_url : str
        URL of the original BSDS dataset.
    path_to_folder_rgbs : str
        Path to the folder to which the original BSDS dataset
        (training RGB images and test RGB images) is extracted.
    path_to_bsds : str
        Path to the file in which the BSDS test
        set is saved. The path ends with ".npy".
    path_to_list_rotation : str
        Path to the file in which the list
        storing the indices of the rotated
        luminance images is saved. The path
        ends with ".pkl".
    path_to_tar : str, optional
        Path to the downloaded archive containing the original
        BSDS dataset. The default value is ''. If the path
        is not the default path, the archive is extracted
        to `path_to_folder_rgbs` before the function starts
        creating the BSDS test set.
    
    Raises
    ------
    RuntimeError
        If the number of BSDS RGB images to be
        read is not 100.
    ValueError
        If a RGB image is neither 481x321x3
        nor 321x481x3.
    
    """
    if os.path.isfile(path_to_bsds) and os.path.isfile(path_to_list_rotation):
        print('"{0}" and "{1}" already exist.'.format(path_to_bsds, path_to_list_rotation))
        print('Delete them manually to recreate the BSDS test set.')
    else:
        if path_to_tar:
            is_downloaded = tls.download_untar_archive(source_url,
                                                       path_to_folder_rgbs,
                                                       path_to_tar)
            if is_downloaded:
                print('Successfully downloaded "{}".'.format(path_to_tar))
            else:
                print('"{}" already exists.'.format(path_to_tar))
                print('Delete it manually to re-download it.')
        
        # The height and width of the luminance images we
        # feed into the autoencoders has to be divisible by 16.
        height_bsds = 321
        width_bsds = 481
        reference_uint8 = numpy.zeros((100, height_bsds - 1, width_bsds - 1), dtype=numpy.uint8)
        list_rotation = []
        
        # `os.listdir` returns a list whose order depends on the OS.
        # To make `create_bsds` independent of the OS, the output of
        # `os.listdir` is sorted.
        path_to_folder_test = os.path.join(path_to_folder_rgbs,
                                           'BSDS300/images/test/')
        list_names = tls.clean_sort_list_strings(os.listdir(path_to_folder_test),
                                                 'jpg')
        if len(list_names) != 100:
            raise RuntimeError('The number of BSDS RGB images to be read is not 100.')
        for i in range(100):
            path_to_file = os.path.join(path_to_folder_test,
                                        list_names[i])
            
            # `tls.read_image_mode` is not put into a `try` `except` clause
            # as each BSDS300 RGB image has to be read.
            rgb_uint8 = tls.read_image_mode(path_to_file,
                                            'RGB')
            
            # `tls.rgb_to_ycbcr` checks that the data-type of
            # its input array is equal to `numpy.uint8`. `tls.rgb_to_ycbcr`
            # also checks that its input array has 3 dimensions
            # and its 3rd dimension is equal to 3.
            luminance_uint8 = tls.rgb_to_ycbcr(rgb_uint8)[:, :, 0]
            (height_image, width_image) = luminance_uint8.shape
            if height_image == height_bsds and width_image == width_bsds:
                reference_uint8[i, :, :] = luminance_uint8[1:height_bsds, 1:width_bsds]
            elif width_image == height_bsds and height_image == width_bsds:
                reference_uint8[i, :, :] = numpy.rot90(luminance_uint8[1:width_bsds, 1:height_bsds])
                list_rotation.append(i)
            else:
                raise ValueError('"{0}" is neither {1}x{2}x3 nor {2}x{1}x3.'.format(path_to_file, height_bsds, width_bsds))
        
        numpy.save(path_to_bsds,
                   reference_uint8)
        with open(path_to_list_rotation, 'wb') as file:
            pickle.dump(list_rotation, file, protocol=2)


