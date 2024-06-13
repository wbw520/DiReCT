def gen_disease_diagnose(note, disease_options):
    setting_head = f"""Suppose you are one of the greatest AI scientists and medical expert. Let us think step by step. 
You will review a clinical 'Note' and your 'Response' is to diagnose the disease that the patient have for this admission. 
All possible disease options are in a list structure: {disease_options}. Note that you can only choose one disease from the disease options and directly output the origin name of that disease.
"""
    setting_end = f"""
Now, start to complete your task.
Don't output any information other than your 'Response'.
'Note':
{note}
Your 'Response':
"""
    input_ = setting_head + setting_end
    return input_


def gen_reasoning_initial(note, disease, premise=None):
    if premise is not None:
        pp = f"""Here are some premise for the diagnosis of this disease category. You can refer them for your task.
        Premise are: "{premise}"
        """
    else:
        pp = ""
    setting_head = f"""Suppose you are one of the greatest AI scientists and medical expert. Let us think step by step.
You will review a part of clinical "Note" from a patient. 
The disease for which the patient was admitted to hospital this time is {disease}.
Your task is to extract the original text as confidence "Observations" that lead to {disease}.
{pp}
Note that you also need to briefly provide the "Reason" for your extraction.
Note that both "Observations" and "Reason" should be string.
Note that your "Response" should be a list structure as following:
[["Observation", "Reason"], ......, ["Observation", "Reason"]]
Note that if you can't find any "Observation" your "Response" should be: [].
    """
    setting_end = f"""
Now, start to complete your task.
Note that you should not output any information other than your "Response".
"Note":
{note}
Note that you should not output any information other than your "Response".
Your "Response":
"""
    input_ = setting_head + setting_end
    return input_


def gen_reasoning_advanced(observation, disease, disease_option, premise=None):
    if premise is not None:
        pp = f"""Here are some golden standards to discriminate diseases. You can refer them for your task.
                Golden standards are:" {premise}"
           """
    else:
        pp = ""
    setting_head = f"""Suppose you are one of the greatest AI scientists and medical expert. Let us think step by step.
You will receive a list of "Observations" from a clinical "Note". These "Observations" are possible support to diagnose {disease}.
Based on these "Observations", you need to diagnose the "Disease" from the following options: {disease_option}.
{pp}
Note that you can only choose one "Disease" from the disease options and directly output the name in disease options.
Note that you also required to select the "Observations" that satisfy the golden standard to diagnose the "Disease" you choose.
Note that you also required to provide the "Reason" for your choice.
Note that your "Response" should be a list structure as following:
[["Observation", "Reason", "Disease"], ......, ["Observation", "Reason", "Disease"]]
Note that if you can't find any "Observation" to support a disease option, your "Response" should be: None
"""
    setting_end = f"""
Now, start to complete your task.
Note that you should not output any information other than your "Response".
"Observations":
{observation}
Note that you should not output any information other than your "Response".
Your "Response":
"""
    input_ = setting_head + setting_end
    return input_


def discriminate_similarity_observation(gt_observation, pred_observation):
    setting_head = f"""Suppose you are one of the greatest AI scientists and medical expert. Let us think step by step.
You will receive two "Observations" extracted from a patient's clinical note. 
Your task is to discriminate whether they textually description is similar? 
Note that "Response" should be one selection from "Yes" or "No".
"""
    setting_end = f"""
Now, start to complete your task.
Don't output any information other than your "Response".
"Observation 1":
{gt_observation}
"Observation 2":
{pred_observation}
Your "Response":
"""
    input_ = setting_head + setting_end
    return input_


def discriminate_similarity_reason(gt_reasoning, pred_reasoning):
    setting_head = f"""Suppose you are one of the greatest AI scientists and medical expert. Let us think step by step.
You will receive two "Reasoning" for the explanation of why an observation cause a disease. 
Your task is to discriminate whether they explain a similar medical diagnosis premise? 
Note that "Response" should be one selection from "Yes" or "No".

Here are some samples:
Sample 1:
    "Reasoning 1": Facial sagging is a classic symptom of stroke
    "Reasoning 2": Indicates possible facial nerve palsy, a common symptom of stroke
    "Response": Yes
Sample 2:
    "Reasoning 1": Family history of Diabetes is an important factor
    "Reasoning 2": Patient's mother had a history of Diabetes, indicating a possible genetic predisposition to stroke
    "Response": Yes
Sample 3:
    "Reasoning 1": headache is one of the common symptoms of HTN
    "Reasoning 2": Possible symptom of HTN
    "Response": No
Sample 4:
    "Reasoning 1": Acute bleeding is one of the typical symptoms of hemorrhagic stroke
    "Reasoning 2": The presence of high-density areas on Non-contrast CT Scan is a golden standard for Hemorrhagic Stroke
    "Response": No
Sample 5:
    "Reasoning 1": Loss of strength on one side of the body, especially when compared to the other side, is a common sign of stroke
    "Reasoning 2": Supports ischemic stroke diagnosis
    "Response": No
"""
    setting_end = f"""
Now, start to complete your task.
Don't output any information other than your "Response".
"Reasoning 1":
{gt_reasoning}
"Reasoning 2":
{pred_reasoning}
Your "Response":
"""
    input_ = setting_head + setting_end
    return input_


def gen_disease_closed(note, disease_options):
    setting_head = f"""Suppose you are one of the greatest AI scientists and medical expert. Let us think step by step. 
You will review a clinical 'Note' and your 'Response' is to diagnose the disease that the patient have for this admission. 
All possible disease options are in a list structure: {disease_options}. Note that you can only choose one disease from the disease options and directly output the origin name of that disease.
"""
    setting_end = f"""
Now, start to complete your task.
Don't output any information other than your 'Response'.
'Note':
{note}
Your 'Response':
"""
    input_ = setting_head + setting_end
    return input_


def gen_disease_open(note):
    setting_head = f"""Suppose you are one of the greatest AI scientists and medical expert. Let us think step by step. 
You will review a clinical 'Note' and your 'Response' is to diagnose the disease that the patient have for this admission. 
Note that you can only give one disease name and directly output the name of that "Disease".
"""
    setting_end = f"""
Now, start to complete your task.
Don't output any information other than your 'Response'.
'Note':
{note}
Your 'Response':
"""
    input_ = setting_head + setting_end
    return input_


def gen_disease_closed2(note, disease_options):
    setting_head = f"""Suppose you are one of the greatest AI scientists and medical expert. Let us think step by step. 
You will review a clinical 'Note' and your 'Response' is to diagnose the disease that the patient have for this admission. 
All possible disease options are in a list structure: {disease_options}. 
Note that you can only choose one disease from the disease options and directly output the origin name of that disease.
Note that you also need to extract original text as confidence "Observations" that lead to the "Disease" you selected.
Note that you should extract all necessary "Observation".
Note that you also need to briefly provide the "Reason" for your extraction.
Note that both "Observations" and "Reason" should be string.
Note that your "Response" should be a list structure as following:
[["Observation", "Reason", "Disease"], ......, ["Observation", "Reason", "Disease"]]
"""
    setting_end = f"""
Now, start to complete your task.
Don't output any information other than your 'Response'.
'Note':
{note}
Your 'Response':
"""
    input_ = setting_head + setting_end
    return input_


def gen_disease_open2(note):
    setting_head = f"""Suppose you are one of the greatest AI scientists and medical expert. Let us think step by step. 
You will review a clinical 'Note' and your 'Response' is to diagnose the disease that the patient have for this admission. 
Note that you can only give one disease name and directly output the name of that "Disease".
Note that you also need to extract the original text as confidence "Observations" that lead to the "Disease" you selected.
Note that you also need to extract original text as confidence "Observations" that lead to the "Disease" you selected.
Note that you should extract all necessary "Observation".
Note that you also need to briefly provide the "Reason" for your extraction.
Note that both "Observations" and "Reason" should be string.
Note that your "Response" should be a list structure as following:
[["Observation", "Reason", "Disease"], ......, ["Observation", "Reason", "Disease"]]
"""
    setting_end = f"""
Now, start to complete your task.
Don't output any information other than your 'Response'.
'Note':
{note}
Your 'Response':
"""
    input_ = setting_head + setting_end
    return input_