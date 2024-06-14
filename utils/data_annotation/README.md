# Data Annotation
## Annotation for DiReCT
We demonstrate our data annotation here. Here is a sample for the annotation of Heart Failure (HF). Physicians are ask to find the observation "purple" from
the clinical note and provide the rationale why it causes the disease during diagnostic procedure.
![Annotation_sample](annotation_sample.png)

Our annotation tool is provided as "annotation tool.exe". We developed it by ourselves and current no license from Microsoft (alert safety information).
You can read the JSON file in "samples" folder to show the annotation results.

## Diagnostic Knowledge Graph
The knowledge graph for each disease category is saved as JSON file in "diagnostic_kg" folder. Key of diagnostic represent the diagnostic procedure and key of knowledge records the premise for each diagnosis d.

