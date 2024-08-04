# Data Loading and Analysis
## Data Structure
We store the annotated JSON files in folders named after the disease categories and PDD. Each JSON file record the annotated diagnostic procedure for a PDD. 
After unzipping the samples.rar file, the data is formulated as following:
```
-samples
    - Disease Category 1
          - PDD Category 1
                 - note_1.json
                 - note_2.json
                 - note_3.json
                 ...
          - PDD Category 2
          ...
    - Disease Category 2
    - Disease Category 3
    ...
```
A JSON file is with tree structure and you can use the [Annotation Tool](https://github.com/wbw520/DiReCT/tree/master/utils/data_annotation) to visualize it.
Here we demonstrate the code to load a JSON.
```
from utils.data_analysis import cal_a_json, deduction_assemble

root = "samples/Stroke/sample1.json"
record_node, input_content, chain = cal_a_json(root)
```
record_node: A dictionary for all nodes in our annotation with node index as key. Each node is also saved as a dictionary where <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"content" record the content of the node. <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"type" show the node annotation type, e.g., "Input" as observations, "Cause" as rationale, and "Intermedia" as diagnosis. <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"connection" gives the children node's key (if no child, it is the leaf diagnostic node). <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"upper" gives the parent node's key (if no parent, it is the observation node). <br>
input_content: A dictionary saves original clinical note from "input1"-"Chief Complaint" to "input6"-"Pertinent Results" <br>
chain: A list structure saves the diagnostic procedure in order (from suspected to one PDD).
```
GT = deduction_assemble(record_node)
```
deduction_assemble() organizes all nodes and return the all deductions as {o: [z,r,d]...}.  <br>
 <br>
o: extracted observation from raw text. <br>
d: name of the diagnosis. <br>
z: the rationale to explain why an observation can be related to a diagnosis d. <br>
r: the part (from one of input1-6) of the clinical note where o is extracted.