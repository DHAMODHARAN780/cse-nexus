import os
import google.generativeai as genai
from PyPDF2 import PdfReader

# ---------------------------
# Configure Gemini AI
# ---------------------------
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY environment variable not set")

genai.configure(api_key=GEMINI_API_KEY)


class RAGService:
    def __init__(self):
        # ✅ Use ONLY supported model
        self.model_name = "models/gemini-1.5-flash"
        try:
            self.model = genai.GenerativeModel(self.model_name)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Gemini model: {e}")

    # ---------------------------
    # PDF Text Extraction
    # ---------------------------
    def extract_text_from_pdf(self, pdf_path):
        try:
            if not os.path.exists(pdf_path):
                pdf_path = os.path.join(os.getcwd(), pdf_path)

            if not os.path.exists(pdf_path):
                print(f"PDF not found: {pdf_path}")
                return ""

            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
            return text

        except Exception as e:
            print(f"PDF extraction error ({pdf_path}): {e}")
            return ""

    # ---------------------------
    # Context Builder (RAG)
    # ---------------------------
    def get_relevant_context(self, query, content_list):
        context = ""
        sources = []

        for content in content_list:
            pdf_text = self.extract_text_from_pdf(content.filepath)
            if pdf_text:
                context += (
                    f"\n\n--- From {content.title} "
                    f"({content.subject}, Unit {content.unit}) ---\n"
                )
                context += pdf_text[:4000]

                sources.append({
                    "title": content.title,
                    "subject": content.subject,
                    "unit": content.unit,
                    "filepath": content.filepath
                })

        return context, sources

    # ---------------------------
    # Main Ask Doubt Logic
    # ---------------------------
    def answer_doubt(self, query, content_list=None, history=None):
        try:
            # Conversation history
            history_text = ""
            if history:
                for msg in history[-6:]:
                    role = "Student" if msg["role"] == "user" else "Assistant"
                    history_text += f"{role}: {msg['content']}\n"

            greetings = {"hi", "hii", "hello", "hey", "yo", "halo"}
            is_greeting = query.lower().strip() in greetings or len(query.split()) < 3

            context = ""
            sources = []

            if content_list and not is_greeting:
                context, sources = self.get_relevant_context(query, content_list)

            # Prompt construction
            if context:
                prompt = f"""
You are a helpful Computer Science & Engineering professor assistant at CSE NEXUS.

Conversation History:
{history_text}

Student Question:
"{query}"

Relevant Course Material:
{context}

Instructions:
- Answer clearly and educationally.
- Cite PDF content when used.
- If supplementing with general CS knowledge, mention it.
- Maintain conversational tone.
"""
            else:
                prompt = f"""
You are a helpful Computer Science & Engineering professor assistant at CSE NEXUS.

Conversation History:
{history_text}

Student Question:
"{query}"

Instructions:
- If greeting, respond warmly.
- Otherwise, answer using CS knowledge.
- Be concise, friendly, and clear.
"""

            response = self.model.generate_content(prompt)

            return {
                "answer": response.text,
                "sources": sources,
                "mode": "rag" if context else "general"
            }

        except Exception as e:
            print(f"Ask Doubt Error: {e}")
            return {
                "answer": "Sorry, I'm temporarily unable to answer your question. Please try again shortly.",
                "sources": [],
                "mode": "error"
            }


# ---------------------------
# Singleton Instance
# ---------------------------
rag_service = RAGService()
