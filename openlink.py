"""
Opens all Bangladesh Ministry / Government Office tender & notice links in the browser.
Source: Bangladesh_Govt_Tender_Directory.xlsx (Notice + Tender master list sheets,
with Petrobangla, ACC, CEGIS, IWM, and UCEP patched in from the updated Govt Offices
sheet, and OCAG added via its general website since no notice/tender page exists).

Usage:
    python openlink.py           # open all links
    python openlink.py 10        # open first 10 links
    python openlink.py 5 20      # open links 5 through 20
"""

import webbrowser
import time
import sys

LINKS = [

    # ===== Ministries & Divisions =====
    # President's Office
    "https://bangabhaban.gov.bd/pages/notices",
    "https://bangabhaban.gov.bd/pages/tenders",
    # Prime Minister's Office
    "https://pmo.gov.bd/pages/notices",
    "https://pmo.gov.bd/pages/tenders",
    # Cabinet Division
    "https://cabinet.gov.bd/pages/notices",
    "https://cabinet.gov.bd/pages/tenders",
    # Ministry of Chittagong Hill Tracts Affairs
    "https://mochta.gov.bd/pages/notices",
    "https://mochta.gov.bd/pages/tenders",
    # Ministry of Primary and Mass Education
    "https://mopme.gov.bd/pages/notices",
    "https://mopme.gov.bd/pages/tenders",
    # Ministry of Agriculture
    "https://moa.gov.bd/pages/notices",
    "https://moa.gov.bd/pages/tenders",
    # Ministry of Civil Aviation and Tourism
    "https://mocat.gov.bd/pages/notices",
    "https://mocat.gov.bd/pages/tenders",
    # Ministry of Commerce
    "https://mincom.gov.bd/pages/notices",
    "https://mincom.gov.bd/pages/tenders",
    # Ministry of Road Transport and Bridges
    "https://rthd.gov.bd/pages/notices",
    "https://rthd.gov.bd/pages/tenders",
    # Ministry of Cultural Affairs
    "https://moca.gov.bd/pages/notices",
    "https://moca.gov.bd/pages/tenders",
    # Ministry of Defence
    "https://mod.gov.bd/pages/notices",
    "https://mod.gov.bd/pages/tenders",
    # Ministry of Food
    "https://mofood.gov.bd/pages/notices",
    "https://mofood.gov.bd/pages/tenders",
    # Ministry of Education
    "https://shed.gov.bd/pages/notices",
    "https://shed.gov.bd/pages/tenders",
    # Ministry of Power, Energy and Mineral Resources
    "https://emrd.gov.bd/pages/notices",
    "https://emrd.gov.bd/pages/tenders",
    # Ministry of Environment, Forest and Climate Change
    "https://moef.gov.bd/pages/notices",
    "https://moef.gov.bd/pages/tenders",
    # Ministry of Public Administration
    "https://mopa.gov.bd/pages/notices",
    "https://mopa.gov.bd/pages/tenders",
    # Ministry of Fisheries and Livestock
    "https://mofl.gov.bd/pages/notices",
    "https://mofl.gov.bd/pages/tenders",
    # Ministry of Finance
    "https://mof.gov.bd/pages/notices",
    "https://mof.gov.bd/pages/tenders",
    # Ministry of Foreign Affairs
    "https://mofa.gov.bd/pages/notices",
    "https://mofa.gov.bd/pages/tenders",
    # Ministry of Health and Family Welfare
    "https://hsd.gov.bd/pages/notices",
    "https://hsd.gov.bd/pages/tenders",
    # Ministry of Home Affairs
    "https://moha.gov.bd/pages/notices",
    "https://moha.gov.bd/pages/tenders",
    # Ministry of Housing and Public Works
    "https://mohpw.gov.bd/pages/notices",
    "https://mohpw.gov.bd/pages/tenders",
    # Ministry of Industries
    "https://mohpw.gov.bd/pages/notices",
    "https://mohpw.gov.bd/pages/tenders",  # NOTE: Source notice/tender points to Housing (mohpw) domain — likely copy error; verify
    # Ministry of Information and Broadcasting
    "https://moi.gov.bd/pages/notices",
    "https://moi.gov.bd/pages/tenders",
    # Ministry of Textiles and Jute
    "https://motj.gov.bd/pages/notices",
    "https://motj.gov.bd/pages/tenders",
    # Ministry of Labour and Employment
    "https://mole.gov.bd/pages/notices",
    "https://mole.gov.bd/pages/tenders",
    # Ministry of Law, Justice and Parliamentary Affairs
    "https://lawjusticediv.gov.bd/pages/notices",
    "https://lawjusticediv.gov.bd/pages/tenders",
    # Ministry of Land
    "https://minland.gov.bd/pages/notices",
    "https://minland.gov.bd/pages/tenders",
    # Ministry of Local Government, Rural Development and Co-operatives
    "https://lgd.gov.bd/pages/notices",
    "https://lgd.gov.bd/pages/tenders",
    # Ministry of Planning
    "https://plancomm.gov.bd/pages/notices",
    "https://plancomm.gov.bd/pages/tenders",
    # Ministry of Posts, Telecommunications and Information Technology (no standard notice/tender page — portal link)
    "https://ictd.gov.bd/pages/go-ultimates?filters=%7B%22order%22%3A%20%2269414a4c35ce18e1c059a822%22%7D",
    # Ministry of Religious Affairs
    "https://mora.gov.bd/pages/notices",
    "https://mora.gov.bd/pages/tenders",
    # Ministry of Disaster Management and Relief
    "https://modmr.gov.bd/pages/notices",
    "https://modmr.gov.bd/pages/tenders",
    # Ministry of Shipping
    "https://mos.gov.bd/pages/notices",
    "https://mos.gov.bd/pages/tenders",
    # Ministry of Social Welfare (no standard notice/tender page — portal link)
    "https://msw.gov.bd/pages/static-pages/694032e635ce18e1c05640ce",
    # Ministry of Women and Children Affairs
    "https://mowca.gov.bd/pages/notices",
    "https://mowca.gov.bd/pages/tenders",
    # Ministry of Water Resources
    "https://mowr.gov.bd/pages/notices",
    "https://mowr.gov.bd/pages/tenders",
    # Ministry of Youth and Sports
    "https://moysports.gov.bd/pages/notices",
    "https://moysports.gov.bd/pages/tenders",
    # Ministry of Liberation War Affairs
    "https://molwa.gov.bd/pages/notices",
    "https://molwa.gov.bd/pages/tenders",
    # Ministry of Expatriates' Welfare and Overseas Employment
    "https://probashi.gov.bd/pages/notices",
    "https://probashi.gov.bd/pages/tenders",
    # Ministry of Railways
    "https://mor.gov.bd/pages/notices",
    "https://mor.gov.bd/pages/tenders",
    # Ministry of Science and Technology
    "https://most.gov.bd/pages/notices",
    "https://most.gov.bd/pages/tenders",

    # ===== Government Offices, Directorates & Agencies =====
    # Bangladesh Bureau of Statistics (BBS)
    "https://bbs.gov.bd/pages/notices",
    "https://bbs.gov.bd/pages/tenders",
    # Bangladesh Chemical Industries Corporation
    "https://bcic.gov.bd/pages/notices",
    "https://bcic.gov.bd/pages/tenders",
    # Bangladesh Civil Service Administration Academy
    "https://bcsadminacademy.gov.bd/pages/notices",
    "https://bcsadminacademy.gov.bd/pages/tenders",
    # Bangladesh Land Port Authority
    "https://blpa.gov.bd/pages/notices",
    "https://blpa.gov.bd/pages/tenders",
    # Bangladesh Meteorological Department (BMD)
    "https://bmd.gov.bd/pages/notices",
    "https://bmd.gov.bd/pages/tenders",
    # Bangladesh Parjatan Corporation
    "https://parjatan.gov.bd/pages/notices",
    "https://parjatan.gov.bd/pages/tenders",
    # Bangladesh Power Development Board
    "https://bpdb.gov.bd/pages/notices",
    "https://bpdb.gov.bd/pages/tenders",
    # Bangladesh Public Service Commission
    "https://bpsc.gov.bd/pages/notices",
    "https://bpsc.gov.bd/pages/tenders",
    # Bangladesh Space Research and Remote Sensing Organization (SPARRSO)
    "https://sparrso.gov.bd/pages/notices",
    "https://sparrso.gov.bd/pages/tenders",
    # Bangladesh Telecommunication Regulatory Commission
    "https://btrc.gov.bd/pages/notices",
    "https://btrc.gov.bd/pages/tenders",
    # Bangladesh Water Development Board
    "https://bwdb.gov.bd/pages/notices",
    "https://bwdb.gov.bd/pages/tenders",
    # Department of Archives and Libraries
    "https://nanl.gov.bd/pages/notices",
    "https://nanl.gov.bd/pages/tenders",
    # Department of Environment
    "https://doe.gov.bd/pages/notices",
    "https://doe.gov.bd/pages/tenders",
    # Department of Immigration and Passport
    "https://dip.gov.bd/pages/notices",
    "https://dip.gov.bd/pages/tenders",
    # Department of Shipping
    "https://dos.gov.bd/pages/notices",
    "https://dos.gov.bd/pages/tenders",
    # Department of Social Services
    "https://dss.gov.bd/pages/notices",
    "https://dss.gov.bd/pages/tenders",
    # Directorate General of Family Planning
    "https://dgfp.gov.bd/pages/notices",
    "https://dgfp.gov.bd/pages/tenders",
    # Directorate General of Food
    "https://dgfood.gov.bd/pages/notices",
    "https://dgfood.gov.bd/pages/tenders",
    # Directorate General of Health Services
    "https://dghs.gov.bd/pages/notices",
    "https://dghs.gov.bd/pages/tenders",
    # Directorate of Secondary and Higher Education (DSHE)
    "https://dshe.gov.bd/pages/notices",
    "https://dshe.gov.bd/pages/tenders",
    # Forest Department
    "https://bforest.gov.bd/pages/notices",
    "https://bforest.gov.bd/pages/tenders",
    # Gas Transmission Company Limited
    "https://gtcl.gov.bd/pages/notices",
    "https://gtcl.gov.bd/pages/tenders",
    # Land Record and Survey Department
    "https://dlrs.gov.bd/pages/notices",
    "https://dlrs.gov.bd/pages/tenders",
    # Land Reforms Board
    "https://lrb.gov.bd/pages/notices",
    "https://lrb.gov.bd/pages/tenders",
    # Local Government Engineering Department (LGED)
    "https://lged.gov.bd/pages/notices",
    "https://lged.gov.bd/pages/tenders",
    # NGO Affairs Bureau
    "https://ngoab.gov.bd/pages/notices",
    "https://ngoab.gov.bd/pages/tenders",
    # Palli Karma Sahayak Foundation (Non-gov.bd domain; tender URL confirmed manually, notice URL still unconfirmed)
    "https://pksf.org.bd/tender/",
    # Petrobangla (Bangladesh Oil, Gas & Mineral Corporation)
    "https://petrobangla.org.bd/pages/notices",
    "https://petrobangla.org.bd/pages/tenders",  # NOTE: Non-gov.bd domain; URL(s) confirmed via Govt Offices sheet update (master Notice/Tender sheet was stale)
    # University Grants Commission of Bangladesh
    "https://ugc.gov.bd/pages/notices",
    "https://ugc.gov.bd/pages/tenders",
    # Planning Ministry
    "https://plandiv.gov.bd/pages/notices",
    "https://plandiv.gov.bd/pages/tenders",
    # Election Commission
    "https://ecs.gov.bd/pages/notices",
    "https://ecs.gov.bd/pages/tenders",
    # Banagladesh Petrolium Corporation
    "https://bpc.gov.bd/pages/notices",
    "https://bpc.gov.bd/pages/tenders",
    # Dhaka Mass Transit Company Limited
    "https://dmtcl.gov.bd/pages/notices",
    "https://dmtcl.gov.bd/pages/tenders",
    # Roads and Highways Department
    "https://rhd.gov.bd/pages/notices",
    "https://rhd.gov.bd/pages/tenders",
    # Department of Disaster Management (DDM)
    "https://ddm.gov.bd/pages/notices",
    "https://ddm.gov.bd/pages/tenders",
    # Directorate General of Medical Education (DGME)
    "https://dgme.gov.bd/pages/notices",
    "https://dgme.gov.bd/pages/tenders",
    # Department of Youth Development
    "https://dyd.gov.bd/pages/notices",
    "https://dyd.gov.bd/pages/tenders",
    # Bangladesh Bureau of Educational Information and Statistics
    "https://banbeis.gov.bd/pages/notices",
    "https://banbeis.gov.bd/pages/tenders",
    # Directorate of Madrasa Education
    "https://dme.gov.bd/pages/notices",
    "https://dme.gov.bd/pages/tenders",
    # Bangladesh Hi-Tech Park Authority
    "https://bhtpa.gov.bd/pages/notices",
    "https://bhtpa.gov.bd/pages/tenders",
    # Department of ICT
    "https://doict.gov.bd/pages/notices",
    "https://doict.gov.bd/pages/tenders",
    # Jatiyo Mahila Sangstha
    "https://jms.gov.bd/pages/notices",
    "https://jms.gov.bd/pages/tenders",
    # Anti Corruption Commission (ACC)
    "https://acc.org.bd/pages/notices",
    "https://acc.org.bd/pages/tenders",  # NOTE: Non-gov.bd domain; URL(s) confirmed via Govt Offices sheet update (master Notice/Tender sheet was stale)
    # Comptroller and Auditor General (OCAG) (No dedicated notice/tender page found; linking to main website — verify manually for tender notices)
    "https://cag.org.bd",
    # Department of Agricultural Extension
    "https://dae.gov.bd/pages/notices",
    "https://dae.gov.bd/pages/tenders",
    # Bangladesh Food Safety Authority
    "https://bfsa.gov.bd/pages/notices",
    "https://bfsa.gov.bd/pages/tenders",
    # Bangladesh Agricultural Development Corporation
    "https://badc.gov.bd/pages/notices",
    "https://badc.gov.bd/pages/tenders",
    # Dhaka Transport Coordination Authority
    "https://dtca.gov.bd/pages/notices",
    "https://dtca.gov.bd/pages/tenders",
    # Department of Public Health Engineering
    "https://dphe.gov.bd/pages/notices",
    "https://dphe.gov.bd/pages/tenders",
    # Dhaka WASA
    "https://dwasa.gov.bd/pages/notices",
    "https://dwasa.gov.bd/pages/tenders",  # NOTE: Source Ministries sheet listed dwasa.org.bd; using official dwasa.gov.bd
    # Directorate of Primary Education
    "https://dpe.gov.bd/pages/notices",
    "https://dpe.gov.bd/pages/tenders",
    # UCEP
    "https://tender.ucepbd.org/",  # NOTE: Non-gov.bd domain; URL(s) confirmed via Govt Offices sheet update (master Notice/Tender sheet was stale)
    # Infrastructure Investment Facilitation Company
    "https://iifc.gov.bd/pages/notices",
    "https://iifc.gov.bd/pages/tenders",
    # Department of Explosives
    "https://explosives.gov.bd/pages/notices",
    "https://explosives.gov.bd/pages/tenders",
    # Water Resources Planning Organization
    "https://warpo.gov.bd/pages/notices",
    "https://warpo.gov.bd/pages/tenders",
    # Center for Environmental and Geographic Information Services
    "https://web.cegisbd.com/Events_News",  # NOTE: Non-gov.bd domain; URL(s) confirmed via Govt Offices sheet update (master Notice/Tender sheet was stale)
    # Institute of Water Modelling
    "https://iwmbd.org/Projects",  # NOTE: Non-gov.bd domain; URL(s) confirmed via Govt Offices sheet update (master Notice/Tender sheet was stale)
    # Civil Aviation Authority of Bangladesh
    "https://caab.gov.bd/pages/notices",
    "https://caab.gov.bd/pages/tenders",

    # ===== Excluded — no confirmed notice/tender URL, needs manual verification =====
    # SKIPPED: Armed Forces Division — No notice/tender link in source
]

# Parse optional range arguments
args = sys.argv[1:]
if len(args) == 0:
    subset = LINKS
elif len(args) == 1:
    subset = LINKS[:int(args[0])]
elif len(args) == 2:
    start, end = int(args[0]) - 1, int(args[1])
    subset = LINKS[start:end]
else:
    print("Usage: python openlink.py [count] OR [start end]")
    sys.exit(1)

print(f"Opening {len(subset)} links...\n")

for i, url in enumerate(subset, 1):
    print(f"[{i}/{len(subset)}] {url}")
    webbrowser.open_new_tab(url)
    time.sleep(0.3)  # small delay so browser doesn't get overwhelmed

print("\nDone.")
