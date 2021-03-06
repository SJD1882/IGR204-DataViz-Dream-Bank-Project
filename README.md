## IGR204 Data Visualization Project - Decrypting Dreambank

![](assets/dreambank_viewer1.PNG)

### Motivation

Our goal is to help  identify groups of people having similar dreams, and allows them to dig deeper into dreams by selecting specific dreams or groups of dreams to get information. This would allow researchers to draw parallels and formulate hypotheses regarding the process of dreaming with several examples from different people. They may also be able to detect patterns in dreams and draw links between types of people and themes in dreams.

### Instructions

**Required dependencies**:

In addition to the standard Python packages, the following dependencies are required:

```console
pip install dash
pip install dash-bootstrap-components
```

**To run our application:**

Once the repository is cloned, run the following commands in the Console Prompt:

```console
cd IGR204-DataViz-Dream-Bank-Project
python app.py
```

A localhost will appear where the application can be displayed.

### Data Preprocessing 

We used baseline NLP approaches relying on word count and TF-IDF to preprocess Dream Bank. Data preprocessing steps are detailed in the following Jupyter Notebook:

[Dream Bank Data Preprocessing](https://github.com/SJD1882/IGR204-DataViz-Dream-Bank-Project/blob/master/notebooks/Dream_Bank_Data_Preprocessing.ipynb)

Dimensionality Reduction was done with the UMAP algorithm:

[Dream Bank UMAP Dimensionality Reduction](https://github.com/SJD1882/IGR204-DataViz-Dream-Bank-Project/blob/master/notebooks/Dream_Bank_Dimensionality_Reduction.ipynb)
