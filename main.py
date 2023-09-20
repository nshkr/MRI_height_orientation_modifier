import subprocess
import os
import glob

dir_path = "./dataset"
#How many times do you want each slice to be repeated for increasing the 3rd dimension of the MRI?
n_layers = 5

#which MR contrast files do you need to be modified?
wish_list = ["Flair", "T1" ] #Choose one or more contrasts: "Flair", "T1", "T2"

folder_list = []
for item in os.listdir(dir_path):
    # check if current item is a folder
    if not os.path.isfile(os.path.join(dir_path, item)):
        # add filename to list
        folder_list.append(item)



for folder in folder_list:
    folder_path = os.path.join(dir_path, folder)
    for file in os.listdir(folder_path):
        if file[-3:]=="nii":
            for contrast in wish_list:
                if contrast in file:
                    #Renaming files
                    file_path = os.path.join(folder_path, file)
                    new_name = file.replace('-','_')
                    new_name_path = os.path.join(folder_path, new_name)
                    
                    #Splitting slices
                    command_split = ["fslsplit", file_path, os.path.join(folder_path,str(new_name[0:-4])+"_slice_"), "-z"]
                    subprocess.run(command_split)

                    #Merging slices
                    slices_list = glob.glob(os.path.join(folder_path, str(new_name[0:-4])+'_slice_*.nii.gz'))
                    num_slices = len(slices_list)
                    command_merge_orient = f"""
                    for i in $(seq -f '%04g' 0  {num_slices-1}); do
                        echo $i
                        if [ $i -eq 0000 ]; then
                            for j in $(seq 1 {n_layers}); do
                            echo $j
                            fslmerge -z {new_name_path}.gz {os.path.join(folder_path, str(new_name[0:-4])+'_slice_${i}.nii.gz')};
                            done
                        else
                            for k in $(seq 1 {n_layers}); do
                            echo $k
                            fslmerge -z {new_name_path}.gz {new_name_path}.gz {os.path.join(folder_path, str(new_name[0:-4])+'_slice_${i}.nii.gz')};
                            done;
                        fi
                    done
                    
                    fslorient -deleteorient {new_name_path}.gz
            
                    fslorient -setqform 0 1 0 0 -1 0 0 0 0 0 1 0 0 0 0 1 {new_name_path}.gz
                    
                    fslorient -setqformcode 1 {new_name_path}.gz
                    
                    fslreorient2std {new_name_path}.gz {new_name_path}.gz
                    """
                    print(command_merge_orient)
                    subprocess.run(command_merge_orient, shell=True)
                    for item in slices_list:
                        os.remove(item)
