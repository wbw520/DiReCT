# Data Loading and Analysis
## Data Structure
Our data is saved in a JSON file (tree structure) and you can use the [Annotation Tool](https://github.com/wbw520/DiReCT/tree/master/utils/data_annotation) to visualize it.
Here we demonstrate the code to load a JSON.
```
from utils.data_analysis import cal_a_json, deduction_assemble

root = "samples/sample1.json"
record_node, input_content, chain = cal_a_json(root)
```
record_node: A dictionary for all nodes in our annotation. Each node is also saved as a dictionary where <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"content" record the content of the node. <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"type" show the node annotation type, e.g., "Input" as observations, "Cause" as rationale, and "Intermedia" as diagnosis. <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"connection" gives the children nodes (if no child, it is the leaf diagnostic node). <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"upper" gives the parent node (if no parent, it is the observation node). <br>
input_content: A dictionary saves original clinical note from "input1"-"Chief Complaint" to "input6"-"Pertinent Results" <br>
chain: A list structure saves the diagnostic procedure in order.
```
GT = deduction_assemble(record_node)
```
deduction_assemble() organizes all nodes and return the all deductions as {o: [z,r,d]...}.  <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;o: extracted observation from raw text. <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;d: name of the diagnosis. <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;r: the rationale to explain why an observation can be related to a diagnosis d. <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;r: the part (from one of input1-6) of the clinical note where o is extracted.