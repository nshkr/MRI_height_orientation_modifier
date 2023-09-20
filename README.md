# Brain MR image orientation and height modifier 
A Python code for correcting the orientation and increasing the height of brain MR images

## General Description
<p align="justify"> This code is adapted to modify the "<i>Brain MRI dataset of multiple sclerosis with consensus manual lesion segmentation and patient meta information</i>" (<a href="https://doi.org/10.1016/j.dib.2022.108139">Link</a> to dataset article). However, the code can be used for any other dataset. I wanted to use the above-mentioned dataset for training a CNN model but the NIFTI image files of this dataset need some modifications before preprocessing them: </p>

- <p align="justify"> The NIFTI files of this dataset do not include the orientation information (qform and sform) therefore the MRI viewers or MRI processing algorithms cannot know the orientation of the patient in the image. As shown in the figure below in FSLeyes, the orientations are unknown (question marks). The current repository corrects this problem by, first deleting any previous orientation information in the NIFTI header, then the correct orientation information (qform matrix) is saved (<b>IMPORTANT</b>: the orientation information in the code is intended for the above-mentioned dataset. If you are using this code for another dataset, you should carefully set the correct orientation as the qform matrix in the code. Always make sure to create a backup of your MRI data since manipulating the orientation information can make your data unuseful). Finally, the image is reoriented to match the orientation of the standard template images (MNI152) so that they appear the same in an MRI viewer. </p>
  
- <p align="justify"> The brain MRIs of this dataset are 2D, i.e. they have high resolution in the 1st and 2nd axes (principal plane) while the number of slices in the 3rd axis is much lower. Moreover, the voxel dimension is set to 1 mm in all directions. As a result, when you view the original images of the dataset, the brain (or the skull) is not shown like a normal one and it looks much shorter than a normal brain (as shown in the figure below). One of the problems that is caused by this condition is during the registration of the brain to a brain atlas. The current repository tries to modify this issue by increasing the image height (only in 3rd dimension). This is done simply by repeating each slice multiple times. Keep in mind that the thickness of each layer is not changed, instead the number of slices is multipled. You can set the desired number of times you want each layer to be repeated (<code>n_layers</code>). Of course, this affects only the height of the brain and the resulting resolution will not increase in the non-principal planes. </p>

![image](https://github.com/nshkr/MRI_height_orientation_modifier/assets/99551131/f841637e-bd61-4ace-a795-257802b9cc3e)
<p align="justify"> The original FLAIR image of patient-1 from the "<i>Brain MRI dataset of multiple sclerosis with consensus manual lesion segmentation and patient meta information</i>" dataset </p>

&nbsp;


![image](https://github.com/nshkr/MRI_height_orientation_modifier/assets/99551131/12c32c75-58c2-452f-9ad4-d156cc11d994)
<p align="justify"> The same image after increasing the slice thickness to 5 mm and correcting the orientations (A: Anterior, P: Posterior, R: Right, L: Left, S: Superior, I: Inferior) </p>

<p align="justify"> In the code, you can choose which MR contrasts to be modified (T1, T2, Flair). By choosing one or more contrasts, the image itself and the related lesion mask is modified accordingly. </p>

## Execution Requirements
<p align="justify"> The code mainly uses <a href="https://fsl.fmrib.ox.ac.uk/fsl/fslwiki">FSL</a>. In this repository, Python 3.10.12 and FSL 6.0.6.2 is used.  </p>


## Repository Structure
<p align="justify">The input dataset should be saved in <i>dataset</i> folder in the project repository. The "<i>Brain MRI dataset of multiple sclerosis with consensus manual lesion segmentation and patient meta information</i>" dataset is downloadable from this <a href="https://doi.org/10.17632/8bctsm8jz7.1
">link</a>.</p>

```
README.md
main.py  
dataset 
│
└───Patient-1
│   │   1-Flair.nii
│   │   1-LesionSeg-Flair.nii
│   │   1-LesionSeg-T1.nii
│   │   1-LesionSeg-T2.nii
│   │   1-T1.nii
│   │   1-T2.nii
│   
└───Patient-2
│   │   2-Flair.nii
│   │   2-LesionSeg-Flair.nii
│   │   2-LesionSeg-T1.nii
│   │   2-LesionSeg-T2.nii
│   │   2-T1.nii
│   │   2-T2.nii
└───...
output 
│
└───Patient_1
│   │   1_Flair.nii.gz
│   │   1_LesionSeg_Flair.nii.gz
│   │   1_LesionSeg_T1.nii.gz
│   │   1_LesionSeg_T2.nii.gz
│   │   1_T1.nii.gz
│   │   1_T2.nii.gz
│   
└───Patient_2
│   │   2_Flair.nii.gz
│   │   2_LesionSeg_Flair.nii.gz
│   │   2_LesionSeg_T1.nii.gz
│   │   2_LesionSeg_T2.nii.gz
│   │   2_T1.nii.gz
│   │   2_T2.nii.gz
└───...
```

## Citation
If you found this code useful and used it in your project, please cite this repository:

```
@misc{Shekarchizadeh2023,
  author = {Shekarchizadeh, Navid},
  title = {Brain MR image orientation and height modifier},
  year = {2023},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/nshkr/MRI_height_orientation_modifier,
  commit = {}
}
```
