from pydantic import BaseModel
from typing import Literal, Optional
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()


class RouterDecision(BaseModel):
    retrieval_mode: Literal["single_paper", "cross_paper"]
    search_query: str


class QueryRouter:
    def __init__(self):
        llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0, api_key=os.getenv("GROQ_API_KEY"))
        self.structured_llm = llm.with_structured_output(RouterDecision)

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a query router for a research-paper chat assistant. Your job is to decide HOW the
next step should search for relevant content — you do not answer the question yourself.

Decide:
1. retrieval_mode:
   - "single_paper" — the question is genuinely about the anchor paper specifically.
   - "cross_paper" — the question requires looking beyond just the anchor paper, or there is no anchor.

   Treat the anchor paper as a soft starting point, not a hard restriction.

2. search_query: rewrite the message into a clear, standalone search query using the anchor
   paper's topic and/or conversation history if the raw message relies on implied context."""),
   
            ("user", "Anchor paper: {anchor_paper}\nConversation history: {history}\nUser's message: {user_message}")
        ])

        self.chain = self.prompt | self.structured_llm

    def route_query(self, user_message: str, anchor_paper: Optional[str] = None, history: Optional[str] = None) -> RouterDecision:
        if not anchor_paper:
            return RouterDecision(retrieval_mode="cross_paper", search_query=user_message)
        
        return self.chain.invoke({
            "anchor_paper": anchor_paper,
            "history": history or "None",
            "user_message": user_message
        })


if __name__ == "__main__":
    router = QueryRouter()
    result = router.route_query(
        user_message="How does this compare to other quantization methods?",
        anchor_paper="Quantization Techniques for LLM Inference"
    )
    print(result)