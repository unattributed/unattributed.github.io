---
layout: post
title: "Primer: Building Secure, Compliant & Cost-Efficient Domain-Specific LLMs for Cyber-Security & Infrastructure Teams"
date: 2025-08-21
author: unattributed
categories: [ai, llm, security-operations, cloud-security, self-hosting]
tags: [llama3, mistral, phi-3, lora, aws, azure, gcp, fedramp, gdpr, hipaa, cobalt-strike, threat-hunting]
---

> TL;DR  
> This 12 k-word field manual shows security engineers and infrastructure teams **how to train, harden, and run** their own LLMs—without leaking data, breaking the bank, or violating GDPR/HIPAA/FSTEC. Copy-paste configs, region-specific blueprints, and Colab-ready code included.

---

## 0. Why You Should Care

Commercial LLM APIs are **toxic** for high-sensitivity workloads:

<table>
  <thead>
    <tr>
      <th>Pain Point</th>
      <th>Real-World Impact</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>$0.06 / 1 k tokens</td>
      <td>1 M SOC alerts / mo ≈ $60 k</td>
    </tr>
    <tr>
      <td>GDPR Art. 44</td>
      <td>EU SOC logs can’t leave the region</td>
    </tr>
    <tr>
      <td>FedRAMP High</td>
      <td>Only AWS GovCloud or C2S</td>
    </tr>
    <tr>
      <td>Generic Reasoning</td>
      <td>“Block IP 10.0.0.12” turns into “Have you tried turning it off and on again?”</td>
    </tr>
  </tbody>
</table>

The fix is **Shift-Left AI**:

1. **Domain-Specific Training** on your logs, tickets, and threat intel.  
2. **Integration Programming** → strict JSON schemas, not prose.  
3. **Compliance-by-Design** → pick the right region, crypto, and tenancy.  
4. **Cost Engineering** → LoRA + spot GPUs + quantisation → **50–60 % cost cut**.

---

## 1. Model Selection Matrix

<table>
  <thead>
    <tr>
      <th>Model</th>
      <th>Params</th>
      <th>Strength</th>
      <th>VRAM (4-bit)</th>
      <th>Licence</th>
      <th>Use-Case Fit</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Llama 3 8B</strong></td>
      <td>8 B</td>
      <td>General reasoning</td>
      <td>6 GB</td>
      <td>Meta (commercial OK)</td>
      <td>Earnings calls, policy Q&amp;A</td>
    </tr>
    <tr>
      <td><strong>Mistral 7B</strong></td>
      <td>7 B</td>
      <td>Fast/cheap LoRA</td>
      <td>5 GB</td>
      <td>Apache-2.0</td>
      <td>Threat triage, log anomaly</td>
    </tr>
    <tr>
      <td><strong>Phi-3 3.8B</strong></td>
      <td>3.8 B</td>
      <td>Edge SOC boxes</td>
      <td>3 GB</td>
      <td>MIT</td>
      <td>Offline incident response</td>
    </tr>
    <tr>
      <td><strong>YaLM 100B (open)</strong></td>
      <td>100 B</td>
      <td>Multilingual</td>
      <td>60 GB</td>
      <td>Apache-2.0</td>
      <td>Public research</td>
    </tr>
    <tr>
      <td><strong>YaLM-2 (gov)</strong></td>
      <td>100 B</td>
      <td>Russia FSTEC</td>
      <td>60 GB</td>
      <td><strong>Custom licence</strong></td>
      <td>Air-gapped Kremlin subnet</td>
    </tr>
    <tr>
      <td><strong>Gemma 2B/7B</strong></td>
      <td>2–7 B</td>
      <td>Lightweight</td>
      <td>2–5 GB</td>
      <td>Google (commercial OK)</td>
      <td>Ticket classification</td>
    </tr>
  </tbody>
</table>

> Rule of thumb: start with **Mistral-7B + LoRA** on a T4; graduate to Llama-3-70B only if reasoning depth is poor.

---

## 2. Data Engineering Playbook

### 2.1 Extraction

<table>
  <thead>
    <tr>
      <th>Source</th>
      <th>Tooling</th>
      <th>Example Snippet</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Splunk</strong></td>
      <td><code>splunk-sdk</code> → JSON</td>
      <td><code>index=fw sourcetype=ids \| eval label="bruteforce"</code></td>
    </tr>
    <tr>
      <td><strong>CrowdStrike</strong></td>
      <td>FalconPy</td>
      <td><code>get_alerts(limit=10000)</code></td>
    </tr>
    <tr>
      <td><strong>Confluence</strong></td>
      <td><code>atlassian-python-api</code></td>
      <td>Strip macros, retain headings</td>
    </tr>
    <tr>
      <td><strong>Jira</strong></td>
      <td>REST API</td>
      <td>Map <code>summary + description → input</code>, <code>resolution → output</code></td>
    </tr>
    <tr>
      <td><strong>Slack</strong></td>
      <td><code>slack_sdk</code></td>
      <td>Export #incident-* channels</td>
    </tr>
  </tbody>
</table>

### 2.2 Cleaning

```bash
pip install text-dedup langchain
python -m text_dedup.minhash \
  --path "data/raw/" \
  --output "data/dedup/" \
  --column "text"
```

- Remove PII with `presidio-analyzer`.  
- Deduplicate >30 % on typical SOC dumps.  
- Convert to **conversational JSONL**:

```json
{"input": "SOC Alert: Brute-force on VPN (src_ip: 10.0.0.12)", "output": "{\"action\": \"block_ip\", \"target\": \"10.0.0.12\", \"confidence\": 0.92}"}
```

---

## 3. Fine-Tuning Recipes

### 3.1 LoRA (90 % of cases)

```python
from peft import LoraConfig, get_peft_model
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)
```

- **VRAM**: 7 B model → 6 GB (batch=1, 4-bit).  
- **Speed**: ~500 samples/sec on A100 80 GB.  
- **Convergence**: 3 epochs on 10 k samples ≈ 45 min.  
- **Parameter delta**: r × d_model × n_layers × 2 ≈ 262 k params (≈ 0.004 %).

### 3.2 Full Fine-Tuning (high-stakes)

<table>
  <thead>
    <tr>
      <th>Hyper-param</th>
      <th>Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Model</td>
      <td>Llama-3-8B</td>
    </tr>
    <tr>
      <td>GPUs</td>
      <td>8×A100 80 GB (NVLink)</td>
    </tr>
    <tr>
      <td>Batch</td>
      <td>32 (DP=8, GA=4)</td>
    </tr>
    <tr>
      <td>LR</td>
      <td>2e-5</td>
    </tr>
    <tr>
      <td>Time</td>
      <td>12 h / 50 k samples</td>
    </tr>
    <tr>
      <td>Cost (spot)</td>
      <td>~$180 (AWS p4d.24xlarge @ $3.06/h)</td>
    </tr>
  </tbody>
</table>

> Only when you need **max fidelity** (legal docs, medical).

### 3.3 Quantisation for Edge

```python
from transformers import BitsAndBytesConfig
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.float16
)
```

- Jetson AGX Orin (32 GB GPU slice) → **~40 tok/sec** for 4-bit Mistral-7B.  
- Latency <500 ms for SOC chat-bot.

---

## 4. Infrastructure Overhead Cheatsheet

### 4.1 Public Cloud (spot pricing 2025-08)

<table>
  <thead>
    <tr>
      <th>Provider</th>
      <th>GPU</th>
      <th>RAM</th>
      <th>$ / hr</th>
      <th>Region Lock</th>
      <th>Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>AWS</strong></td>
      <td>g4dn.xlarge (T4)</td>
      <td>16 GB</td>
      <td>$0.21</td>
      <td>Global</td>
      <td>Egress $0.09/GB</td>
    </tr>
    <tr>
      <td><strong>AWS</strong></td>
      <td>p4d.24xlarge (8×A100)</td>
      <td>320 GB</td>
      <td>$3.06</td>
      <td>us-east-1 / us-gov-west-1</td>
      <td>FedRAMP High</td>
    </tr>
    <tr>
      <td><strong>Azure</strong></td>
      <td>NC6s_v3 (T4)</td>
      <td>12 GB</td>
      <td>$0.45</td>
      <td>Global</td>
      <td>Private Link egress free</td>
    </tr>
    <tr>
      <td><strong>Azure</strong></td>
      <td>ND96amsr_A100_v4</td>
      <td>900 GB</td>
      <td>$2.97</td>
      <td>France Central (GDPR)</td>
      <td>EU-only storage</td>
    </tr>
    <tr>
      <td><strong>GCP</strong></td>
      <td>n1-standard-4 + T4</td>
      <td>16 GB</td>
      <td>$0.35</td>
      <td>europe-west4 (GDPR)</td>
      <td>VPC-SC</td>
    </tr>
    <tr>
      <td><strong>GCP</strong></td>
      <td>a2-ultragpu-8g (8×A100)</td>
      <td>320 GB</td>
      <td>$2.89</td>
      <td>europe-west4</td>
      <td>CMEK</td>
    </tr>
  </tbody>
</table>

> **Spot savings**: **50–60 %** (GPU) and **up to 80 %** on Azure Low-Priority VMs.

### 4.2 On-Prem / Air-Gapped

<table>
  <thead>
    <tr>
      <th>Component</th>
      <th>SKU</th>
      <th>Unit Cost</th>
      <th>5-yr TCO</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>GPU Node</strong></td>
      <td>2×A100 80 GB NVLink</td>
      <td>$20 k</td>
      <td><strong>$40 k total</strong> → $0.82 /hr amortised</td>
    </tr>
    <tr>
      <td><strong>Storage</strong></td>
      <td>Ceph 20 TB SSD</td>
      <td>$8 k</td>
      <td>$0.10 /GB</td>
    </tr>
    <tr>
      <td><strong>K8s</strong></td>
      <td>OpenShift + TGI</td>
      <td>$0</td>
      <td>Runs offline</td>
    </tr>
    <tr>
      <td><strong>NVIDIA AI Ent.</strong></td>
      <td>License</td>
      <td>$4 k / socket</td>
      <td>Includes support</td>
    </tr>
  </tbody>
</table>

> Physical isolation **eliminates** egress and compliance surface—mandatory for classified enclaves.

---

## 5. Regional Compliance Blueprints

### 5.1 EU GDPR – Finance Analytics

- **Location**: GCP `europe-west4`  
- **Storage**: Cloud Storage bucket with `EU_LOCATION` constraint  
- **Compute**: Vertex AI with VPC Service Controls  
- **Crypto**: CMEK or **Cloud HSM / external key** (FIPS 140-2 Level 3)

### 5.2 HIPAA – US Healthcare

- **Training**: SageMaker in **AWS GovCloud (us-gov-west-1)**  
- **Inference**: PrivateLink endpoint inside dedicated VPC  
- **PHI Redaction**: Lambda layer using `presidio-anonymizer`  
- **Audit**: CloudTrail + GuardDuty → Splunk

### 5.3 Israel Defense – Air-Gapped

- **Hardware**: 2×A100 80 GB, no NIC to Internet  
- **Stack**: OpenShift + TGI container (`ghcr.io/huggingface/text-generation-inference:1.4.2`)  
- **Model Signing**: GPG-sign every LoRA adapter  
- **Update Cycle**: USB sneakernet every 30 days

### 5.4 China DSL – Threat Intelligence

- **Provider**: Alibaba PAI (Ascend 910 NPUs)  
- **Data Residency**: MaxCompute in Beijing region  
- **Encryption**: SM4 for data at rest, TLS 1.3 CN-specific ciphers  
- **Model**: YaLM-100B fine-tuned on local SOC logs

### 5.5 Russia FSTEC – Sovereign Cloud

- **Provider**: Yandex DataSphere  
- **Encryption**: GOST 28147-89  
- **Hardware**: A100 cluster in Moscow DC  
- **Model**: YaLM-100B or custom 70 B Llama

---

## 6. Deployment Patterns

### 6.1 Real-Time SOC Co-Pilot

```yaml
# k8s/tgi-stack.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-triage
spec:
  replicas: 2
  selector:
    matchLabels: { app: llm-triage }
  template:
    metadata:
      labels: { app: llm-triage }
    spec:
      containers:
      - name: tgi
        image: ghcr.io/huggingface/text-generation-inference:1.4.2
        args:
          - --model-id=/mnt/models/mistral-7b-lora
          - --quantize bitsandbytes-nf4
        resources:
          limits:
            nvidia.com/gpu: 1
            memory: 8Gi
        volumeMounts:
          - { mountPath: /mnt/models, name: model }
      volumes:
        - name: model
          persistentVolumeClaim: { claimName: pvc-model }
```

- **Latency**: p95 < 400 ms  
- **Auto-scale**: KEDA on GPU utilisation > 80 %.

### 6.2 Batch Earnings-Call Pipeline

```python
# lambda_handler.py (AWS)
import boto3, sagemaker
sess = sagemaker.Session()
model = sagemaker.model.Model(
    image_uri="763104351884.dkr.ecr.us-east-1.amazonaws.com/huggingface-pytorch-inference:2.1.0-transformers4.40-gpu-py310-cu121-ubuntu22.04",
    model_data="s3://artifacts/llama3-earnings.tar.gz",
    role=role,
    sagemaker_session=sess)
model.deploy(
    initial_instance_count=2,
    instance_type="ml.g4dn.xlarge",
    endpoint_name="earnings-batch")
```

- **Throughput**: 600 calls / hour  
- **Cost**: \$0.012 per call (spot g4dn)

---

## 7. Monitoring & Guardrails

<table>
  <thead>
    <tr>
      <th>Layer</th>
      <th>Tool</th>
      <th>Check</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Drift</strong></td>
      <td>Weights &amp; Biases</td>
      <td>Perplexity ↑ > 10 % → retrain</td>
    </tr>
    <tr>
      <td><strong>Hallucinations</strong></td>
      <td>Eval dataset (1 k golden samples)</td>
      <td>F1 < 95 % → roll back</td>
    </tr>
    <tr>
      <td><strong>PII Leak</strong></td>
      <td>Presidio</td>
      <td>Regex post-filter</td>
    </tr>
    <tr>
      <td><strong>Output Schema</strong></td>
      <td><code>jsonschema</code></td>
      <td>Invalid JSON → retry w/ temperature=0</td>
    </tr>
  </tbody>
</table>

---

## 8. Cost Calculator (copy-paste)

```python
# cost.py
def training_cost(gpus, hours, spot_discount=0.55, rate=3.06):
    on_demand = gpus * hours * rate
    return on_demand * (1 - spot_discount)

def inference_cost(req_per_month, per_1k=0.012):
    return req_per_month * per_1k / 1000

print("Training:", training_cost(8, 12), "USD")
print("Inference:", inference_cost(1_000_000), "USD/month")
```

---

## 9. Quick-Start Colab Notebook

<https://colab.research.google.com/github/unattributed/llm-guide/blob/main/domain_llm_quickstart.ipynb>

> *The notebook is currently in a private repo.*  
> [Request access here](mailto:shopkeeper@unattributed.blog?subject=Colab%20Notebook%20Request) or clone the repo locally.
> Runs on **free T4**; fine-tunes Mistral-7B LoRA in 25 min on 5 k SOC alerts.

---

## 10. Checklist Before Go-Live

- [ ] Data cleaned + deduped  
- [ ] GPU spot quota approved  
- [ ] VPC-SC / PrivateLink tested  
- [ ] PII filter passes pen-test  
- [ ] JSON schema enforced  
- [ ] Drift job scheduled (weekly)  
- [ ] Cost budget + alerts set

---

## 11. Roadmap for Advanced Teams

<table>
  <thead>
    <tr>
      <th>Phase</th>
      <th>Milestone</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Q3</strong></td>
      <td>Multi-model routing (Phi-3 for edge, Llama-3 for deep)</td>
    </tr>
    <tr>
      <td><strong>Q4</strong></td>
      <td>RLHF on analyst feedback</td>
    </tr>
    <tr>
      <td><strong>Q1 26</strong></td>
      <td>Federated learning across 3 regions</td>
    </tr>
    <tr>
      <td><strong>Q2 26</strong></td>
      <td>Signed SBOM + reproducible builds</td>
    </tr>
  </tbody>
</table>

---

## 12. References & Credits

- HuggingFace PEFT docs  
- AWS “HIPAA on SageMaker” whitepaper  
- Google “VPC Service Controls Best Practices”  
- NVIDIA AI Enterprise Deployment Guide  
- unattributed.blog threat-hunting primers

```