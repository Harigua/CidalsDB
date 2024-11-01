import traceback
import streamlit as st
from stmol import showmol
import py3Dmol
from rdkit import Chem
from rdkit.Chem import AllChem
import pubchempy
from rdkit import Chem
from rdkit.Chem import Descriptors
import numpy as np
from scipy.spatial import distance
import pubchempy as pcp
import pickle
import os
import pickle
import torch
from streamlit_extras.add_vertical_space import add_vertical_space
import deepchem as dc
from deepchem.data import NumpyDataset
import dill
from transformers import RobertaTokenizerFast
import os
import gdown
import requests
import torch.nn.functional as F

def gcn_predictor(smiles_string, model):  
    featurizer = dc.feat.MolGraphConvFeaturizer()
    features = featurizer.featurize([smiles_string])
    dataset = NumpyDataset(X=features, y=None, ids=None)
    proba = model.predict(dataset)
    predictions = np.argmax(proba, axis=1)
    if (predictions[0] == 1):
        return [predictions[0], proba[0][1]]
    else:
        return [predictions[0], proba[0][0]]

def chemebrta_predictor(smiles_string, model):
    tokenizer = RobertaTokenizerFast.from_pretrained('seyonec/SMILES_tokenized_PubChem_shard00_160k')
    
    inputs = tokenizer(smiles_string, truncation=True, padding=True, return_tensors='pt')
    
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    probabilities = F.softmax(logits, dim=1).squeeze()
    
    predicted_class = torch.argmax(logits, dim=1).item()
    predicted_probability = probabilities[predicted_class].item()
    return [predicted_class, predicted_probability]


def download_file_from_google_drive(url, destination):
    session = requests.Session()
    response = session.get(url, params={'confirm': 'true'}, stream=True)
    
    # Save the response content to the destination file
    with open(destination, 'wb') as f:
        for chunk in response.iter_content(32768):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)

def download_model_if_needed(model_name, file_id, folder_path):
    os.makedirs(folder_path, exist_ok=True)
    model_path = os.path.join(folder_path, model_name)
    if not os.path.exists(model_path):
        gdrive_url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(gdrive_url, model_path, quiet=False)
        print(f"Downloaded to {model_path}")


# Load the list of models after ensuring they are downloaded
def load_pickle_files_from_folder(folder_path, drive_path, name_condition=None):
    file_names = []
    
    for filename in os.listdir(folder_path):
        if name_condition is None or name_condition(filename):
            file_name_without_extension = os.path.splitext(filename)[0]
            file_names.append(file_name_without_extension)
            file_names.sort()

    return file_names

folder_path = "./Web_Interface/models"
drive_path = "/mount/src/cidaldb2/Web_Interface/models"
file_id_covid_chemberta = "11N3HU8Ll0Rou-hc-yGilnz2UyQIAAMWA"
file_id_leishmania_chemberta = "13uAsXTzJ3ZiubvWgnLjToOHsecHFUdet"
download_model_if_needed("Coronavirus_ChemBERTa.pkl", file_id_covid_chemberta, folder_path)
download_model_if_needed("Leishmania_ChemBERTa.pkl", file_id_leishmania_chemberta, folder_path)
loaded_models_filenames = load_pickle_files_from_folder(folder_path, drive_path, name_condition=lambda x: x.endswith('.pkl'))

def predict_with_model(smile, model_path):
    #st.text(type(model_path))
    #st.write(model_path)
    
    if model_path == "./Web_Interface/models/Coronavirus_GCN.pkl":
        #st.text("GCN")
        with open('./Web_Interface/models/Coronavirus_GCN.pkl', 'rb') as file:
            gcn_model = dill.load(file)
        # st.text(gcn_model.keys())
        [y, z] = gcn_predictor(smile, gcn_model)
        return [y, z]
    elif model_path == './Web_Interface/models/Coronavirus_ChemBERTa.pkl':
        with open(model_path, 'rb') as file:
            chemberta_model = dill.load(file)
        return chemebrta_predictor(smile, chemberta_model)
    elif model_path == './Web_Interface/models/Leishmania_ChemBERTa.pkl':
        with open(model_path, 'rb') as file:
            chemebrta_model = dill.load(file)
        return chemebrta_predictor(smile,chemebrta_model)
    else:
        molecule = Chem.MolFromSmiles(smile)
        x = np.array(AllChem.RDKFingerprint(molecule, fpSize=2048))
        # Load the pickled model
        with open(model_path, 'rb') as f:
            model = pickle.load(f)

        # Make the prediction using the loaded model
        y = model.predict([x])
        z = model.predict_proba([x])
        if (model_path == './Web_Interface/models/Coronavirus_GB.pkl'):
            y = y[0]
        if (model_path == './Web_Interface/models/Coronavirus_GCN.pkl'):
            z = z[0]
    if (y == 1):
        return [y, z[0][1]]
    else:
        return [y, z[0][0]]

def pubchem_id_to_smiles(pubchem_id):
    try:
        compound = pcp.get_compounds(pubchem_id)[0]
        smiles = compound.canonical_smiles
        return smiles
    except (IndexError, pcp.PubChemHTTPError) as e:
        print(f"Error retrieving SMILES for PubChem ID {pubchem_id}: {str(e)}")
        return None

def calculate_distance(smiles, fingerprint_array):
    molecule = Chem.MolFromSmiles(smiles)
    fingerprint = np.array(AllChem.RDKFingerprint(molecule, fpSize=1024))
    distances = distance.cdist(fingerprint.reshape(-1,1), fingerprint_array.reshape(-1,1), 'hamming')
    
    return distances.mean()


def passes_lipinski_rule(smiles):
    molecule = Chem.MolFromSmiles(smiles)
    molecular_weight = Descriptors.MolWt(molecule)
    logp = Descriptors.MolLogP(molecule)
    hbd = Descriptors.NumHDonors(molecule)
    hba = Descriptors.NumHAcceptors(molecule)
    
    if molecular_weight > 500 or logp > 5 or hbd > 5 or hba > 10:
        return False
    else:
        return True


def makeblock(smi):
    mol = Chem.MolFromSmiles(smi)
    mol = Chem.AddHs(mol)
    AllChem.EmbedMolecule(mol)
    mblock = Chem.MolToMolBlock(mol)
    return mblock

def render_mol(xyz):
    xyzview = py3Dmol.view()#(width=400,height=400)
    xyzview.addModel(xyz,'mol')
    xyzview.setStyle({'stick':{}})
    xyzview.setBackgroundColor('white')
    xyzview.zoomTo()
    showmol(xyzview,height=400,width=800)

def generate_name(smiles):
    compounds = pubchempy.get_compounds(smiles, namespace='smiles')
    match = compounds[0]
    return match.iupac_name


def predict():

    """
    ### Search By Smiles
    """

    st.markdown("<h1 style='font-size:2rem;'>Predict</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:1.2rem;'>Please select the predictive model corresponding to the pathogen you are interested in:</p>",
        unsafe_allow_html=True
    )


    data = np.load("./Web_Interface/data/data.npy")


    tabs_css = """
    <style>
    button[data-baseweb="tab"] > div[data-testid="stMarkdownContainer"] > p {
    font-size: 20px;
    }
    </style>
    """

    st.write(tabs_css, unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["Molecule SMILE",'PUBCHEM ID'])
    with tab1:
            smile = st.text_input(
                label='Molecule SMILE', 
                placeholder='COC1=C(C=C(C=C1)F)C(=O)C2CCCN(C2)CC3=CC4=C(C=C3)OCCO4',
                key='smile_input'
            )
            st.markdown(
                """
                <style>
                [data-testid="stMarkdownContainer"] p {
                    font-size: 20px !important;
                }
                </style>
                """,
                unsafe_allow_html=True
            )
            st.markdown(
                """
                <style>
                input[type="text"] {
                    font-size: 20px !important;
                }
                </style>
                """,
                unsafe_allow_html=True
            )
            option = st.selectbox(
                'Select Model',
                loaded_models_filenames, key = 42)
            if not smile:
                pass 
            else:
                try:
                    col1, col2 = st.columns([0.7, 0.3])
                    with col1:
                        name = generate_name(smile)
                        st.caption(name)
                        render = makeblock(smile)
                        render_mol(render)
                        progress_text = "Operation in progress. Please wait."
                    with col2:
                        with st.spinner(progress_text):
                            [res, proba] = predict_with_model(smile, f"./Web_Interface/models/{option}.pkl")
                            if res == 1:
                                add_vertical_space(4)
                                st.success(f'Active (Probability: {proba:.2f})', icon="✅")
                            else:
                                add_vertical_space(4)
                                st.error(f'Inactive (Probability: {proba:.2f})', icon="❌")
                except Exception as e:
                    # st.error(e)
                    st.error(traceback.format_exc())
                    st.error("Invalid Smile")  # You might want to adjust this message based on the context of the error

    with tab2:
        pub = st.text_input(label = 'PUBCHEM ID', placeholder = '161916')
        option = st.selectbox('Select Model',loaded_models_filenames, key = 43)
        if not pub:
            pass 
        else:
            try:
                cola, colb = st.columns([0.7, 0.3])
                with cola:
                    smile = pubchem_id_to_smiles(pub)
                    name = generate_name(smile)
                    st.caption(name)
                    render = makeblock(smile)
                    render_mol(render)
                    progress_text = "Operation in progress. Please wait."
                with colb:
                    with st.spinner(progress_text):
                        [res, proba] = predict_with_model(smile, f"./Web_Interface/models/{option}.pkl")
                        if res == 1:
                            st.success(f'Active (Probability: {proba:.2f})', icon="✅")
                        else:
                            st.error(f'Inactive (Probability: {proba:.2f})', icon="❌")
            except Exception as e:
                print(e)
                st.error('Invalid PubchemID')
