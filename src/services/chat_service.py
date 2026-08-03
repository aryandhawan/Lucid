from src.services.retrieval_service import RetrievalService
from src.services.query_router import QueryRouter
from src.components.vectorstore import VectorStore
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.memory import ConversationBufferMemory
from dotenv import load_dotenv
import os
from pydantic import BaseModel

load_dotenv()


class ChatReply(BaseModel):
    reply: str


class ChatService:
    def __init__(self, vectorstore: VectorStore):
        self.retrieval_service = RetrievalService(vectorstore)
        self.query_router = QueryRouter()
        self.memory = ConversationBufferMemory(return_messages=False)

        llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
            temperature=float(os.getenv("GROQ_TEMPERATURE", 0.3)),
        )
        self.structured_llm = llm.with_structured_output(ChatReply)

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are the research assistant for Lucid, answering questions about papers from the user's
personal research digest.

Answer using ONLY the information in the retrieved excerpts. Do not use outside knowledge about
the topic, even if you're confident about it.

If the retrieved excerpts don't contain enough information to answer, say so plainly.

Mention which paper an answer came from when relevant, especially if multiple papers were retrieved."""),
            ("user", "Conversation so far:\n{history}\n\nRetrieved excerpts:\n{retrieved_excerpts}\n\nCurrent question: {user_message}")
        ])

        self.chain = self.prompt | self.structured_llm

    def chat(self, user_message: str, anchor_paper_id: str = None) -> str:
        decision = self.query_router.route_query(user_message, anchor_paper=anchor_paper_id)

        docs = self.retrieval_service.retrieve_documents(
            search_query=decision.search_query,
            retrieval_mode=decision.retrieval_mode,
            anchor_paper_id=anchor_paper_id
        )

        excerpts_text = "\n\n".join(d.page_content for d in docs)

        # 3. Generate a reply using the retrieved excerpts and conversation history
        history_text = self.memory.load_memory_variables({})["history"]
        result = self.chain.invoke({
            "history": history_text,
            "retrieved_excerpts": excerpts_text,
            "user_message": user_message
        })

        # 4. Save this turn to memory for future follow-ups
        self.memory.save_context({"input": user_message}, {"output": result.reply})

        return result.reply