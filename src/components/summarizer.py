from groq import Groq
from utils.common import *
from entity.summarization_config import SummarizationConfig
import os
from dotenv import load_dotenv
load_dotenv()

class Summarizer:
    def __init__(self,config: SummarizationConfig):
        self.config = config
        self.client=Groq(api_key=os.getenv("GROQ_API_KEY"))
        
    def summarize(self, paper: dict) -> str:
        """
        Summarizes the content of a research paper using the Groq API.
        """
        system_prompt = system_prompt = """You are summarizing AI/ML research papers for a daily digest email, written for an AI engineer/developer, not a business audience.

Task: Write a 3-4 sentence summary of the paper below, covering two things:
1. What the paper actually proposes or does — the core technical contribution, stated directly and precisely.
2. A concrete developer-facing implication — what this actually lets someone DO differently in practice. Be specific and technical, not business-y.

Examples of the right framing for the implication:
- A cheaper inference method → "this means you could serve the same model at lower token cost, or run larger batch sizes on the same hardware"
- A new GPU architecture/optimization → "this means you could run more powerful models locally that previously needed cloud-scale hardware"
- A new quantization technique → "this means you could deploy a comparable model on consumer GPUs like a 4090, without significant accuracy loss"
If the paper's implication isn't a resource/deployment one (e.g. it's a benchmark, dataset, or theoretical result), translate it into what changes for someone building or evaluating models instead — don't force a resource-saving claim where it doesn't fit.

Rules:
- No preamble ("This paper presents..." / "The authors propose...") — start directly with substance
- Avoid restating the title verbatim
- Keep technical precision — don't oversimplify terms that matter (e.g. keep "KV-cache compression," don't dumb it down)
- Output ONLY the summary text, no headers, no labels, no quotation marks"""

        summary = self.client.chat.completions.create(model=self.config.model_name,
                                       messages=[{"role": "system", "content": system_prompt},
                                                 {"role": "user", "content": f"this is the abstract of the paper: {paper['abstract']} and this is the title of the paper: {paper['title']}"}],
                                       temperature=self.config.temperature,
                                       max_tokens=self.config.max_summary_tokens
        
        )

        return summary.choices[0].message.content
    
