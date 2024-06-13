# DiReCT: Diagnostic Reasoning for Clinical Notes via Large Language Models 
This repository is the official implementation of DiReCT. It contains the codes for running the baseline method as well as automatic evaluation.

## Data Set
We are now applying for the permission of releasing our data on PhysioNet. Several samples of annotated data are available in samples folder.

[Annotation and Tools](https://github.com/wbw520/DiReCT/tree/master/utils/data_annotation)
[Data Loading and Analysis](https://github.com/wbw520/DiReCT/tree/master/utils/data_loading_analysisi)

## Implementation of Baseline Experiment
We show the implementation for LLama3-8B and GPT Azure.
For [LLama3](https://github.com/meta-llama/llama3), we use the official code on GitHub. Refer to their settings to prepare the environments and download the pre-trained models. 
The final output is save in a JSON file in a dictionary structure as: {o: [z, r, d] ...}. r mean the part of the clinical note where o is extracted. 

#### Experiment with LLama3
Using the following command for the calculation of annotated samples. Set --use_p as True for utilizing the premise in knowledge graph.
```
torchrun --nproc_per_node 1 llama3_diagnosis.py --ckpt_dir Meta-Llama-3-8B-Instruct/ --tokenizer_path Meta-Llama-3-8B-Instruct/tokenizer.model  --root samples --use_p False
```
#### Experiment with GPT Azure
Fill in you account for Azure GPT API
```
from gpts_diagnosis import USE_GPT_API

USE_GPT_API(root="samples", use_p=False, api_key="Your key", azure_endpoint="Your endpoint", api_version="Your API version", model="Your Model")
```

## Automatic Evaluation
We use the LLama3-8B for this evaluation. Our prompts refer to utils/dataextraction.py <br>
With functions: discriminate_similarity_observation() and  def discriminate_similarity_reason()
#### Evaluation for Completeness and Faithfulness
#### Results Statistics
