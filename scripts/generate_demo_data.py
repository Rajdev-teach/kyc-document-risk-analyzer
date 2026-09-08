"""Generate synthetic PDFs and gold inventory; never contains real customer data."""
import csv
from pathlib import Path
from reportlab.pdfgen.canvas import Canvas

DOCS = [
("doc_001","passport","low","Name: John Carter\nPassport ID: PUS1234567\nCountry: United States\nExpiry: 2029-04-10\nIdentity verified."),
("doc_002","bank_statement","low","Name: Maya Patel\nACCT-50001234\nRiver Bank\nBalance: $12,450.00\nAddress verified in Missouri."),
("doc_003","business_record","low","Name: Noah Wilson\nClear Water LLC\nRegistered: 2021-06-09\nDelaware\nOwnership verified."),
("doc_004","passport","medium","Name: Emma Davis\nPassport ID: PUS2222222\nCountry: United States\nExpiry: 2027-01-01\nAddress unverified."),
("doc_005","bank_statement","medium","Name: Liam Brown\nACCT-50007777\nMetro Bank\nCash deposits: $24,000\nSource details missing."),
("doc_006","business_record","medium","Name: Olivia Martin\nNorth Star Inc\nRegistered: 2020-02-02\nOwnership mismatch requires review."),
("doc_007","passport","high","Name: Ethan Clark\nPassport ID: PUS9999999\nCountry: United States\nExpiry: 2019-03-01\nDocument expired and sanction match flagged."),
("doc_008","bank_statement","high","Name: Ava Lewis\nACCT-50009999\nGlobal Bank\nOffshore cash transfers: $850,000\nAdverse media and sanction alert."),
("doc_009","business_record","high","Name: Lucas Hall\nRapid Holdings Ltd\nOwnership unverified\nAddress mismatch\nSanction screening match."),
("doc_010","passport","low","Name: Sophia Young\nPassport ID: PUS3131313\nCountry: India\nExpiry: 2030-11-25\nIdentity verified."),
("doc_011","bank_statement","medium","Name: Mason King\nACCT-50001111\nCity Bank\nCash activity: $18,500\nEmployer details missing."),
("doc_012","business_record","high","Name: Isabella Wright\nShadow Trade Corporation\nOffshore ownership unverified\nAdverse media alert."),
("doc_013","passport","low","Name: James Scott\nPassport ID: PUS4141414\nCountry: United States\nExpiry: 2028-08-18\nIdentity verified."),
("doc_014","bank_statement","medium","Name: Mia Green\nACCT-50002222\nUnion Bank\nBalance: $42,000\nAddress mismatch under review."),
("doc_015","business_record","high","Name: Benjamin Adams\nOpaque Ventures LLC\nRegistration missing\nSanction match and offshore transfers."),
]

def main():
    raw=Path("data/raw"); labels=Path("data/labels"); raw.mkdir(parents=True,exist_ok=True); labels.mkdir(parents=True,exist_ok=True)
    rows=[]
    for i,(doc_id,kind,risk,text) in enumerate(DOCS):
        path=raw/f"{doc_id}_{kind}.pdf"; c=Canvas(str(path)); y=760
        c.setFont("Helvetica-Bold",14); c.drawString(72,y,"SYNTHETIC KYC DEMONSTRATION"); y-=35; c.setFont("Helvetica",11)
        for line in text.splitlines(): c.drawString(72,y,line); y-=22
        c.drawString(72,60,"Page 1 of 1"); c.save()
        expected="PERSON,DATE,GPE,ID_NUMBER" if kind=="passport" else ("PERSON,ORG,MONEY,ID_NUMBER" if kind=="bank_statement" else "PERSON,ORG,DATE,GPE")
        split="train" if i<9 else ("validation" if i<12 else "test")
        rows.append([doc_id,str(path),kind,expected,risk,split,"Synthetic; selectable text; no duplicates"])
    with (labels/"inventory.csv").open("w",newline="") as f:
        w=csv.writer(f); w.writerow(["doc_id","file_path","doc_type","expected_entities","risk_label","split","notes"]); w.writerows(rows)
    print(f"Generated {len(rows)} synthetic PDFs and inventory")
if __name__=="__main__": main()

