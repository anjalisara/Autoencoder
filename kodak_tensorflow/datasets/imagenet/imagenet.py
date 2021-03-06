"""A library that contains a function for creating the ImageNet training and validation sets."""

import numpy
import os

import tools.tools as tls

def create_imagenet(path_to_folder_rgbs, width_crop, nb_training, nb_validation, path_to_training, path_to_validation, path_to_tar=''):
    """Creates the ImageNet training and validation sets.
    
    The ImageNet RGB images are converted into
    luminance images. Then, the luminance images
    are cropped. Finally, the ImageNet training and
    validation sets are filled with the luminance
    crops and they are saved.
    
    Parameters
    ----------
    path_to_folder_rgbs : str
        Path to the folder storing ImageNet RGB images.
    width_crop : int
        Width of the crop.
    nb_training : int
        Number of luminance crops in
        the ImageNet training set.
    nb_validation : int
        Number of luminance crops in
        the ImageNet validation set.
    path_to_training : str
        Path to the file in which the
        ImageNet training set is saved.
        The path ends with ".npy".
    path_to_validation : str
        Path to the file in which the
        ImageNet validation set is saved.
        The path ends with ".npy".
    path_to_tar : str, optional
        Path to an archive containing ImageNet
        RGB images. The default value is ''. If
        the path is not the default path, the
        archive is extracted to `path_to_folder_rgbs`
        before the function starts creating the
        ImageNet training and validation sets.
    
    Raises
    ------
    RuntimeError
        If there are not enough ImageNet
        RGB images to create the ImageNet
        training and validation sets.
    
    """
    if os.path.isfile(path_to_training) and os.path.isfile(path_to_validation):
        print('"{0}" and "{1}" already exist.'.format(path_to_training, path_to_validation))
        print('Delete them manually to recreate the ImageNet training and validation sets.')
    else:
        if path_to_tar:
            tls.untar_archive(path_to_folder_rgbs,
                              path_to_tar)
        nb_total = nb_training + nb_validation
        
        # `width_crop` has to be divisible by 16.
        luminances_uint8 = numpy.zeros((nb_total, width_crop, width_crop, 1), dtype=numpy.uint8)
        
        # `os.listdir` returns a list whose order depends on the OS.
        # To make `create_bsds` independent of the OS, the output of
        # `os.listdir` is sorted.
        list_names = tls.clean_sort_list_strings(os.listdir(path_to_folder_rgbs),
                                                 ('jpg', 'JPEG', 'png'))
        i = 0
        for name in list_names:
            path_to_rgb = os.path.join(path_to_folder_rgbs,
                                       name)
            
            # If the condition below is met, the result of
            # the processing of `rgb_uint8` is added to the
            # ImageNet training set. Otherwise, the result
            # the processing of `rgb_uint8` is added to the
            # ImageNet validation set.
            if i < nb_training:
                is_random = True
            else:
                is_random = False
            try:
                rgb_uint8 = tls.read_image_mode(path_to_rgb,
                                                'RGB')
                crop_uint8 = tls.crop_option_2d(tls.rgb_to_ycbcr(rgb_uint8)[:, :, 0],
                                                width_crop,
                                                is_random)
            except (TypeError, ValueError) as err:
                print(err)
                print('"{}" is skipped.\n'.format(path_to_rgb))
                continue
            luminances_uint8[i, :, :, 0] = crop_uint8
            i += 1
            if i == nb_total:
                break
        
        # If the previous loop was not broken,
        # `luminances_uint8` is not full. In this
        # case, the program crashes as the ImageNet
        # training and validation sets should not
        # contain any "zero" luminance crop.
        if i != nb_total:
            raise RuntimeError('There are not enough ImageNet RGB images at "{}" to create the ImageNet training and validation sets.'.format(path_to_folder_rgbs))
        training_data = luminances_uint8[0:nb_training, :, :, :]
        validation_data = luminances_uint8[nb_training:nb_total, :, :, :]
        numpy.save(path_to_training,
                   training_data)
        numpy.save(path_to_validation,
                   validation_data)


