
# TRAILMAP Modification

This is a modification of the code described in  [Mapping Mesoscale Axonal Projections in the Mouse Brain Using A 3D Convolutional Network](https://www.biorxiv.org/content/10.1101/812644v1.full) Friedmann D, Pun A, et al and located at [Github TrailMap](https://github.com/AlbertPun/TRAILMAP). The original TrailMap licence is located [here](https://github.com/dfriedma/TRAILMAP/blob/master/LICENSE) and the licence for nnUNet and batchgenerators are [here](https://github.com/MIC-DKFZ/nnUNet/blob/master/LICENSE) and [here](https://github.com/MIC-DKFZ/batchgenerators/blob/master/LICENSE), respectively. Files have been modified.

## Getting Started - Installation

Please follow the detailed instruction on [Github TrailMap](https://github.com/AlbertPun/TRAILMAP) and also pip install batchgenerators

```
pip install batchgenerators==0.25
```

## Inference

Please follow the instructions at [Github TrailMap](https://github.com/AlbertPun/TRAILMAP) with these modifications. 
* Add model weights path to segment_brain_batch.py at the model_weight_list variable.
* Add the path to the data (with label and volume folders) for the image_path variable. This path can include an suffix variable. This script will use labels to calculate performance metrics for inference.
* The boolean argument indicates if you want to use guassian inference
* The string argument indicates training/validation/test data division suffix (leave '' if not using suffix)
* Use the combination number of the desired model_weight and image_path combination as an argument for segment_brain_batch.py.


```
python3 segment_brain_batch.py True "_test_1" {combination_number}

```

## Training

Please follow the instructions at [Github TrailMap](https://github.com/AlbertPun/TRAILMAP) with these modifications. 
For preparing data:
* When preparing the data for training, the location of the  data is set directly with the prepare_data.py file at data_original_path (input) and data_set_path (output) for each of the functions.
* The data_set_path should match the name provided as the training data under train.py (training_path and validation_path).
* The number of examples should be set directly within prepare_data with the nb_examples variable.
* The second string argument indicates training/validation/test data division suffix (leave '' if not using suffix). 
* The boolean argument indicates if the training should oversample 

```
python3 prepare_data.py "generate_validation_set" "_val_2_test_1" True
python3 prepare_data.py "generate_training_set"  "_val_2_test_1" True

```

For training:

* The first string indicates the model name suffix. 
* The combination_number argument indicates the index of the combination of arguments set by variable combo under train.py
* The location of the training data is set directly with the train.py file  (training_path and validation_path) 
* The positive booleans under the argument list under variable combo indicate 1) no oversampling, 2) no rotation, 3) no learn scheduler, 4) flip, 5) elastic deformation percentage, 6) rotate deformation percentage, 7) layer settting (needs to be set in model.py), 8) learning rate (needs to be set in model.py), and 9) training/validation/test data division suffix (leave '' if not using suffix)

```
python3 train.py "_july23_test" {combination_number}
```


## Authors
The work is adapted from  [Github TrailMap](https://github.com/AlbertPun/TRAILMAP), which was created by
* **Albert Pun**
* **Drew Friedmann**

The modified code was used in a paper by:
Marjolein Oostrom, Michael A. Muniak, Rogene Eichler West, Sarah Akers, Paritosh Pande, Moses Obiri, Wei Wang, Kasey Bowyer, Zhuhao Wu, Lisa Bramer, Tianyi Mao*, Bobbie Jo Webb-Robertson*


## Acknowledgments


MO, RMEW, SA, MO, LB, BJWR were supported by the Laboratory Directed Research and Development at Pacific Northwest National Laboratory (PNNL), a Department of Energy facility operated by Battelle under contract DE-AC05-76RLO01830. WW, KB, and ZW were supported in part by a NIH/BRAIN Initiative Grant RF1MH128969. MAM and TM were supported by two NIH/BRAIN Initiative Grants R01NS104944, RF1MH120119 and NIH R01NS081071. This research is affiliated with the Pacific northwest bioMedical Innovation Co-laboratory (PMedIC) collaboration between OHSU and PNNL.

The work is adapted from work sponsored by: 
* Research sponsored by Liqun Luo's Lab

## Disclaimer

This material was prepared as an account of work sponsored by an agency of the United States Government.  Neither the United States Government nor the United States Department of Energy, nor Battelle, nor any of their employees, nor any jurisdiction or organization that has cooperated in the development of these materials, makes any warranty, express or implied, or assumes any legal liability or responsibility for the accuracy, completeness, or usefulness or any information, apparatus, product, software, or process disclosed, or represents that its use would not infringe privately owned rights.
Reference herein to any specific commercial product, process, or service by trade name, trademark, manufacturer, or otherwise does not necessarily constitute or imply its endorsement, recommendation, or favoring by the United States Government or any agency thereof, or Battelle Memorial Institute. The views and opinions of authors expressed herein do not necessarily state or reflect those of the United States Government or any agency thereof.
PACIFIC NORTHWEST NATIONAL LABORATORY
operated by
BATTELLE
for the
UNITED STATES DEPARTMENT OF ENERGY
under Contract DE-AC05-76RL01830

## Copyright
Simplified BSD
____________________________________________
Copyright 2023 Battelle Memorial Institute

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.




