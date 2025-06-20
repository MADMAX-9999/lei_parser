import streamlit as st
import pandas as pd
import xml.etree.ElementTree as ET
from io import StringIO, BytesIO

st.title("LEI XML Parser - eksport danych do CSV")

uploaded_file = st.file_uploader("Wgraj plik XML z rekordami LEI", type="xml")

if uploaded_file:
    tree = ET.parse(uploaded_file)
    root = tree.getroot()

    namespaces = {'lei': 'http://www.gleif.org/data/schema/leidata/2016'}
    records = root.findall('.//lei:LEIRecord', namespaces)

    data = []

    for rec in records:
        entry = {
            'LEI': rec.findtext('lei:LEI', default='', namespaces=namespaces),
            'LegalName': rec.findtext('lei:Entity/lei:LegalName', default='', namespaces=namespaces),
            'TransliteratedName': rec.findtext('lei:Entity/lei:TransliteratedOtherEntityNames/lei:TransliteratedOtherEntityName', default='', namespaces=namespaces),
            'LegalAddress_Line': rec.findtext('lei:Entity/lei:LegalAddress/lei:FirstAddressLine', default='', namespaces=namespaces),
            'LegalAddress_City': rec.findtext('lei:Entity/lei:LegalAddress/lei:City', default='', namespaces=namespaces),
            'LegalAddress_Region': rec.findtext('lei:Entity/lei:LegalAddress/lei:Region', default='', namespaces=namespaces),
            'LegalAddress_PostalCode': rec.findtext('lei:Entity/lei:LegalAddress/lei:PostalCode', default='', namespaces=namespaces),
            'LegalAddress_Country': rec.findtext('lei:Entity/lei:LegalAddress/lei:Country', default='', namespaces=namespaces),
            'RegistrationAuthorityID': rec.findtext('lei:Entity/lei:RegistrationAuthority/lei:RegistrationAuthorityID', default='', namespaces=namespaces),
            'LegalJurisdiction': rec.findtext('lei:Entity/lei:LegalJurisdiction', default='', namespaces=namespaces),
            'LegalFormCode': rec.findtext('lei:Entity/lei:LegalForm/lei:EntityLegalFormCode', default='', namespaces=namespaces),
            'EntityStatus': rec.findtext('lei:Entity/lei:EntityStatus', default='', namespaces=namespaces),
            'InitialRegistrationDate': rec.findtext('lei:Registration/lei:InitialRegistrationDate', default='', namespaces=namespaces),
            'LastUpdateDate': rec.findtext('lei:Registration/lei:LastUpdateDate', default='', namespaces=namespaces),
            'RegistrationStatus': rec.findtext('lei:Registration/lei:RegistrationStatus', default='', namespaces=namespaces),
            'NextRenewalDate': rec.findtext('lei:Registration/lei:NextRenewalDate', default='', namespaces=namespaces),
            'ManagingLOU': rec.findtext('lei:Registration/lei:ManagingLOU', default='', namespaces=namespaces),
            'ValidationSources': rec.findtext('lei:Registration/lei:ValidationSources', default='', namespaces=namespaces),
        }
        data.append(entry)

    df = pd.DataFrame(data)

    st.success(f"Znaleziono {len(df)} rekordów.")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Pobierz CSV", data=csv, file_name="LEI_data.csv", mime='text/csv')
