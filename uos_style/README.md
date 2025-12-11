# UoS AI 20026 — Natural Language Processing

Minimal, classroom-friendly practice Jupyter Notebooks for the University of Seoul NLP course (AI 20026).   
Each notebook is Colab-ready and verified to run end-to-end on a T4 GPU.

- [Class page](https://uos-nlp.notion.site/Natural-Language-Processing-23d406a65da78073a8e0fb48bf204d17?pvs=143)
- License: MIT

## Run in Google Colab
Click and run cell-by-cell (Runtime → GPU). No local setup required.

- Pre-Training (PT): Train a tiny Llama-style Causal LM from scratch  
  [Open in Colab](https://colab.research.google.com/github/abzb1/UoS_AI_20026/blob/main/01_Pre-Training.ipynb)

- Supervised Fine-Tuning (SFT): LoRA SFT on a small instruction model  
  [Open in Colab](https://colab.research.google.com/github/abzb1/UoS_AI_20026/blob/main/02_Fine-Tuning.ipynb)

- GRPO (RL): Quick SFT + GRPO with Unsloth + vLLM for reasoning tasks  
  [Open in Colab](https://colab.research.google.com/github/abzb1/UoS_AI_20026/blob/main/03_GRPO.ipynb)

## What’s Inside
```
UoS_AI_20026/
├── 01_Pre-Training.ipynb   # PT: tiny Causal LM from scratch
├── 02_Fine-Tuning.ipynb    # SFT: LoRA fine-tuning for chat/instruction
├── 03_GRPO.ipynb           # GRPO: RL with simple reward functions
├── LICENSE                 # MIT
└── README.md
```

## Notes
- Tested on Google Colab (T4 GPU). 
- Uses public datasets/models from Hugging Face. 
- HF token is optional for public resources.
