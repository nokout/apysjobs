import json

def create_acronym_pair(name):
  words = name.split()
  acronym = ""
  for word in words:
      if word[0].isupper():
          acronym = acronym + word[0]
  return {'name': name, 'acronym': acronym}


if __name__ == "__main__":
    names_text = '''
Administrative Appeals Tribunal
Aboriginal Hostels Limited
AirServices Australia
Asbestos Safety and Eradication Agency
Attorney-General's Department
Austrade
Australian Accounting Standards Board
Australian Accounting Standards Board and Auditing and Assurance Standards Board
Australian Aged Care Quality Agency
Australian Antarctic Division
Australian Astronomical Observatory (AAO)
Australian Broadcasting Corporation
Australian Building and Construction Commission
Australian Bureau of Statistics
Australian Centre for International Agricultural Research (ACIAR)
Australian Charities and Not-for-profits Commission (ACNC)
Australian Children's Education and Care Quality Authority
Australian Commission for Law Enforcement Integrity
Australian Commission on Safety and Quality in Health Care (ACSQHC)
Australian Communications and Media Authority
Australian Competition and Consumer Commission
Australian Criminal Intelligence Commission (ACIC)
Australian Curriculum, Assessment and Reporting Authority (ACARA)
Australian Digital Health Agency
Australian Electoral Commission
Australian Federal Police
Australian Film Television and Radio School
Australian Financial Security Authority
Australian Fisheries Management Authority
Australian Government Solicitor
Australian Hearing
Australian Human Rights Commission
Australian Industrial Registry
Australian Industry Participation (AIP) Authority
Australian Institute of Aboriginal and Torres Strait Islander Studies
Australian Institute of Family Studies
Australian Institute of Health and Welfare
Australian Institute of Marine Science
Australian Law Reform Commission
Australian Maritime Safety Authority
Australian National Audit Office
Australian National Maritime Museum
Australian National Preventive Health Agency
Australian Nuclear Science and Technology Organisation
Australian Office of Financial Management
Australian Organ and Tissue Donation and Transplantation Authority
Australian Pesticides and Veterinary Medicines Authority
Australian Prudential Regulation Authority
Australian Public Service Commission
Australian Radiation Protection and Nuclear Safety Agency
Australian Reinsurance Pool Corporation
Australian Research Council
Australian Secret Intelligence Service
Australian Securities and Investments Commission
Australian Security Intelligence Organisation
Australian Skills Quality Authority (ASQA)
Australian Sports Anti-Doping Authority
Australian Sports Commission
Australian Taxation Office
Australian Transaction Reports and Analysis Centre (AUSTRAC)
Australian Transport Safety Bureau
Australian Valuation Office
Australian War Memorial
Bureau of Meteorology
Cancer Australia
Central Land Council
Civil Aviation Safety Authority Australia
Clean Energy Finance Corporation
Clean Energy Regulator
Climate Change Authority
COAG Reform Council
Comcare
Commonwealth Grants Commission
Commonwealth Ombudsman
Commonwealth Scientific and Industrial Research Organisation (CSIRO)
Commonwealth Superannuation Corporation
Defence Housing Australia
Defence Materiel Organisation (DMO)
Department of Agriculture and Water Resources
Department of Communications and the Arts
Department of Defence
Department of Education and Training
Department of Employment
Department of Finance
Department of Foreign Affairs and Trade
Department of Health
Department of Human Services
Department of Immigration and Border Protection
Department of Industry, Innovation and Science
Department of Infrastructure and Regional Development
Department of Parliamentary Services
Department of Resources, Energy and Tourism
Department of Social Services
Department of the Environment and Energy
Department of the House of Representatives
Department of the Prime Minister and Cabinet
Department of the Senate
Department of the Treasury
Department of Veterans' Affairs
Digital Transformation Agency (DTA)
Director of Public Prosecutions
Fair Work Commission
Fair Work Ombudsman
Family Court of Australia - FCoA
Federal Circuit Court of Australia - FCC
Federal Court of Australia
Food Standards Australia New Zealand
Future Fund Management Agency
Geoscience Australia
Great Barrier Reef Marine Park Authority
Health Workforce Australia
High Court of Australia
Independent Hospital Pricing Authority
Indian Ocean Territories Administration (IOTA)
Indigenous Business Australia
Indigenous Land Corporation
Infrastructure Australia
IP Australia
Murray-Darling Basin Authority
Museum of Australian Democracy - Old Parliament House
National Archives of Australia
National Blood Authority
National Capital Authority
National Competition Council
National Disability Insurance Agency
National Film and Sound Archive of Australia
National Gallery of Australia
National Health and Medical Research Council
National Health Funding Body
National Health Performance Authority
National Library of Australia
National Measurement Institute
National Mental Health Commission
National Museum of Australia
National Offshore Petroleum Safety and Environmental Management Authority (NOPSEMA)
National Portrait Gallery of Australia
National Science and Technology Centre (Questacon)
Office of Migration Agents Registration Authority
Office of National Assessments
Office of Parliamentary Counsel
Office of the Aged Care Commissioner
Office of the Australian Information Commissioner
Office of the Inspector-General of Intelligence and Security
Office of the Inspector-General of Taxation
Office of the Official Secretary to the Governor-General
Parliamentary Budget Office
Private Health Insurance Administration Council (PHIAC)
Productivity Commission
Professional Services Review
Royal Australian Mint
Royal Commission into Institutional Responses to Child Sexual Abuse
Rural Industries Research and Development Corporation
Rural Industries Research and Development Corporation  (RIRDC)
Safe Work Australia
Screen Australia
Special Broadcasting Service (SBS)
Tertiary Education Quality and Standards Agency
Therapeutic Goods Administration
Torres Strait Regional Authority
Tourism Australia
Tourism Research Australia
Various
Workplace Gender Equality Agency
'''
    names = names_text.split('\n')

    print("Name Count: {}".format(len(names)))

    # for name in names:
    #     print(create_acronym_pair(name))
    acronym_pairs = [create_acronym_pair(name) for name in names]


    with open('acronym_pairs.json', 'w') as f:
        json.dump(acronym_pairs, f)
    print('"Name","Acronym"')
    for name in acronym_pairs:
        print('"{}","{}"'.format(name["name"], name["acronym"]))
