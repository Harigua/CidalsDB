import streamlit as st

def documentation():
    st.markdown(r"""
    # Documentation
    """)
    st.markdown(r"""
    ## Chemical Similarity Search

    Chemical similarity search uses distance measures to assess the similarity or dissimilarity between compounds. These measures help evaluate how different two compounds are from each other, based on their binary fingerprint representation. They are important in the context of matching, searching, and classifying chemical information.

    Different distance measures are used to compare the compounds, such as 
    """)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(r"""
            #### Tanimoto
    Tanimoto distance is a simple yet powerful metric. It is defined as the ratio of the intersection of the sets to the union of the sets.

    $$
    T = \frac{|A \cap B|}{|A|  +  |B| - |A \cap B|}
    $$

        """)
    with col2:
        st.markdown(r"""
            #### Sørensen-Dice Coefficient
    The Dice distance, also known as the Dice coefficient. It is closely related to the Tanimoto coefficient and quantifies the degree of overlap between two sets of molecular features.

    $$
    D = \frac{2 \cdot |A \cap B|}{|A|  +  |B|}
    $$

        """)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(r"""
            #### Cosine
            Cosine similarity is a common measure of similarity between two vectors. It is calculated by taking the cosine of the angle between the vectors.

            $$
            C = \frac{A \cdot B}{\|A\|  \cdot \|B\|}
            $$
                """)


    with col2:
        st.markdown(r""" 
            #### Tversky
        Tversky is a measure of dissimilarity between two molecular fingerprints.

        $$
        T_2 = \frac{|A \cap B|}{|A \cap B|  +  \alpha \cdot |A \backslash B|  + \beta \cdot |B \backslash A|}
        $$

        """)

    st.markdown(r"""        
    ## Activity Prediction

    We trained and optimized ML and DL algorithms on the content of the CidalsDB, namely RF, MLP and ChemBERTa models on the Leishmania dataset and the GB, GCN and ChemBERTa models on the Coronaviruses dataset. All technical details on the training, optimization, and validation of the models can be found in the publication Harigua-Souia et al.[³](#cidalsdb-an-open-resource-for-anti-pathogen-molecules)

    - **RF**: Random Forest is an algorithm widely used for classification tasks. It is an ensemble learning method that combines multiple decision trees to make predictions. Random Forest utilizes the concept of bagging and incorporates randomness in both feature selection and data sampling.

    - **MLP**: The Multilayer Perceptron (MLP) Classifier is a type of artificial neural network that can be used for supervised learning tasks such as classification. It consists of multiple layers of interconnected nodes, known as neurons.

    - **GB**: The Gradient Boosting Classifier is an algorithm that belongs to the ensemble learning family. It combines the strengths of weak prediction models, often referred to as weak learners, to build a strong predictive model.

    - **GCN**: Graph Convolution Network (GCN) is a type of graph neural network designed for learning representations that encode both the local structure and the node features of graph-structured data. This model employs a series of graph convolution layers to update node representations.

    - **ChemBERTa**: ChemBERTa is a pre-trained model tailored for molecular property prediction. This model, based on RoBERTa, leverages self-attention mechanisms to capture complex dependencies within molecular structures.
    """)

    st.markdown(
        """
        <div style="display: flex; flex-direction: column; align-items: center;">
            <img src="https://i.ibb.co/N2VXFxL/Workflow-Presentation-cidals.png" width="1100" alt="Pipeline of Training and Predictions">
            <p style="text-align: center; font-style: italic;">Pipeline of Training and Predictions</p>
        </div>
        """,
        unsafe_allow_html=True
    )
