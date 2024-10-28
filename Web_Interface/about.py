import streamlit as st
from lorem_text import lorem
import pandas as pd
from PIL import Image

text = lorem.paragraph()
meep = Image.open('./Web_Interface/media/Logo_MEEP.png')
bind = Image.open('./Web_Interface/media/logo_BIND.png')
ipt = Image.open('./Web_Interface/media/logo_IPT.png')
compound_distribution = Image.open('./Web_Interface/media/Distribution_of_compounds2.png')
all_logos = Image.open("./Web_Interface/media/all_logos.png")
def about():
    st.markdown(r"""
 # CidalsDB: An Open Resource for Anti-Pathogen Molecules

CidalsDB is an open resource on anti-pathogen molecules that provides a chemical similarity-based browsing function and an AI-based prediction tool for the 'cidal' effect of chemical compounds against pathogens. These include Leishmania parasites[^1^] and Coronaviruses (SARS-Cov, SARS-Cov-2, MERS)[^2^].

CidalsDB serves as an evolutive platform for democratized and no-code Computer-Aided Drug Discovery (CADD)[^3^]. We are committed to continuous improvement, actively incorporating additional pathogens, datasets, and AI predictive models.

[^1^]: Harigua-Souiai, E., Oualha, R., Souiai, O., Abdeljaoued-Tej, I. & Guizani, I. (2022). Applied machine learning toward drug discovery enhancement: Leishmaniases as a case study. Bioinforma. Biol. Insights 16, 11779322221090349.

[^2^]: Harigua-Souiai, E. et al. (2021). Deep learning algorithms achieved satisfactory predictions when trained on a novel collection of anticoronavirus molecules. Front. Genet. 12, 744170.

[^3^]: Harigua-Souiai, E., Masmoudi, O.,  Makni, S., Oualha, R., Abdelkrim, Y.Z., Hamdi, S., Souiai, O., Guizani, I. CidalsDB: An AI-empowered platform for anti-pathogen therapeutics research. Submitted.

    """)
    st.header("Datasets")
    st.write("""
    For now, we have datasets for two infectious diseases of interest within the **CidalsDB** database, that are accessible for the scientific community, namely *Leishmaniases* and *Coronaviruses*. For each disease, we performed an extensive search of the literature and retrieved data on molecules with validated anti-pathogen effects. We defined a data dictionary of published information related to the biological activity of the chemical compounds and used it to build the database. Then, we enriched the literature data with confirmatory screening datasets from PubChem. This led to consolidated sets of active and inactive molecules against Leishmania parasites and Coronaviruses. Additional infectious diseases will be considered to expand the database content.
    """)
    col1, col2 = st.columns(2)
    # Define color for the caption
    caption_color = "#000000"  # Adjust color as needed

    # Image 1 in col1
    with col1:
        st.markdown(
            f"""
            <div style="display: flex; flex-direction: column; align-items: center;">
                <img src="https://i.ibb.co/Wy35HXc/Distribution-of-compounds-leishmania-revised.png" width="370" alt="Molecules counts in the Leishmania dataset of CidalsDB">
                <p style="text-align: center; color: {caption_color};">Molecules counts in the Leishmania dataset of CidalsDB</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Image 2 in col2
    with col2:
        st.markdown(
            f"""
            <div style="display: flex; flex-direction: column; align-items: center;">
                <img src="https://i.ibb.co/BqMN5ps/Distribution-of-categories-leishamniasi-updated.png" width="450" alt="Numbers of data entries in each experimental category in the Leishmania dataset of CidalsDB">
                <p style="text-align: center; color: {caption_color};">Numbers of data entries in each experimental category in the Leishmania dataset of CidalsDB</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Image 3 in colh
    colh, colg = st.columns(2)
    with colh:
        st.markdown(
            f"""
            <div style="display: flex; flex-direction: column; align-items: center;">
                <img src="https://i.ibb.co/34T8g0S/Distribution-of-compounds-Covid-updated.png" width="370" alt="Molecules counts in the Coronavirus dataset of CidalsDB">
                <p style="text-align: center; color: {caption_color};">Molecules counts in the Coronavirus dataset of CidalsDB</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Image 4 in colg
    with colg:
        st.markdown(
            f"""
            <div style="display: flex; flex-direction: column; align-items: center;">
                <img src="https://i.ibb.co/s61tR37/Distribution-of-categories-covid-app-revised.png" width="450" alt="Numbers of data entries in each experimental category in the Coronavirus dataset of CidalsDB">
                <p style="text-align: center; color: {caption_color};">Numbers of data entries in each experimental category in the Coronavirus dataset of CidalsDB</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(r"""
    ## Acknowledgement
    """)

    st.markdown(
        f"""
        <div style="display: flex; flex-direction: column; align-items: center;">
            <img src="https://i.ibb.co/179hyrh/all-logos.png" width="1500" alt="All logos">
        </div>
        """,
        unsafe_allow_html=True
    )
    
