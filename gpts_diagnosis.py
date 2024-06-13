# Copyright (c) Meta Platforms, Inc. and affiliates.
# This software may be used and distributed in accordance with the terms of the Llama 3 Community License Agreement.

from typing import List
from utils.data_extraction import gen_reasoning_initial, gen_disease_diagnose, gen_reasoning_advanced
from utils.gpt_call import AskGPTAzure, AskChatGPT
import ast
import os
import json
from utils.data_analysis import all_content, cal_a_json, prepare_note, prepare_note_slit, transmit_to_observation
from utils.data_analysis import disease_category, combine_premise, extract_keys, check, delete_end, match, get_all_file_paths


disease_options, flowchart = disease_category()


def USE_GPT_API(root, use_p=False, api_key="Your key", azure_endpoint="Your endpoint", api_version="Your API version", model="Your Model"):
    # root: direction to the annotated data

    if use_p:
        suffix = "_premise"
    else:
        suffix = ""

    pred_name = f"predict_{model}" + suffix
    all_files_gt = get_all_file_paths(root)
    all_files_pred = get_all_file_paths(pred_name)

    for i in range(len(all_files_gt)):
        print(f"{i}/{len(all_files_gt)}")
        root_file = all_files_gt[i]
        # skip processed file
        root_pred = root_file.replace(root, pred_name)
        if root_pred in all_files_pred:
            continue

        try:
            cal_one_file(root_file, root_pred, use_p, api_key, azure_endpoint, api_version, model)
        except Exception as e:
            print(root_file)
            continue


def cal_one_file(root_file, root_pred, use_p, api_key, azure_endpoint, api_version, model):
    # Whether use premise for generation.
    root_gt = root_file
    record_node, input_content, chain_gt = cal_a_json(root_gt)
    diagnosis_chain = []

    # first inference for possible disease category
    notes = prepare_note(input_content)
    input_ = gen_disease_diagnose(notes, disease_options)
    disease_cat = one_contact(input_, api_key, azure_endpoint, api_version, model)

    # Agree some mistakes. We find a few generation inconsistency e.g., Schemic Stroke (leaf node disease) other than
    # Stroke (disease category), which is hallucination. If one name can match with a disease category,
    # we count this generation as correct and renamed it.
    if disease_cat not in disease_options:
        out_ = match(disease_cat, disease_options)
        if out_ is None:
            print("Hallucinations name:", disease_cat)
        else:
            disease_cat = out_

    diagnosis_chain.append(disease_cat)
    # Select the first disease name for a disease category
    disease_list = extract_keys(flowchart[disease_cat]["diagnostic"])
    current_disease = disease_list[0]
    # Select the whole subgraph for a disease category
    flowchart_position = flowchart[disease_cat]["diagnostic"]
    knowledge = flowchart[disease_cat]["knowledge"]
    diagnosis_chain.append(current_disease)

    # not use p for initial observation as low capability
    if use_p:
        p_initial = combine_premise(knowledge, disease_list, initial=True)
    else:
        p_initial = None

    # extract all observations for the suspected disease
    all_r = list(all_content.keys())
    record_suspect = {}
    for r in all_r:
        notet_r = prepare_note_slit(input_content, r)
        input_r = gen_reasoning_initial(notet_r, disease_cat, p_initial)
        r_suspect = one_contact(input_r, api_key, azure_endpoint, api_version, model)
        r_suspect = delete_end(r_suspect)
        try:
            record_suspect.update({r: ast.literal_eval(r_suspect)})
        except Exception as e:
            continue
    all_observation, record = transmit_to_observation(record_suspect, current_disease)

    # iteratively go through the diagnosis flowchart
    flowchart_position = flowchart_position[current_disease]
    loop_index = True
    while loop_index:
        option_disease = list(flowchart_position.keys())

        # whether use premise as input for iterative processing
        if use_p:
            p_advanced = combine_premise(knowledge, option_disease)
        else:
            p_advanced = None
        input_adv = gen_reasoning_advanced(all_observation, disease_cat, option_disease, p_advanced)
        r_adv = one_contact(input_adv, api_key, azure_endpoint, api_version, model)
        # if None, no children node can be accessed, thus quit
        if r_adv == "None":
            break

        r_adv = ast.literal_eval(delete_end(r_adv))
        current_disease = r_adv[-1][-1]
        diagnosis_chain.append(current_disease)
        for item in r_adv:
            try:
                record[item[0]][0] = item[1]  # cover new reason
                record[item[0]][2] = item[2]  # cover new disease
            except:
                continue
        flowchart_position = flowchart_position[current_disease]

        if len(flowchart_position) == 0:
            # finished when reach a leaf node
            loop_index = False

    record.update({"chain": diagnosis_chain})
    # If direction not exist, make one
    directory = os.path.dirname(root_pred)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(root_pred, 'w') as json_file:
            json.dump(record, json_file)


def one_contact(input_template, api_key, azure_endpoint, api_version, model):
    res = AskGPTAzure(input_template, api_key, azure_endpoint, api_version, model)
    # res = AskChatGPT(input_template, model="Your Model", api_key="Your key")
    out = res.choices[0].message.content
    return out
