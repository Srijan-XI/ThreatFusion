# ThreatFusion - Dataset Plan

## 📊 **FREE Cybersecurity Datasets for ThreatFusion**

This document contains all FREE datasets that can be used for training, testing, and improving ThreatFusion's capabilities.

---

## 🦠 **1. Malware Datasets**

### **VirusShare**
- **Link**: https://virusshare.com/
- **Cost**: 100% FREE
- **Size**: 40+ million malware samples
- **Format**: Malware binaries, hashes
- **Updates**: Daily
- **Use Case**: Malware classification, hash database, ML training
- **Registration**: Optional (required for sample downloads)
- **API**: Yes (FREE)

### **MalwareBazaar (Abuse.ch)**
- **Link**: https://bazaar.abuse.ch/
- **Cost**: 100% FREE
- **Size**: Fresh malware samples daily
- **Format**: Malware binaries, hashes, YARA rules
- **Updates**: Real-time
- **Use Case**: Fresh malware samples, testing scanner
- **Registration**: No
- **API**: Yes (FREE, unlimited)

### **EMBER Dataset**
- **Link**: https://github.com/elastic/ember 
- **Cost**: 100% FREE
- **Size**: 1.1 million PE files (900K training, 200K test)
- **Format**: JSON features, PE binaries
- **Labels**: Malware/Benign
- **Use Case**: ML training for malware detection
- **Provider**: Elastic Security
- **Download**: https://ember.elastic.co/ember_dataset_2018_2.tar.bz2

### **Malware Traffic Analysis**
- **Link**: https://malware-traffic-analysis.net/
- **Cost**: 100% FREE
- **Size**: Hundreds of PCAP files
- **Format**: PCAP, malware samples
- **Updates**: Weekly
- **Use Case**: Network analysis, malware behavior
- **Registration**: No
- **Download**: Direct

### **VirusTotal**
- **Link**: https://www.virustotal.com/
- **Cost**: FREE tier (4 requests/min)
- **Size**: Unlimited lookups
- **Format**: JSON API responses
- **Use Case**: File/URL reputation checking
- **Registration**: Yes (FREE)
- **API Key**: FREE

### **theZoo (Malware Repository)**
- **Link**: https://github.com/ytisf/theZoo
- **Cost**: 100% FREE
- **Size**: 1000+ malware samples
- **Format**: Binaries (password protected)
- **Use Case**: Research, testing
- **Warning**: Live malware - use with caution
- **Download**: GitHub

---

## 🌐 **2. Network Traffic Datasets**

### **CICIDS2017**
- **Link**: https://www.unb.ca/cic/datasets/ids-2017.html
- **Cost**: 100% FREE
- **Size**: 5 days of network traffic
- **Format**: CSV, PCAP
- **Labels**: Benign, DDoS, PortScan, Botnet, etc.
- **Records**: ~2.8 million
- **Use Case**: Network anomaly detection, IDS training
- **Download**: Direct from UNB

### **CICIDS2018**
- **Link**: https://www.unb.ca/cic/datasets/ids-2018.html
- **Cost**: 100% FREE
- **Size**: 10 days of network traffic
- **Format**: CSV, PCAP
- **Labels**: 14 attack types
- **Use Case**: Advanced IDS/IPS training
- **Download**: Direct from UNB

### **KDD Cup 1999**
- **Link**: http://kdd.ics.uci.edu/databases/kddcup99/kddcup99.html
- **Cost**: 100% FREE
- **Size**: 5 million records
- **Format**: CSV
- **Features**: 41 features
- **Labels**: Normal, DoS, Probe, R2L, U2R
- **Use Case**: Classic IDS benchmark
- **Download**: UCI Repository

### **NSL-KDD** remove from site
- **Link**: https://www.unb.ca/cic/datasets/nsl.html
- **Cost**: 100% FREE
- **Size**: Improved KDD Cup dataset
- **Format**: CSV
- **Improvements**: Removed duplicates, balanced
- **Use Case**: Better ML training than KDD Cup
- **Download**: Direct from UNB

### **UNSW-NB15**
- **Link**: https://research.unsw.edu.au/projects/unsw-nb15-dataset
- **Cost**: 100% FREE
- **Size**: 2.5 million records
- **Format**: CSV, PCAP
- **Labels**: 9 attack types
- **Features**: 49 features
- **Use Case**: Modern network intrusion detection
- **Download**: UNSW Sydney

### **CTU-13**
- **Link**: https://www.stratosphereips.org/datasets-ctu13
- **Cost**: 100% FREE
- **Size**: 13 scenarios of botnet traffic
- **Format**: PCAP, NetFlow
- **Use Case**: Botnet detection
- **Download**: Direct

---

## 📧 **3. Phishing & Spam Datasets**

### **PhishTank**
- **Link**: https://phishtank.org/
- **Cost**: 100% FREE
- **Size**: 10,000+ verified phishing URLs
- **Format**: JSON, CSV, XML
- **Updates**: Hourly
- **Use Case**: Phishing URL detection
- **API**: Yes (FREE)
- **Download**: Direct

### **OpenPhish**
- **Link**: https://openphish.com/
- **Cost**: FREE (Community feed)
- **Size**: Active phishing URLs
- **Format**: Text file
- **Updates**: Every 6 hours
- **Use Case**: Real-time phishing detection
- **Download**: Direct

### **SpamAssassin Public Corpus**
- **Link**: https://spamassassin.apache.org/old/publiccorpus/
- **Cost**: 100% FREE
- **Size**: 6000+ emails
- **Format**: Raw email files
- **Labels**: Spam/Ham
- **Use Case**: Email spam detection
- **Download**: Direct

### **Enron Email Dataset**
- **Link**: https://www.cs.cmu.edu/~enron/
- **Cost**: 100% FREE
- **Size**: 500,000+ emails
- **Format**: Raw email files
- **Use Case**: Email analysis, NLP training
- **Download**: CMU

---

## 🔓 **4. Vulnerability & Exploit Datasets**

### **NVD (National Vulnerability Database)**
- **Link**: https://nvd.nist.gov/
- **Cost**: 100% FREE
- **Size**: All CVEs (200,000+)
- **Format**: JSON, XML
- **Updates**: Daily
- **Use Case**: Vulnerability tracking
- **API**: Yes (FREE)
- **Download**: Direct

### **Exploit-DB**
- **Link**: https://www.exploit-db.com/
- **Cost**: 100% FREE
- **Size**: 50,000+ exploits
- **Format**: Text, code files
- **Search**: Yes
- **Use Case**: Exploit research
- **Download**: CSV export available
- **GitHub**: https://github.com/offensive-security/exploitdb

### **VulnDB (Risk Based Security)**
- **Link**: https://vulndb.cyberriskanalytics.com/
- **Cost**: FREE (limited)
- **Size**: Vulnerability database
- **Format**: Web interface
- **Use Case**: Vulnerability research

---

## 🎯 **5. Threat Intelligence Datasets**

### **AlienVault OTX (Open Threat Exchange)**
- **Link**: https://otx.alienvault.com/
- **Cost**: 100% FREE
- **Size**: Millions of IOCs
- **Format**: JSON API
- **Updates**: Real-time
- **Use Case**: Threat intelligence feeds
- **API**: Yes (FREE, unlimited)
- **Registration**: Yes (FREE)

### **Abuse.ch - URLhaus**
- **Link**: https://urlhaus.abuse.ch/
- **Cost**: 100% FREE
- **Size**: Malicious URLs
- **Format**: CSV, JSON
- **Updates**: Real-time
- **Use Case**: URL reputation
- **API**: Yes (FREE)

### **Abuse.ch - ThreatFox**
- **Link**: https://threatfox.abuse.ch/
- **Cost**: 100% FREE
- **Size**: IOCs (IPs, domains, hashes)
- **Format**: CSV, JSON
- **Updates**: Real-time
- **Use Case**: IOC feeds
- **API**: Yes (FREE)

### **Abuse.ch - Feodo Tracker**
- **Link**: https://feodotracker.abuse.ch/
- **Cost**: 100% FREE
- **Size**: Botnet C&C servers
- **Format**: CSV, JSON
- **Updates**: Real-time
- **Use Case**: Botnet detection
- **API**: Yes (FREE)

### **Emerging Threats**
- **Link**: https://rules.emergingthreats.net/
- **Cost**: FREE (Community rules)
- **Size**: Snort/Suricata rules
- **Format**: Rule files
- **Updates**: Daily
- **Use Case**: IDS/IPS rules
- **Download**: Direct

### **MISP Threat Sharing**
- **Link**: https://www.misp-project.org/
- **Cost**: 100% FREE (Open Source)
- **Size**: Community feeds
- **Format**: JSON, STIX
- **Use Case**: Threat intelligence platform
- **Self-Hosted**: Yes
- **GitHub**: https://github.com/MISP/MISP

### **Spamhaus**
- **Link**: https://www.spamhaus.org/
- **Cost**: FREE (for non-commercial)
- **Size**: IP/Domain blocklists
- **Format**: Text files
- **Updates**: Real-time
- **Use Case**: IP reputation
- **Lists**: DROP, EDROP, ASN-DROP

### **GreyNoise**
- **Link**: https://www.greynoise.io/
- **Cost**: FREE (Community API)
- **Size**: Internet scanner data
- **Format**: JSON API
- **Use Case**: Distinguish threats from noise
- **API**: Yes (FREE tier)

---

## 🔍 **6. IP/Domain Reputation Datasets**

### **ip-api.com**
- **Link**: https://ip-api.com/
- **Cost**: FREE (45 requests/min)
- **Size**: Unlimited lookups
- **Format**: JSON, XML, CSV
- **Use Case**: IP geolocation
- **API**: Yes (FREE)
- **Already Integrated**: ✅ In ThreatFusion

### **IPQualityScore**
- **Link**: https://www.ipqualityscore.com/
- **Cost**: FREE tier (5000 lookups/month)
- **Size**: IP/Email/URL reputation
- **Format**: JSON API
- **Use Case**: Fraud detection
- **API**: Yes (FREE tier)

### **AbuseIPDB**
- **Link**: https://www.abuseipdb.com/
- **Cost**: FREE tier (1000 checks/day)
- **Size**: IP abuse reports
- **Format**: JSON API
- **Use Case**: IP reputation
- **API**: Yes (FREE tier)
- **Already Integrated**: ✅ In ThreatFusion

### **Shodan**
- **Link**: https://www.shodan.io/
- **Cost**: FREE tier (100 results/month)
- **Size**: Internet-connected devices
- **Format**: JSON API
- **Use Case**: Asset discovery
- **API**: Yes (FREE tier)

### **URLScan.io**
- **Link**: https://urlscan.io/
- **Cost**: 100% FREE
- **Size**: Unlimited scans
- **Format**: JSON API
- **Use Case**: URL analysis
- **API**: Yes (FREE, unlimited)

---

## 📚 **7. General Security Datasets**

### **SecRepo**
- **Link**: http://www.secrepo.com/
- **Cost**: 100% FREE
- **Size**: Various security datasets
- **Format**: Logs, PCAP, malware
- **Use Case**: General security research
- **Download**: Direct

### **LANL Cyber Security Dataset**
- **Link**: https://csr.lanl.gov/data/cyber1/
- **Cost**: 100% FREE
- **Size**: 58 days of enterprise data
- **Format**: CSV
- **Data**: Auth events, network flows, DNS
- **Use Case**: Enterprise security analysis
- **Download**: Direct

### **Kaggle Security Datasets**
- **Link**: https://www.kaggle.com/datasets?search=security
- **Cost**: 100% FREE
- **Size**: Hundreds of datasets
- **Format**: Various
- **Use Case**: ML training, research
- **Download**: Kaggle account (FREE)

### **UCI Machine Learning Repository**
- **Link**: https://archive.ics.uci.edu/
- **Cost**: 100% FREE
- **Size**: 600+ datasets
- **Format**: Various
- **Use Case**: ML training
- **Download**: Direct

---

## 🎓 **8. Academic & Research Datasets**

### **Canadian Institute for Cybersecurity (CIC)**
- **Link**: https://www.unb.ca/cic/datasets/
- **Cost**: 100% FREE
- **Datasets**: CICIDS2017, CICIDS2018, CICDDoS2019, etc.
- **Format**: CSV, PCAP
- **Use Case**: Academic research, IDS training
- **Download**: Direct

### **CAIDA (Center for Applied Internet Data Analysis)**
- **Link**: https://www.caida.org/catalog/datasets/
- **Cost**: FREE (registration required)
- **Size**: Internet topology, DDoS attacks
- **Format**: Various
- **Use Case**: Network research
- **Download**: After registration

### **CRAWDAD (Community Resource for Archiving Wireless Data)**
- **Link**: https://crawdad.org/
- **Cost**: FREE (registration required)
- **Size**: Wireless network traces
- **Format**: Various
- **Use Case**: Wireless security research

---

## 📥 **Download & Usage Guide**

### **Recommended Download Order:**

1. **Start Small** (for testing):
   - PhishTank (phishing URLs)
   - MalwareBazaar (recent malware)
   - AlienVault OTX (threat intel)

2. **Medium Datasets** (for ML training):
   - CICIDS2017 (~3GB)
   - NSL-KDD (~20MB)
   - SpamAssassin Corpus (~100MB)

3. **Large Datasets** (for production):
   - EMBER (~1.1M samples)
   - VirusShare (requires registration)
   - UNSW-NB15 (~100GB)

### **Storage Structure:**

```
ThreatFusion/
├── data/
│   ├── datasets/
│   │   ├── malware/
│   │   │   ├── ember/
│   │   │   ├── malwarebazaar/
│   │   │   └── virushare/
│   │   ├── network/
│   │   │   ├── cicids2017/
│   │   │   ├── nsl-kdd/
│   │   │   └── unsw-nb15/
│   │   ├── phishing/
│   │   │   ├── phishtank/
│   │   │   └── openphish/
│   │   └── threat_intel/
│   │       ├── otx/
│   │       ├── urlhaus/
│   │       └── threatfox/
│   └── models/
│       └── trained/
```

### **Download Script Example:**

```bash
# Create directories
mkdir -p data/datasets/{malware,network,phishing,threat_intel}

# Download PhishTank
cd data/datasets/phishing
wget http://data.phishtank.com/data/online-valid.csv

# Download CICIDS2017
cd ../network
# Visit https://www.unb.ca/cic/datasets/ids-2017.html and download

# Download AlienVault OTX via API
cd ../threat_intel
# Use Python script with OTX API
```

---

## 🚀 **Integration with ThreatFusion**

### **For Machine Learning:**
```python
import pandas as pd
from sklearn.ensemble import RandomForest

# Load CICIDS2017
df = pd.read_csv('data/datasets/network/cicids2017/Monday-WorkingHours.csv')

# Train model
model = RandomForest()
model.fit(df[features], df['Label'])
```

### **For Threat Intelligence:**
```python
from network import ThreatIntelligence

# Use AlienVault OTX
threat_intel = ThreatIntelligence()
iocs = threat_intel.get_otx_indicators()
```

### **For Testing Scanner:**
```bash
# Test with malware samples
python run.py --scan data/datasets/malware/malwarebazaar/
```

---

## 📊 **Dataset Comparison**

| Dataset | Size | Type | Labels | Best For |
|---------|------|------|--------|----------|
| CICIDS2017 | 3GB | Network | Yes | IDS Training |
| EMBER | 1.1M files | Malware | Yes | ML Classification |
| PhishTank | 10K+ URLs | Phishing | Yes | URL Detection |
| NSL-KDD | 20MB | Network | Yes | Quick Testing |
| MalwareBazaar | Daily | Malware | Yes | Fresh Samples |
| AlienVault OTX | Millions | Threat Intel | Yes | IOC Feeds |

---

## ⚠️ **Important Notes**

### **Legal & Ethical:**
- ✅ All datasets listed are legally available for research
- ✅ Some require registration (always FREE)
- ⚠️ Malware samples should be handled in isolated environments
- ⚠️ Follow each dataset's terms of use
- ⚠️ Use for educational/research purposes only

### **Safety:**
- 🔒 Use virtual machines for malware analysis
- 🔒 Disable network when analyzing malware
- 🔒 Use sandbox environments
- 🔒 Never execute malware on production systems

### **Storage:**
- 💾 CICIDS2017: ~3GB
- 💾 EMBER: ~1GB (features), ~100GB (binaries)
- 💾 UNSW-NB15: ~100GB
- 💾 Plan for 200GB+ for comprehensive collection

---

## 🔄 **Update Schedule**

| Dataset | Update Frequency | Auto-Update Available |
|---------|------------------|----------------------|
| MalwareBazaar | Real-time | Yes (API) |
| PhishTank | Hourly | Yes (API) |
| AlienVault OTX | Real-time | Yes (API) |
| URLhaus | Real-time | Yes (API) |
| NVD | Daily | Yes (API) |
| VirusTotal | Real-time | Yes (API) |

---

## 📞 **Support & Resources**

- **GitHub Issues**: Report dataset problems
- **Community Forums**: Ask questions
- **Documentation**: Each dataset has its own docs
- **Research Papers**: Many datasets have associated papers

---

**Last Updated**: November 24, 2025  
**Total Datasets Listed**: 35+  
**Total Cost**: $0 (100% FREE) 💰✨

---

## 🎯 **Quick Start Recommendations**

### **For Beginners:**
1. PhishTank (small, easy)
2. NSL-KDD (classic, well-documented)
3. AlienVault OTX (API-based)

### **For ML Training:**
1. CICIDS2017 (network)
2. EMBER (malware)
3. SpamAssassin (email)

### **For Production:**
1. MalwareBazaar (fresh malware)
2. AlienVault OTX (threat intel)
3. AbuseIPDB (IP reputation)

**All datasets are 100% FREE and ready to use!** 🚀
