import json
import os


all_content = {"input1": "Chief Complaint", "input2": "History of Present Illness", "input3": "Past Medical History", "input4": "Family History", "input5": "Physical Exam", "input6": "Pertinent Results"}


def get_name(root, mode_folder=True):
    for root, dirs, file in os.walk(root):
        if mode_folder:
            return sorted(dirs)
        else:
            return sorted(file)


def cal_a_json(root):
    chain = []

    def traverse(key_, content, index_, upper):
        key_content, type_ = key_.split("$")
        if "Intermedia" in type_:
            chain.append(key_content)
        key_type = key_.split("$")[1].split("_")[0]
        current_key = list(content.keys())
        len_current_key = len(current_key)
        connection = []
        if len_current_key > 0:
            for i in range(len_current_key):
                connection.append(index[0])
                p_index = index.pop(0)
                traverse(current_key[i], content[current_key[i]], p_index, index_)
        record_node.update({index_: {"content": key_content, "type": key_type, "connection": connection, "upper": upper}})

    record_node = {}
    index = [i for i in range(1, 101, 1)]

    with open(root, 'r', encoding='utf-8') as f:
        data = json.load(f)

    input_content = {}
    for key, value in data.items():
        if "input" in key:
            input_content.update({key: value.replace("\ufeff", "")})
        else:
            traverse(key, value, 0, None)

    return record_node, input_content, chain


def deduction_assemble(record_node):
    GT = {}
    for key, value in record_node.items():
        if "Input" not in value['type']:
            continue
        observation = value['content']
        next_step = value["upper"]
        reasoning = record_node[next_step]['content']
        next_next_step = record_node[next_step]["upper"]
        disease = record_node[next_next_step]['content']
        GT.update({observation: [reasoning, value['type'], disease]})
    return GT


def disease_category():
    root = "/data/wangbowen/PycharmProject/llama3/Diagnosis_flowchart"
    files = get_name(root, mode_folder=False)
    disease_cat_options = []
    flowchart = {}
    for item in files:
        disease_cat = item.split(".")[0]
        disease_cat_options.append(disease_cat)
        with open(os.path.join(root, item), 'r') as file:
            data = json.load(file)
        flowchart.update({disease_cat: data})

    return disease_cat_options, flowchart


def disease_category2():
    disease_options, flowchart = disease_category()
    record = []
    for di in disease_options:
        flows = flowchart[di]["diagnostic"]
        leaf_node = get_non_dict_keys(flows, "")
        record.extend(leaf_node)
    return record


def prepare_note(input_content):
    out = """"""
    for key, value in input_content.items():
        out += all_content[key] + ":\n" + value
    return out


def prepare_note_slit(input_content, index):
    out = """"""
    out += all_content[index] + "\n" + input_content[index]
    return out


def transmit_to_observation(ob_suspected, disease):
    all_observation = []
    record = {}
    for key, value in ob_suspected.items():
        for item in value:
            if len(item) == 0:
                continue
            try:
                record.update({item[0]: [item[1], key, disease]})
                all_observation.append(item[0])
            except Exception as e:
                continue

    return all_observation, record


def combine_premise(knowledge, choice, initial=False):
    premise = """"""
    if initial:
        for i in range(len(choice)):
            if i == 0:
                elements = knowledge[choice[i]]
                for key, value in elements.items():
                    premise += f"{key}:{value}\n"
            else:
                premise += f"Golden standard for {choice[i]}:{knowledge[choice[i]]}\n"
    else:
        for i in range(len(choice)):
            premise += f"Golden standard for {choice[i]}:{knowledge[choice[i]]}\n"
    return premise


def extract_keys(d, parent_key=''):
    keys = []
    keys_leaf = []
    for k, v in d.items():
        full_key = f"{k}" if parent_key else k
        keys.append(full_key)
        if isinstance(v, dict):
            keys.extend(extract_keys(v, full_key))

    return keys


def get_non_dict_keys(data, parent_key=''):
    keys = []
    for key, value in data.items():
        full_key = f"{key}" if parent_key else key
        if isinstance(value, dict):
            keys.extend(get_non_dict_keys(value, full_key))
        else:
            keys.append(full_key)
    return keys


def check(text):
    if text[-2] != "]" and text[-2] != "," and text[-2] != "[":
        print("----------")
        print(text[-2])
        print("-----------")
        text += "]"
    return text


def delete_end(r_adv):
    ooo = r_adv.split("]")
    if len(ooo[-1]) > 0:
        out = r_adv.replace(ooo[-1], "")
    else:
        out = r_adv
    return out


def match(pred, disease_list):
    preds = pred.split(" ")
    record = {}
    for disease in disease_list:
        dd = disease.split(" ")
        record.update({disease: 0})
        temp = []
        for i in range(len(preds)):
            for j in range(len(dd)):
                if j in temp:
                    continue
                if preds[i] == dd[j]:
                    record[disease] += 1
                    temp.append(j)
                    break
    sorted_dict = dict(sorted(record.items(), key=lambda item: item[1], reverse=True))
    ll = list(sorted_dict.keys())[0]
    if sorted_dict[ll] == 0:
        return None
    else:
        return ll


def get_all_file_paths(directory):
    file_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_paths.append(os.path.join(root, file))
    return file_paths


def capitalize_first_letter(text):
    words = text.split()
    capitalized_words = [word[0].upper() + word[1:] if word else '' for word in words]
    return ' '.join(capitalized_words)

# disease_options, flowchart = disease_category()
# match("Acute Gastrointestinal Bleeding", disease_options)

# disease_options, flowchart = disease_category()
# disease_cat = "Stroke"
# disease_list = extract_keys(flowchart[disease_cat]["diagnostic"])
# print(disease_list)
# current_disease = disease_list[0]
# flowchart_position = flowchart[disease_cat]["diagnostic"]
# knowledge = flowchart[disease_cat]["knowledge"]
# p_initial = combine_premise(knowledge, disease_list, initial=True)
# print(p_initial)