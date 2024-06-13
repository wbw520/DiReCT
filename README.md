# DiReCT: Diagnostic Reasoning for Clinical Notes via Large Language Models 
This repository is the official implementation of DiReCT. It contains the codes for running the baseline method as well as automatic evaluation.

## Data Set
We are now applying for the permission of releasing our data on PhysioNet. Several samples of annotated data are available in samples folder.

## Implementation of Baseline Experiment
We show the implementation for LLama3-8B and GPT Azure.
For using [LLama3](https://github.com/meta-llama/llama3), we use the official code on GitHub. Refer to their settings to prepare the environments .

#### Experiment with LLama3
Using the following command for training
```
python main_recon.py --num_classes 10 --num_cpt 20 --lr 0.001 --epoch 50 --lr_drop 30
```

#### Experiment with GPT Azure

