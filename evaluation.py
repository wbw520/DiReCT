from typing import List, Optional
from utils.data_analysis import deduction_assemble
from utils.data_extraction import discriminate_similarity_observation, discriminate_similarity_reason
import fire
import os
import sys
from utils.data_analysis import cal_a_json, get_all_file_paths
from llama import Dialog, Llama
import json

os.environ["CUDA_VISIBLE_DEVICES"] = "2"


def main(
    root: str,
    pred_name: str,
    ckpt_dir: str,
    tokenizer_path: str,
    temperature: float = 0,
    top_p: float = 1,
    max_seq_len: int = 8192,
    max_batch_size: int = 4,
    max_gen_len: Optional[int] = None,
):
    generator = Llama.build(
        ckpt_dir=ckpt_dir,
        tokenizer_path=tokenizer_path,
        max_seq_len=max_seq_len,
        max_batch_size=max_batch_size,
    )

    all_files_gt = get_all_file_paths(root)
    all_files_pred = get_all_file_paths(pred_name)
    all_files_pred_eval = get_all_file_paths(pred_name + "_eval")

    for i in range(len(all_files_gt)):
        print(f"{i}/{len(all_files_gt)}")
        root_file = all_files_gt[i]
        root_pred = root_file.replace(root, pred_name)
        root_eval = root_file.replace(root, pred_name + "_eval")
        # skip processed file
        if root_eval in all_files_pred_eval:
            continue
        # if a prediction is not successfully generated, we do not implement evaluation and treat it as 0 for all metric calculation
        if root_pred not in all_files_pred:
            continue
        try:
            deal_a_file(root_file, root_pred, root_eval, generator, max_gen_len, temperature, top_p)
        except Exception as e:
            print(root_eval)
            continue


def deal_a_file(root_file, root_pred, root_eval, generator, max_gen_len, temperature, top_p):
    root_gt = root_file
    record_node, input_content, chain_gt = cal_a_json(root_gt)
    GT = deduction_assemble(record_node)

    with open(root_pred, 'r') as file:
        predict = json.load(file)
    chain_pred = predict.pop("chain")
    GT_observation = list(GT.keys())
    predict_observation = list(predict.keys())
    ob_record = []
    excepted = []
    len_ob_gt = len(GT_observation)
    len_ob_pred = len(predict_observation)

    # Find similar observation pairs
    for i in range(len(GT_observation)):
        for j in range(len(predict_observation)):
            if j in excepted:
                continue
            input_ob = discriminate_similarity_observation(GT_observation[i], predict_observation[j])
            result_ob = one_contact(generator, max_gen_len, temperature, top_p, input_ob)
            if result_ob == "Yes":
                ob_record.append([i, j])
                excepted.append(j)
                break

    record = {}
    chain_gt.reverse()
    record.update({"chain_gt": chain_gt})
    record.update({"chain_pred": chain_pred})
    record.update({"len_ob_gt": len_ob_gt})
    record.update({"len_ob_pred": len_ob_pred})
    record.update({"ob_record_paired": {}})
    record.update({"GT_observation": GT_observation})
    record.update({"predict_observation": predict_observation})

    # find similar rationales
    for item in ob_record:
        re_gt = GT[GT_observation[item[0]]][0]
        disease_gt = GT[GT_observation[item[0]]][2]
        re_pred = predict[predict_observation[item[1]]][0]
        disease_pred = predict[predict_observation[item[1]]][2]
        input_reason = discriminate_similarity_reason(re_gt, re_pred)
        # print(re_gt)
        # print(re_pred)
        result_reason = one_contact(generator, max_gen_len, temperature, top_p, input_reason)
        # print(result_reason)
        # print("------------")
        record["ob_record_paired"].update({str(item): [disease_gt, disease_pred, re_gt, re_pred, result_reason]})

    # If direction not exist, make one
    directory = os.path.dirname(root_eval)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(root_eval, 'w') as json_file:
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
    fire.Fire(main)
