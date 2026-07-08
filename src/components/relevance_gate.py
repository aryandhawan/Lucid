from groq import Groq
import os 
from dotenv import load_dotenv
load_dotenv()
from src.entity.relevance_config import RelevanceConfig

class RelevanceClassifier:
    def __init__(self,config: RelevanceConfig):
        self.config = config
        
    def classify_relevance(self, paper: dict) -> bool:
        """
        Classifies the relevance of the given paper based on the interest profile and relevance threshold.

        Args:
            paper (dict): The paper to classify.
            """
        
        client=Groq(api_key=os.getenv("GROQ_API_KEY"))

        chat_completion = client.chat.completions.create(model=self.config.model_name, 
                                                         messages=[{"role": "system", "content": f"""You are a research paper relevance classifier for an AI/ML researcher.

                    Interest profile (topics this person cares about): {self.config.interest_profile}

                    Task: Score the paper below on a scale of 0 to 10, indicating how relevant it is to the interest profile.
                    - 10 = directly and centrally about one or more of these topics
                    - 5 = tangentially related or applies these topics as a minor component
                    - 0 = completely unrelated

                    Consider the core contribution of the paper, not just surface keyword overlap. A paper mentioning "LLM" in passing while focusing on an unrelated topic should score low.

                    Respond with ONLY the integer score. No explanation, no words, no punctuation — just the number."""}, 
                    {"role": "user", "content": f"title: {paper['title']}\nabstract: {paper['abstract']}"}], temperature=self.config.temperature)
        
        print(f"RAW RESPONSE: {repr(chat_completion.choices[0].message.content)}")  # Debug print to see the raw response
        score = int(chat_completion.choices[0].message.content.strip())

        return score
    
    def is_relevant(self, score: int) -> bool:
        return score >= self.config.relevance_threshold
    
    