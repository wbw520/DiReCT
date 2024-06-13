from typing import List, Optional
from utils.data_extraction import gen_reasoning_initial, gen_disease_diagnose, gen_reasoning_advanced
import fire
import sys
import ast
import os
import json
from utils.data_analysis import all_content, cal_a_json, prepare_note, prepare_note_slit, transmit_to_observation
from llama import Dialog, Llama
from utils.data_analysis import disease_category, combine_premise, extract_keys, check, delete_end, match, get_all_file_paths


disease_options, flowchart = disease_category()
os.environ["CUDA_VISIBLE_DEVICES"] = "4"


def main(
    ckpt_dir: str,
    tokenizer_path: str,
    temperature: float = 0,
    top_p: float = 0.9,
    max_seq_len: int = 8192,
    max_batch_size: int = 4,
    max_gen_len: Optional[int] = None,
):
    """
    Examples to run with the models finetuned for chat. Prompts correspond of chat
    turns between the user and assistant with the final one always being the user.

    An optional system prompt at the beginning to control how the model should respond
    is also supported.

    The context window of llama3 models is 8192 tokens, so `max_seq_len` needs to be <= 8192.

    `max_gen_len` is optional because finetuned models are able to stop generations naturally.
    """
    generator = Llama.build(
        ckpt_dir=ckpt_dir,
        tokenizer_path=tokenizer_path,
        max_seq_len=max_seq_len,
        max_batch_size=max_batch_size,
    )
    # file_name = "17763117-DS-13.json"
    # root_file = "Finished/Pneumonia/Viral Pneumonia/" + file_name
    # root_pred = "predict_llama3_8b/Pneumonia/Viral Pneumonia/" + file_name
    # cal_one_file(root_file, root_pred, generator, max_gen_len, temperature, top_p)

    pred_name = "predict_llama3_8b_premise"
    all_files_gt = get_all_file_paths("Finished")
    all_files_pred = get_all_file_paths(pred_name)

    for i in range(len(all_files_gt)):
        print(f"{i}/{len(all_files_gt)}")
        root_file = all_files_gt[i]
        # skip processed file
        root_pred = root_file.replace("Finished", pred_name)
        if root_pred in all_files_pred:
            continue

        try:
            cal_one_file(root_file, root_pred, generator, max_gen_len, temperature, top_p)
        except Exception as e:
            print(root_file)
            continue


def cal_one_file(root_file, root_pred, generator, max_gen_len, temperature, top_p):
    # Whether use premise for generation.
    use_p = True
    root_gt = root_file
    record_node, input_content, chain_gt = cal_a_json(root_gt)
    diagnosis_chain = []

    # first inference for possible disease category
    notes = prepare_note(input_content)
    input_ = gen_disease_diagnose(notes, disease_options)
    disease_cat = one_contact(generator, max_gen_len, temperature, top_p, input_)

    # agree some mistakes
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
    # if use_p:
    #     p_initial = combine_premise(knowledge, disease_list, initial=True)
    # else:
    #     p_initial = None

    # extract all observations for the suspected disease
    all_r = list(all_content.keys())
    record_suspect = {}
    for r in all_r:
        notet_r = prepare_note_slit(input_content, r)
        input_r = gen_reasoning_initial(notet_r, disease_cat, None)
        r_suspect = one_contact(generator, max_gen_len, temperature, top_p, input_r)
        r_suspect = delete_end(r_suspect)
        r_suspect = check(r_suspect)
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
        if use_p:
            p_advanced = combine_premise(knowledge, option_disease)
        else:
            p_advanced = None
        input_adv = gen_reasoning_advanced(all_observation, disease_cat, option_disease, p_advanced)
        r_adv = one_contact(generator, max_gen_len, temperature, top_p, input_adv)
        if r_adv == "None":
            break

        r_adv = ast.literal_eval(delete_end(r_adv))
        current_disease = r_adv[0][-1]
        diagnosis_chain.append(current_disease)
        for item in r_adv:
            try:
                record[item[0]][0] = item[1]  # cover new reason
                record[item[0]][2] = item[2]  # cover new disease
            except:
                continue
        flowchart_position = flowchart_position[current_disease]
        if len(flowchart_position) == 0:
            loop_index = False

    record.update({"chain": diagnosis_chain})
    # If direction not exist, make one
    directory = os.path.dirname(root_pred)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(root_pred, 'w') as json_file:
            json.dump(record, json_file)

def one_contact(generator, max_gen_len, temperature, top_p, in_):

    dialogs: List[Dialog] = [
        [{"role": "user", "content": in_}]
    ]

    results = generator.chat_completion(
        dialogs,
        max_gen_len=max_gen_len,
        temperature=temperature,
        top_p=top_p,
    )

    rr = results[0]['generation']['content']
    return rr


if __name__ == "__main__":
    sys.argv = ['example_chat_completion.py', '--ckpt_dir=Meta-Llama-3-8B-Instruct', '--tokenizer_path=Meta-Llama-3-8B-Instruct/tokenizer.model']
    fire.Fire(main)
