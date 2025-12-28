import os
import google.generativeai as genai
from PyPDF2 import PdfReader

# Configure Gemini AI
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'AIzaSyARSMBPPXtiHEW6fP-Gu-W46SuiVFh44o8')
genai.configure(api_key=GEMINI_API_KEY)

class RAGService:
    def __init__(self):
        # Using gemini-1.5-flash as default, with fallback logic
        self.model_name = 'gemini-1.5-flash'
        try:
            self.model = genai.GenerativeModel(self.model_name)
        except Exception:
            # Fallback to older model name if 1.5-flash is not available
            self.model_name = 'gemini-pro'
            self.model = genai.GenerativeModel(self.model_name)
    
    def extract_text_from_pdf(self, pdf_path):
        """Extract text content from a PDF file"""
        try:
            # Ensure path is absolute and exists
            if not os.path.exists(pdf_path):
                # Try relative to project root
                pdf_path = os.path.join(os.getcwd(), pdf_path)
            
            if not os.path.exists(pdf_path):
                print(f"PDF not found: {pdf_path}")
                return ""

            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Error extracting PDF text from {pdf_path}: {e}")
            return ""
    
    def get_relevant_context(self, query, content_list):
        """Extract text from relevant PDFs based on the query"""
        context = ""
        sources = []
        
        for content in content_list:
            # Extract text from PDF
            pdf_text = self.extract_text_from_pdf(content.filepath)
            if pdf_text:
                # Add to context with source information
                context += f"\n\n--- From {content.title} ({content.subject}, Unit {content.unit}) ---\n"
                context += pdf_text[:4000]  # Increased limit slightly
                sources.append({
                    'title': content.title,
                    'subject': content.subject,
                    'unit': content.unit,
                    'filepath': content.filepath
                })
        
        return context, sources
    
    def answer_doubt(self, query, content_list=None, history=None):
        """
        Answer a student's doubt using AI with conversational history
        Args:
            query: The student's question
            content_list: List of Content objects (PDFs) to use as context
            history: List of previous messages for context
        Returns:
            dict with 'answer', 'sources', and 'mode'
        """
        try:
            # Build conversation history string
            history_text = ""
            if history:
                for msg in history[-6:]: # Keep last 3 exchanges
                    role = "Student" if msg['role'] == 'user' else "Assistant"
                    history_text += f"{role}: {msg['content']}\n"

            # Check for greetings or small talk
            greetings = ['hi', 'hii', 'hello', 'hey', 'yo', 'halo']
            is_greeting = query.lower().strip() in greetings or len(query.split()) < 3

            context = ""
            sources = []
            
            if content_list and not is_greeting:
                context, sources = self.get_relevant_context(query, content_list)

            # Construct Prompt
            if context:
                prompt = f"""You are a helpful Computer Science & Engineering professor assistant at CSE NEXUS. 
Current Conversation History:
{history_text}

New Question from Student: "{query}"

Relevant content from uploaded course materials (PDFs):
{context}

Based on the provided PDFs, give an educational answer. 
- Be conversational and friendly (like ChatGPT).
- If the answer is in the PDFs, cite them.
- If not fully in PDFs, use your general CS knowledge but mention you're supplementing.
- Maintain flow with the history provided above."""
            else:
                prompt = f"""You are a helpful Computer Science & Engineering professor assistant at CSE NEXUS.
Current Conversation History:
{history_text}

Student: "{query}"

Response Guidelines:
- If this is a greeting (like "Hii"), respond warmly and ask how you can help with their CS studies.
- If it's a question, answer using your general Computer Science knowledge.
- Be friendly, professional, and clear.
- Keep it concise (150-200 words)."""

            response = self.model.generate_content(prompt)
            return {
                'answer': response.text,
                'sources': sources,
                'mode': 'rag' if context else 'general'
            }
                
        except Exception as e:
            print(f"Error in AI response: {e}")
            # Fallback for 404 errors or other API issues
            if "404" in str(e) and self.model_name == 'gemini-1.5-flash':
                print("Fallback to gemini-pro due to 404")
                self.model = genai.GenerativeModel('gemini-pro')
                self.model_name = 'gemini-pro'
                return self.answer_doubt(query, content_list, history)
                
            return {
                'answer': f"I apologize, but I encountered an error. This usually happens if the API key is invalid or the model is overloaded. Error details: {str(e)}",
                'sources': [],
                'mode': 'error'
            }

# Create a singleton instance
rag_service = RAGService()
