from flask import Flask, render_template, request, session, redirect, url_for
import csv, os, uuid
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'epistemic_alignment_conditionA_2024'

# ── ALL 165 STOCK PAIRS — 11 SECTORS × 15 ROUNDS ─────────────────────────────

ALL_ROUNDS = {
    "Information Technology": [
        (1,  "TechCore Inc",     142.50, "+1.4%", "DataStream Ltd",    87.20,  "-0.8%"),
        (2,  "CloudVault Corp",  156.80, "+2.3%", "ByteMatrix Inc",    94.40,  "+0.7%"),
        (3,  "NexGen Systems",   203.60, "-0.5%", "PixelForge Ltd",   118.90,  "+1.9%"),
        (4,  "CyberLink Corp",   178.30, "+1.1%", "SoftWave Inc",     132.60,  "-1.2%"),
        (5,  "TechCore Inc",     145.20, "+0.9%", "CloudVault Corp",  159.40,  "+2.8%"),
        (6,  "ByteMatrix Inc",    97.30, "+1.6%", "NexGen Systems",   198.70,  "-0.3%"),
        (7,  "PixelForge Ltd",   122.50, "+2.1%", "CyberLink Corp",   181.90,  "+0.6%"),
        (8,  "DataStream Ltd",    89.60, "-1.4%", "SoftWave Inc",     135.80,  "+1.8%"),
        (9,  "TechCore Inc",     147.80, "+1.7%", "NexGen Systems",   201.30,  "+0.4%"),
        (10, "CloudVault Corp",  162.10, "-0.9%", "CyberLink Corp",   184.20,  "+2.2%"),
        (11, "ByteMatrix Inc",    99.80, "+0.8%", "PixelForge Ltd",   125.30,  "-0.6%"),
        (12, "SoftWave Inc",     138.40, "+1.3%", "TechCore Inc",     149.90,  "+1.9%"),
        (13, "NexGen Systems",   204.70, "+0.5%", "DataStream Ltd",    91.20,  "-1.1%"),
        (14, "CyberLink Corp",   186.50, "+1.4%", "ByteMatrix Inc",   102.10,  "+2.4%"),
        (15, "TechCore Inc",     152.30, "+2.6%", "PixelForge Ltd",   127.80,  "+0.9%"),
    ],
    "Health Care": [
        (1,  "MediGroup Corp",   198.30, "+0.9%", "HealthPlus Ltd",   134.60, "-0.4%"),
        (2,  "BioCore Inc",      245.80, "+2.1%", "CureVault Corp",    89.40, "+1.3%"),
        (3,  "PharmaBridge Ltd", 312.60, "-0.7%", "WellCare Inc",     167.90, "+2.4%"),
        (4,  "HealthPlus Ltd",   138.20, "+1.5%", "BioCore Inc",      249.30, "-0.6%"),
        (5,  "CureVault Corp",    92.40, "+3.1%", "PharmaBridge Ltd", 308.70, "+1.1%"),
        (6,  "MediGroup Corp",   201.50, "-0.3%", "WellCare Inc",     171.20, "+0.8%"),
        (7,  "BioCore Inc",      252.10, "+1.8%", "HealthPlus Ltd",   141.40, "+2.3%"),
        (8,  "PharmaBridge Ltd", 315.40, "+0.6%", "CureVault Corp",    95.80, "-1.5%"),
        (9,  "WellCare Inc",     174.60, "+2.7%", "MediGroup Corp",   204.20, "+0.4%"),
        (10, "HealthPlus Ltd",   144.30, "-0.8%", "PharmaBridge Ltd", 318.90, "+1.9%"),
        (11, "CureVault Corp",    98.60, "+1.2%", "BioCore Inc",      255.40, "-0.9%"),
        (12, "MediGroup Corp",   207.80, "+2.5%", "PharmaBridge Ltd", 322.10, "+0.7%"),
        (13, "WellCare Inc",     177.30, "-0.5%", "HealthPlus Ltd",   147.60, "+1.6%"),
        (14, "BioCore Inc",      258.70, "+1.4%", "MediGroup Corp",   211.40, "+3.2%"),
        (15, "PharmaBridge Ltd", 325.80, "+0.8%", "CureVault Corp",   101.90, "+2.1%"),
    ],
    "Energy": [
        (1,  "EnergyMax Ltd",    156.40, "+1.8%", "PetroCorp Inc",    203.20, "-0.6%"),
        (2,  "GreenFuel Corp",    89.30, "+3.2%", "PowerGrid Ltd",    134.80, "+1.1%"),
        (3,  "OilStream Inc",    267.50, "-1.3%", "EnergyMax Ltd",    158.90, "+2.7%"),
        (4,  "PetroCorp Inc",    206.80, "+0.9%", "GreenFuel Corp",    92.40, "-0.8%"),
        (5,  "PowerGrid Ltd",    137.60, "+2.4%", "OilStream Inc",    264.30, "+1.5%"),
        (6,  "EnergyMax Ltd",    161.20, "-0.7%", "GreenFuel Corp",    95.80, "+2.9%"),
        (7,  "PetroCorp Inc",    210.40, "+1.3%", "PowerGrid Ltd",    140.50, "+0.4%"),
        (8,  "OilStream Inc",    261.80, "+2.1%", "PetroCorp Inc",    213.70, "-1.1%"),
        (9,  "EnergyMax Ltd",    163.90, "+1.6%", "PowerGrid Ltd",    143.20, "+3.4%"),
        (10, "GreenFuel Corp",    99.20, "-0.4%", "OilStream Inc",    259.40, "+1.8%"),
        (11, "PowerGrid Ltd",    146.30, "+0.7%", "EnergyMax Ltd",    167.10, "+2.3%"),
        (12, "PetroCorp Inc",    217.60, "+2.8%", "GreenFuel Corp",   102.50, "-0.9%"),
        (13, "OilStream Inc",    257.20, "+1.4%", "PowerGrid Ltd",    149.40, "+1.2%"),
        (14, "EnergyMax Ltd",    170.80, "-0.6%", "PetroCorp Inc",    221.30, "+2.6%"),
        (15, "GreenFuel Corp",   105.90, "+3.7%", "EnergyMax Ltd",    174.20, "+1.1%"),
    ],
    "Financials": [
        (1,  "FinanceHub Corp",  312.40, "+1.2%", "BankCore Ltd",      187.60, "-0.5%"),
        (2,  "WealthBridge Inc", 156.80, "+2.8%", "CapitalStream Corp",234.50, "+1.4%"),
        (3,  "InvestGroup Ltd",  289.30, "-0.9%", "FinanceHub Corp",   315.70, "+2.1%"),
        (4,  "BankCore Ltd",     191.20, "+1.7%", "WealthBridge Inc",  159.40, "-0.7%"),
        (5,  "CapitalStream Corp",238.80,"+3.3%", "InvestGroup Ltd",   286.10, "+1.6%"),
        (6,  "FinanceHub Corp",  318.90, "-0.4%", "CapitalStream Corp",242.30, "+2.4%"),
        (7,  "WealthBridge Inc", 162.60, "+1.9%", "BankCore Ltd",      194.80, "+0.8%"),
        (8,  "InvestGroup Ltd",  283.40, "+2.6%", "CapitalStream Corp",246.10, "-1.2%"),
        (9,  "FinanceHub Corp",  322.50, "+1.4%", "WealthBridge Inc",  165.30, "+3.1%"),
        (10, "BankCore Ltd",     198.60, "-0.8%", "InvestGroup Ltd",   281.20, "+1.9%"),
        (11, "CapitalStream Corp",249.80,"+0.9%", "FinanceHub Corp",   326.40, "+2.7%"),
        (12, "WealthBridge Inc", 168.20, "+2.3%", "InvestGroup Ltd",   279.30, "-0.6%"),
        (13, "BankCore Ltd",     202.40, "+1.6%", "CapitalStream Corp",253.20, "+1.3%"),
        (14, "InvestGroup Ltd",  277.50, "+3.8%", "WealthBridge Inc",  171.60, "+0.7%"),
        (15, "FinanceHub Corp",  330.20, "-0.3%", "BankCore Ltd",      206.80, "+2.9%"),
    ],
    "Consumer Discretionary": [
        (1,  "RetailCore Inc",   234.50, "+1.6%", "ShopBridge Ltd",    156.80, "-0.9%"),
        (2,  "BrandStream Corp", 189.30, "+2.9%", "MarketVault Inc",    98.40, "+1.7%"),
        (3,  "ConsumerFirst Ltd",312.60, "-0.6%", "RetailCore Inc",    237.20, "+2.3%"),
        (4,  "ShopBridge Ltd",   160.40, "+1.1%", "BrandStream Corp",  192.80, "-1.4%"),
        (5,  "MarketVault Inc",  101.30, "+3.8%", "ConsumerFirst Ltd", 309.40, "+1.2%"),
        (6,  "RetailCore Inc",   239.80, "-0.7%", "MarketVault Inc",   104.60, "+2.6%"),
        (7,  "BrandStream Corp", 196.20, "+1.4%", "ShopBridge Ltd",    163.90, "+0.8%"),
        (8,  "ConsumerFirst Ltd",306.80, "+2.7%", "MarketVault Inc",   107.40, "-1.1%"),
        (9,  "RetailCore Inc",   242.50, "+1.9%", "BrandStream Corp",  199.60, "+3.4%"),
        (10, "ShopBridge Ltd",   167.30, "-0.5%", "ConsumerFirst Ltd", 304.20, "+1.8%"),
        (11, "MarketVault Inc",  110.80, "+0.7%", "RetailCore Inc",    245.30, "+2.2%"),
        (12, "BrandStream Corp", 203.10, "+2.4%", "ConsumerFirst Ltd", 301.80, "-0.8%"),
        (13, "ShopBridge Ltd",   170.60, "+1.3%", "MarketVault Inc",   114.20, "+1.6%"),
        (14, "ConsumerFirst Ltd",299.50, "+3.6%", "BrandStream Corp",  206.80, "+0.9%"),
        (15, "RetailCore Inc",   248.40, "-0.4%", "ShopBridge Ltd",    174.10, "+2.8%"),
    ],
    "Consumer Staples": [
        (1,  "StapleCore Corp",   178.60, "+0.8%", "FoodBridge Ltd",    234.30, "-0.3%"),
        (2,  "HouseholdFirst Inc",145.20, "+1.9%", "GroceryStream Corp",189.70, "+1.1%"),
        (3,  "StapleCore Corp",   180.40, "-0.4%", "HouseholdFirst Inc",147.80, "+2.6%"),
        (4,  "FoodBridge Ltd",    237.10, "+1.4%", "GroceryStream Corp",192.40, "-0.7%"),
        (5,  "HouseholdFirst Inc",150.30, "+3.1%", "StapleCore Corp",   182.80, "+1.2%"),
        (6,  "GroceryStream Corp",195.20, "-0.5%", "StapleCore Corp",   184.90, "+2.3%"),
        (7,  "FoodBridge Ltd",    239.80, "+0.9%", "HouseholdFirst Inc",153.10, "+0.6%"),
        (8,  "StapleCore Corp",   187.30, "+2.1%", "GroceryStream Corp",198.00, "-1.3%"),
        (9,  "HouseholdFirst Inc",156.40, "+1.7%", "FoodBridge Ltd",    242.60, "+3.2%"),
        (10, "GroceryStream Corp",201.20, "-0.6%", "StapleCore Corp",   190.10, "+1.8%"),
        (11, "StapleCore Corp",   192.60, "+0.7%", "HouseholdFirst Inc",159.20, "+2.4%"),
        (12, "FoodBridge Ltd",    245.80, "+2.8%", "GroceryStream Corp",204.40, "-0.9%"),
        (13, "HouseholdFirst Inc",162.30, "+1.3%", "StapleCore Corp",   195.20, "+1.6%"),
        (14, "GroceryStream Corp",208.10, "+3.7%", "FoodBridge Ltd",    248.90, "+0.8%"),
        (15, "StapleCore Corp",   198.10, "-0.5%", "HouseholdFirst Inc",165.80, "+2.9%"),
    ],
    "Industrials": [
        (1,  "AeroCore Inc",          287.40,"+1.3%","ManufactureBridge Ltd",198.60,"-0.7%"),
        (2,  "TransportFirst Corp",   156.80,"+2.6%","IndustryStream Inc",   234.20,"+1.5%"),
        (3,  "BuildCore Ltd",         312.50,"-0.8%","AeroCore Inc",         291.30,"+2.4%"),
        (4,  "ManufactureBridge Ltd", 201.40,"+1.1%","TransportFirst Corp",  159.60,"-1.2%"),
        (5,  "IndustryStream Inc",    237.80,"+3.4%","BuildCore Ltd",        309.20,"+1.0%"),
        (6,  "AeroCore Inc",          294.80,"-0.5%","IndustryStream Inc",   241.30,"+2.8%"),
        (7,  "TransportFirst Corp",   162.40,"+1.8%","ManufactureBridge Ltd",204.80,"+0.7%"),
        (8,  "BuildCore Ltd",         306.80,"+2.3%","IndustryStream Inc",   244.60,"-1.4%"),
        (9,  "AeroCore Inc",          298.20,"+1.6%","TransportFirst Corp",  165.30,"+3.3%"),
        (10, "ManufactureBridge Ltd", 208.20,"-0.9%","BuildCore Ltd",        304.50,"+1.9%"),
        (11, "IndustryStream Inc",    247.80,"+0.8%","AeroCore Inc",         302.10,"+2.6%"),
        (12, "TransportFirst Corp",   168.20,"+2.7%","ManufactureBridge Ltd",211.60,"-0.6%"),
        (13, "BuildCore Ltd",         302.30,"+1.4%","IndustryStream Inc",   251.20,"+1.3%"),
        (14, "AeroCore Inc",          305.90,"+3.9%","TransportFirst Corp",  171.50,"+0.8%"),
        (15, "ManufactureBridge Ltd", 215.00,"-0.4%","BuildCore Ltd",        300.10,"+3.1%"),
    ],
    "Materials": [
        (1,  "ChemCore Corp",      156.40,"+1.7%","MiningBridge Ltd",    234.80,"-0.5%"),
        (2,  "PackageFirst Inc",    89.30,"+2.4%","MaterialStream Corp", 178.60,"+1.3%"),
        (3,  "ChemCore Corp",      158.90,"-0.8%","PackageFirst Inc",     92.10,"+3.1%"),
        (4,  "MiningBridge Ltd",   237.60,"+1.2%","MaterialStream Corp", 181.40,"-0.9%"),
        (5,  "PackageFirst Inc",    94.80,"+2.9%","ChemCore Corp",       161.40,"+1.6%"),
        (6,  "MaterialStream Corp",184.20,"-0.4%","ChemCore Corp",       163.80,"+2.7%"),
        (7,  "MiningBridge Ltd",   240.40,"+0.9%","PackageFirst Inc",     97.60,"+0.6%"),
        (8,  "ChemCore Corp",      166.20,"+2.2%","MaterialStream Corp", 187.00,"-1.3%"),
        (9,  "PackageFirst Inc",   100.30,"+1.8%","MiningBridge Ltd",    243.20,"+3.6%"),
        (10, "MaterialStream Corp",189.80,"-0.7%","ChemCore Corp",       168.90,"+1.9%"),
        (11, "ChemCore Corp",      171.60,"+0.8%","PackageFirst Inc",    103.10,"+2.5%"),
        (12, "MiningBridge Ltd",   246.30,"+2.8%","MaterialStream Corp", 193.00,"-0.8%"),
        (13, "PackageFirst Inc",   105.80,"+1.4%","ChemCore Corp",       174.30,"+1.7%"),
        (14, "MaterialStream Corp",196.40,"+3.8%","MiningBridge Ltd",    249.80,"+0.9%"),
        (15, "ChemCore Corp",      177.20,"-0.6%","PackageFirst Inc",    108.60,"+3.2%"),
    ],
    "Real Estate": [
        (1,  "PropCore Inc",      234.60,"+1.4%","REITBridge Corp",    312.80,"-0.6%"),
        (2,  "PropertyFirst Ltd", 178.30,"+2.7%","EstateStream Inc",   156.40,"+1.2%"),
        (3,  "PropCore Inc",      237.40,"-0.7%","PropertyFirst Ltd",  181.60,"+3.4%"),
        (4,  "REITBridge Corp",   316.20,"+1.1%","EstateStream Inc",   159.30,"-1.1%"),
        (5,  "PropertyFirst Ltd", 184.90,"+3.6%","PropCore Inc",       240.20,"+1.5%"),
        (6,  "EstateStream Inc",  162.10,"-0.4%","PropCore Inc",       243.10,"+2.9%"),
        (7,  "REITBridge Corp",   319.80,"+0.8%","PropertyFirst Ltd",  188.30,"+0.7%"),
        (8,  "PropCore Inc",      246.20,"+2.4%","EstateStream Inc",   165.00,"-1.6%"),
        (9,  "PropertyFirst Ltd", 191.60,"+1.9%","REITBridge Corp",    323.40,"+3.7%"),
        (10, "EstateStream Inc",  167.80,"-0.9%","PropCore Inc",       249.30,"+1.8%"),
        (11, "PropCore Inc",      252.40,"+0.7%","PropertyFirst Ltd",  195.00,"+2.6%"),
        (12, "REITBridge Corp",   327.20,"+2.9%","EstateStream Inc",   170.60,"-0.7%"),
        (13, "PropertyFirst Ltd", 198.30,"+1.5%","PropCore Inc",       255.60,"+1.4%"),
        (14, "EstateStream Inc",  173.40,"+4.1%","REITBridge Corp",    331.40,"+0.8%"),
        (15, "PropCore Inc",      258.90,"-0.5%","PropertyFirst Ltd",  201.80,"+3.3%"),
    ],
    "Utilities": [
        (1,  "PowerCore Corp",    134.60,"+0.9%","UtilityBridge Ltd",  189.30,"-0.4%"),
        (2,  "ElectricFirst Inc",  98.40,"+1.8%","GasStream Corp",     156.80,"+1.1%"),
        (3,  "PowerCore Corp",    136.80,"-0.5%","ElectricFirst Inc",  100.90,"+2.7%"),
        (4,  "UtilityBridge Ltd", 192.10,"+1.2%","GasStream Corp",     159.40,"-0.8%"),
        (5,  "ElectricFirst Inc", 103.40,"+3.2%","PowerCore Corp",     139.20,"+1.4%"),
        (6,  "GasStream Corp",    162.10,"-0.3%","PowerCore Corp",     141.60,"+2.4%"),
        (7,  "UtilityBridge Ltd", 195.00,"+0.8%","ElectricFirst Inc",  105.90,"+0.6%"),
        (8,  "PowerCore Corp",    144.10,"+2.1%","GasStream Corp",     164.80,"-1.2%"),
        (9,  "ElectricFirst Inc", 108.40,"+1.7%","UtilityBridge Ltd",  197.90,"+3.3%"),
        (10, "GasStream Corp",    167.60,"-0.7%","PowerCore Corp",     146.80,"+1.9%"),
        (11, "PowerCore Corp",    149.50,"+0.8%","ElectricFirst Inc",  110.90,"+2.5%"),
        (12, "UtilityBridge Ltd", 200.80,"+2.7%","GasStream Corp",     170.40,"-0.9%"),
        (13, "ElectricFirst Inc", 113.40,"+1.4%","PowerCore Corp",     152.20,"+1.6%"),
        (14, "GasStream Corp",    173.20,"+3.8%","UtilityBridge Ltd",  203.70,"+0.8%"),
        (15, "PowerCore Corp",    155.00,"-0.4%","ElectricFirst Inc",  115.90,"+3.1%"),
    ],
    "Communication Services": [
        (1,  "MediaCore Corp",    267.40,"+1.6%","TelecomBridge Ltd",  198.60,"-0.7%"),
        (2,  "StreamFirst Inc",   134.80,"+2.9%","CommVault Corp",     312.40,"+1.4%"),
        (3,  "MediaCore Corp",    270.20,"-0.8%","StreamFirst Inc",    137.60,"+3.3%"),
        (4,  "TelecomBridge Ltd", 201.40,"+1.2%","CommVault Corp",     315.80,"-1.1%"),
        (5,  "StreamFirst Inc",   140.50,"+3.7%","MediaCore Corp",     273.10,"+1.3%"),
        (6,  "CommVault Corp",    319.20,"-0.5%","MediaCore Corp",     276.00,"+2.8%"),
        (7,  "TelecomBridge Ltd", 204.30,"+0.9%","StreamFirst Inc",    143.40,"+0.7%"),
        (8,  "MediaCore Corp",    278.90,"+2.3%","CommVault Corp",     322.60,"-1.4%"),
        (9,  "StreamFirst Inc",   146.30,"+1.8%","TelecomBridge Ltd",  207.20,"+3.6%"),
        (10, "CommVault Corp",    326.00,"-0.7%","MediaCore Corp",     281.80,"+1.9%"),
        (11, "MediaCore Corp",    284.70,"+0.8%","StreamFirst Inc",    149.20,"+2.7%"),
        (12, "TelecomBridge Ltd", 210.10,"+2.9%","CommVault Corp",     329.40,"-0.8%"),
        (13, "StreamFirst Inc",   152.10,"+1.5%","MediaCore Corp",     287.60,"+1.6%"),
        (14, "CommVault Corp",    332.80,"+4.2%","TelecomBridge Ltd",  213.40,"+0.9%"),
        (15, "MediaCore Corp",    290.50,"-0.6%","StreamFirst Inc",    155.00,"+3.4%"),
    ],
}

def get_returns(sector, rnd):
    row = ALL_ROUNDS[sector][rnd-1]
    ca = float(row[3].replace('%','').replace('+',''))
    cb = float(row[6].replace('%','').replace('+',''))
    return ca/100, cb/100

def get_phase(rnd):
    if rnd <= 5:  return 1
    if rnd <= 10: return 2
    return 3

DATA_FILE = "responses_A.csv"
CSV_HEADERS = (
    ["participant_id","condition","sector","hold_duration",
     "investment_goal","risk_tolerance","prolific_id","started_at","completed_at"] +
    [f"R{r}_{f}" for r in range(1,16)
     for f in ["stock_a","stock_b","alloc","conf","aci","return"]] +
    ["total_return","benchmark_return","portfolio_score",
     "mean_confidence","mean_accuracy","oci","mean_aci","correct_rounds"] +
    ["age","gender","education","experience",
     "robo_prior","manipulation_check","open_text"]
)

def ensure_csv():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE,'w',newline='') as f:
            csv.DictWriter(f,fieldnames=CSV_HEADERS).writeheader()

def save_response(data):
    ensure_csv()
    with open(DATA_FILE,'a',newline='',encoding='utf-8') as f:
        csv.DictWriter(f,fieldnames=CSV_HEADERS,
                       extrasaction='ignore').writerow(data)

def calc_feedback(rd, start_r, end_r):
    allocs,confs,acis=[],[],[]
    rounds_detail=[]
    chart_data=[]
    for r in range(start_r, end_r+1):
        alloc = float(rd.get(f'R{r}_alloc',50))
        conf  = float(rd.get(f'R{r}_conf', 50))
        aci   = abs(alloc-50)*2/100
        alloc_a = round(alloc*10)
        alloc_b = 1000-alloc_a
        allocs.append(alloc); confs.append(conf); acis.append(aci)
        rounds_detail.append({"round":r,"alloc_a":alloc_a,
            "alloc_b":alloc_b,"conf":round(conf,1),"aci":round(aci,2)})
        chart_data.append({"round":r,"alloc_a":alloc_a,
            "alloc_b":alloc_b,"conf":round(conf,1),"aci":round(aci,2)})
    avg_slider = sum(allocs)/len(allocs) if allocs else 50
    return {
        "avg_a":      round(avg_slider*10),
        "avg_b":      1000-round(avg_slider*10),
        "avg_conf":   round(sum(confs)/len(confs),1) if confs else 50.0,
        "avg_aci":    round(sum(acis)/len(acis),2) if acis else 0.0,
        "rounds":     rounds_detail,
        "chart_data": chart_data,
    }

def calc_final(sector, rd):
    rounds=ALL_ROUNDS.get(sector,ALL_ROUNDS["Information Technology"])
    total_return=benchmark_return=correct=0
    allocs,confs,acis=[],[],[]
    for row in rounds:
        rnd=row[0]
        alloc=float(rd.get(f'R{rnd}_alloc',50))
        conf=float(rd.get(f'R{rnd}_conf',50))
        ra,rb=get_returns(sector,rnd)
        aa=alloc*10; ab=1000-aa
        actual=(aa*ra)+(ab*rb); bench=(500*ra)+(500*rb)
        total_return+=actual; benchmark_return+=bench
        aci=abs(alloc-50)*2/100
        allocs.append(alloc); confs.append(conf); acis.append(aci)
        if actual>=bench: correct+=1
    mc=sum(confs)/len(confs) if confs else 50
    ma=(correct/15)*100
    return {
        "total_return":round(total_return,2),
        "benchmark_return":round(benchmark_return,2),
        "portfolio_score":round(total_return-benchmark_return,2),
        "mean_confidence":round(mc,1),
        "mean_accuracy":round(ma,1),
        "oci":round(mc-ma,1),
        "mean_aci":round(sum(acis)/len(acis),3) if acis else 0,
        "correct_rounds":correct,
    }

def build_ai_text(rnd, stock_a, stock_b, goal, risk, hold, rd):
    """Build Condition A AI text based on phase.
    IMPORTANT: No stock alignment signal — never says which stock is better.
    References profile and behavior only."""
    phase = get_phase(rnd)

    if phase == 1:
        # Rounds 1-5: Survey profile only
        return (
            f"Based on your <strong>{goal}</strong> investment goal, "
            f"your <strong>{risk}</strong> risk preference, and your "
            f"<strong>{hold}</strong> hold duration — both "
            f"<strong>{stock_a}</strong> and <strong>{stock_b}</strong> "
            f"are suitable for your portfolio this round."
        )

    elif phase == 2:
        # Rounds 6-10: Survey profile + behavioral history from rounds 1-5
        allocs = [float(rd.get(f'R{r}_alloc',50)) for r in range(1,6)]
        confs  = [float(rd.get(f'R{r}_conf', 50)) for r in range(1,6)]
        avg_slider = sum(allocs)/len(allocs) if allocs else 50
        avg_a   = round(avg_slider*10)
        avg_b   = 1000-avg_a
        avg_conf= round(sum(confs)/len(confs),1) if confs else 50.0
        return (
            f"Based on your <strong>{goal}</strong> investment goal, "
            f"your <strong>{risk}</strong> risk preference, your "
            f"<strong>{hold}</strong> hold duration, and your recent "
            f"investment pattern — averaging <strong>${avg_a}</strong> "
            f"toward Stock A and <strong>${avg_b}</strong> toward Stock B "
            f"with <strong>{avg_conf}%</strong> average confidence — both "
            f"<strong>{stock_a}</strong> and <strong>{stock_b}</strong> "
            f"are suitable for your portfolio this round."
        )

    else:
        # Rounds 11-15: Full accumulated profile from all previous rounds
        allocs = [float(rd.get(f'R{r}_alloc',50)) for r in range(1,11)]
        confs  = [float(rd.get(f'R{r}_conf', 50)) for r in range(1,11)]
        acis   = [abs(float(rd.get(f'R{r}_alloc',50))-50)*2/100 for r in range(1,11)]
        avg_slider = sum(allocs)/len(allocs) if allocs else 50
        avg_a   = round(avg_slider*10)
        avg_b   = 1000-avg_a
        avg_conf= round(sum(confs)/len(confs),1) if confs else 50.0
        avg_aci = round(sum(acis)/len(acis),2) if acis else 0.0
        return (
            f"Based on your <strong>{goal}</strong> investment goal, "
            f"your <strong>{risk}</strong> risk preference, your "
            f"<strong>{hold}</strong> hold duration, and your consistent "
            f"investment pattern across 10 rounds — averaging "
            f"<strong>${avg_a}</strong> toward Stock A and "
            f"<strong>${avg_b}</strong> toward Stock B with "
            f"<strong>{avg_conf}%</strong> average confidence and a "
            f"concentration index of <strong>{avg_aci}</strong> — both "
            f"<strong>{stock_a}</strong> and <strong>{stock_b}</strong> "
            f"are suitable for your portfolio this round."
        )

# ── ROUTES — CONDITION A ONLY ─────────────────────────────────────────────────

@app.route('/')
def index():
    session.clear()
    session['participant_id'] = str(uuid.uuid4())[:8]
    session['prolific_id']    = request.args.get('PROLIFIC_PID','')
    session['condition']      = 'A'  # FIXED — always Condition A
    session['started_at']     = datetime.now().isoformat()
    session['rd']             = {}
    return render_template('prestudy.html')

@app.route('/prestudy', methods=['POST'])
def prestudy_submit():
    session['hold_duration']   = request.form.get('hold_duration','')
    session['investment_goal'] = request.form.get('investment_goal','')
    session['risk_tolerance']  = request.form.get('risk_tolerance','')
    session['sector']          = request.form.get('sector_choice','Information Technology')
    return redirect(url_for('round_page', rnd=1))

@app.route('/round/<int:rnd>')
def round_page(rnd):
    if rnd < 1 or rnd > 15:
        return redirect(url_for('final_results'))
    sector   = session.get('sector','Information Technology')
    rnd_data = ALL_ROUNDS.get(sector, ALL_ROUNDS["Information Technology"])[rnd-1]
    rd       = session.get('rd',{})
    goal     = session.get('investment_goal','')
    risk     = session.get('risk_tolerance','')
    hold     = session.get('hold_duration','')
    stock_a  = rnd_data[1]
    stock_b  = rnd_data[4]
    ai_text  = build_ai_text(rnd, stock_a, stock_b, goal, risk, hold, rd)
    phase    = get_phase(rnd)
    return render_template('round.html',
        rnd=rnd, rnd_data=rnd_data,
        condition='A', sector=sector,
        ai_text=ai_text, phase=phase,
        total_rounds=15)

@app.route('/round/<int:rnd>/submit', methods=['POST'])
def round_submit(rnd):
    sector = session.get('sector','Information Technology')
    alloc  = float(request.form.get('allocation',50))
    conf   = float(request.form.get('confidence',50))
    aci    = abs(alloc-50)*2/100
    ra,rb  = get_returns(sector,rnd)
    aa=alloc*10; ab=1000-aa
    ret    = (aa*ra)+(ab*rb)
    row    = ALL_ROUNDS.get(sector,ALL_ROUNDS["Information Technology"])[rnd-1]
    rd     = session.get('rd',{})
    rd[f'R{rnd}_stock_a'] = row[1]
    rd[f'R{rnd}_stock_b'] = row[4]
    rd[f'R{rnd}_alloc']   = alloc
    rd[f'R{rnd}_conf']    = conf
    rd[f'R{rnd}_aci']     = round(aci,3)
    rd[f'R{rnd}_return']  = round(ret,2)
    session['rd'] = rd
    return redirect(url_for('trajectory', rnd=rnd))

@app.route('/trajectory/<int:rnd>')
def trajectory(rnd):
    sector   = session.get('sector','Information Technology')
    rnd_data = ALL_ROUNDS.get(sector,ALL_ROUNDS["Information Technology"])[rnd-1]
    if rnd == 5:    next_url = url_for('feedback', phase=1)
    elif rnd == 10: next_url = url_for('feedback', phase=2)
    elif rnd == 15: next_url = url_for('final_results')
    else:           next_url = url_for('round_page', rnd=rnd+1)
    return render_template('trajectory.html',
        rnd=rnd, rnd_data=rnd_data,
        next_url=next_url, sector=sector)

@app.route('/feedback/<int:phase>')
def feedback(phase):
    sector  = session.get('sector','Information Technology')
    rd      = session.get('rd',{})
    start_r = 1 if phase==1 else 6
    end_r   = 5 if phase==1 else 10
    summary = calc_feedback(rd, start_r, end_r)
    goal    = session.get('investment_goal','')
    risk    = session.get('risk_tolerance','')
    hold    = session.get('hold_duration','')
    return render_template('feedback.html',
        phase=phase, summary=summary,
        start_r=start_r, end_r=end_r,
        next_round=6 if phase==1 else 11,
        sector=sector, goal=goal,
        risk=risk, hold=hold)

@app.route('/final_results')
def final_results():
    sector  = session.get('sector','Information Technology')
    rd      = session.get('rd',{})
    results = calc_final(sector, rd)
    session['final_results'] = results
    return render_template('final_results.html', results=results)

@app.route('/post_survey', methods=['GET','POST'])
def post_survey():
    if request.method == 'POST':
        sector  = session.get('sector','Information Technology')
        rd      = session.get('rd',{})
        results = session.get('final_results', calc_final(sector, rd))
        row = {
            'participant_id':    session.get('participant_id'),
            'condition':         'A',
            'sector':            sector,
            'hold_duration':     session.get('hold_duration'),
            'investment_goal':   session.get('investment_goal'),
            'risk_tolerance':    session.get('risk_tolerance'),
            'prolific_id':       session.get('prolific_id'),
            'started_at':        session.get('started_at'),
            'completed_at':      datetime.now().isoformat(),
            **{k:v for k,v in rd.items()},
            **results,
            'age':                request.form.get('age'),
            'gender':             request.form.get('gender'),
            'education':          request.form.get('education'),
            'experience':         request.form.get('experience'),
            'robo_prior':         request.form.get('robo_prior'),
            'manipulation_check': request.form.get('manipulation_check'),
            'open_text':          request.form.get('open_text'),
        }
        save_response(row)
        return redirect(url_for('thankyou', pid=session.get('prolific_id','')))
    return render_template('post_survey.html')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html', pid=request.args.get('pid',''))

@app.route('/data')
def download_data():
    pw = request.args.get('pw','')
    if pw != 'raj_data_conditionA_2024':
        return "Access denied", 403
    if not os.path.exists(DATA_FILE):
        return "No data yet", 404
    with open(DATA_FILE,'r',encoding='utf-8') as f:
        content = f.read()
    return content, 200, {
        'Content-Type': 'text/csv',
        'Content-Disposition': 'attachment; filename=responses_A.csv'
    }

if __name__ == '__main__':
    ensure_csv()
    app.run(debug=True, port=5002)
