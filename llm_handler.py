import logging
from typing import List
from config import AgentConfig


class LLMHandler:
    """Handles LLM API calls and response generation."""
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        try:
            if self.config.llm_provider == "groq":
                self._initialize_groq()
            elif self.config.llm_provider == "anthropic":
                self._initialize_anthropic()
            elif self.config.llm_provider == "openai":
                self._initialize_openai()
            else:
                self.logger.warning(f"Unknown LLM provider: {self.config.llm_provider}")
        except Exception as e:
            self.logger.error(f"Error initializing LLM client: {str(e)}")
    
    def _initialize_groq(self):
        """Initialize Groq client."""
        try:
            from groq import Groq
            if self.config.llm_api_key:
                self.client = Groq(api_key=self.config.llm_api_key)
                self.logger.info(f"Groq client initialized with model: {self.config.model_name}")
            else:
                self.logger.warning("No API key provided for Groq")
        except ImportError:
            self.logger.error("groq package not installed. Install with: pip install groq")
        except Exception as e:
            self.logger.error(f"Error initializing Groq client: {str(e)}")
    
    def _initialize_anthropic(self):
        try:
            import anthropic
            if self.config.llm_api_key:
                self.client = anthropic.Anthropic(api_key=self.config.llm_api_key)
                self.logger.info("Anthropic client initialized")
            else:
                self.logger.warning("No API key provided for Anthropic")
        except ImportError:
            self.logger.error("anthropic package not installed. Install with: pip install anthropic")
    
    def _initialize_openai(self):
        try:
            import openai
            if self.config.llm_api_key:
                openai.api_key = self.config.llm_api_key
                self.client = openai
                self.logger.info("OpenAI client initialized")
            else:
                self.logger.warning("No API key provided for OpenAI")
        except ImportError:
            self.logger.error("openai package not installed. Install with: pip install openai")
    
    def generate_response(self, query: str, context: str, pages: List[int]) -> str:
        try:
            prompt = self._build_prompt(query, context, pages)
            
            if self.config.llm_provider == "groq":
                return self._generate_groq(prompt)
            elif self.config.llm_provider == "anthropic":
                return self._generate_anthropic(prompt)
            elif self.config.llm_provider == "openai":
                return self._generate_openai(prompt)
            else:
                return self._generate_fallback(query, context, pages)
        except Exception as e:
            self.logger.error(f"Error generating LLM response: {str(e)}")
            return self._generate_fallback(query, context, pages)
    
    def _build_prompt(self, query: str, context: str, pages: List[int]) -> str:
        prompt = f"""You are an intelligent Enterprise Assistant for HCLTech. You help employees by answering questions based on the company's official documentation.

Context from HCLTech Annual Report (Pages: {pages}):
{context}

Question: {query}

Instructions:
1. Answer the question accurately based on the provided context
2. If the context contains the answer, cite the specific page numbers
3. If the context doesn't contain enough information, say so clearly
4. Be concise but comprehensive
5. Use professional language appropriate for enterprise communication
6. Format your response clearly with proper structure

Answer:"""
        return prompt
    
    def _generate_groq(self, prompt: str) -> str:
        """Generate response using Groq."""
        if not self.client:
            return self._generate_fallback_error("Groq client not initialized")
        
        try:
            # Groq API call with proper error handling
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an intelligent Enterprise Assistant for HCLTech. Provide accurate, professional responses based on company documentation."
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.config.model_name,  # Should be "llama-3.3-70b-versatile"
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                top_p=1,
                stream=False,
                stop=None,
            )
            
            response = chat_completion.choices[0].message.content
            self.logger.info(f"Response generated successfully with Groq (model: {self.config.model_name})")
            return response
            
        except Exception as e:
            self.logger.error(f"Error calling Groq API: {str(e)}")
            # Log more details for debugging
            self.logger.error(f"Model: {self.config.model_name}, Max tokens: {self.config.max_tokens}")
            return self._generate_fallback_error(str(e))
    
    def _generate_anthropic(self, prompt: str) -> str:
        if not self.client:
            return self._generate_fallback_error("Anthropic client not initialized")
        
        try:
            message = self.client.messages.create(
                model=self.config.model_name,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response = message.content[0].text
            self.logger.info("Response generated successfully with Anthropic")
            return response
        except Exception as e:
            self.logger.error(f"Error calling Anthropic API: {str(e)}")
            return self._generate_fallback_error(str(e))
    
    def _generate_openai(self, prompt: str) -> str:
        if not self.client:
            return self._generate_fallback_error("OpenAI client not initialized")
        
        try:
            response = self.client.ChatCompletion.create(
                model=self.config.model_name,
                messages=[
                    {"role": "system", "content": "You are an intelligent Enterprise Assistant for HCLTech."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature
            )
            
            answer = response.choices[0].message.content
            self.logger.info("Response generated successfully with OpenAI")
            return answer
        except Exception as e:
            self.logger.error(f"Error calling OpenAI API: {str(e)}")
            return self._generate_fallback_error(str(e))
    
    def _generate_fallback(self, query: str, context: str, pages: List[int]) -> str:
        return f"""Based on the HCLTech Annual Report (Pages: {pages}), here's the relevant context:

**Query:** {query}

**Retrieved Information:**
{context[:800]}...

**Citation:** Pages {pages} from HCLTech Annual Integrated Report 2024-25"""
    
    def _generate_fallback_error(self, error: str) -> str:
        return f"""**Error generating response:** {error}

Please check:
1. API key is correctly configured in .env file
2. Groq package is installed (pip install groq)
3. Model name is correct (llama-3.3-70b-versatile)
4. API provider service is available
5. Internet connection is active"""
    
    def generate_with_actions(self, query: str, context: str, pages: List[int], action_result: dict) -> str:
        prompt = f"""You are an intelligent Enterprise Assistant for HCLTech. 

The user requested an action, which has been executed. Now provide a helpful response that:
1. Confirms the action was completed
2. Provides relevant context from the documentation if applicable
3. Explains next steps if any

Context from HCLTech Annual Report (Pages: {pages}):
{context}

User Query: {query}

Action Executed:
- Type: {action_result.get('action_type')}
- Status: {action_result.get('status')}
- Details: {action_result.get('details')}

Provide a professional response:"""

        try:
            if self.config.llm_provider == "groq":
                return self._generate_groq(prompt)
            elif self.config.llm_provider == "anthropic":
                return self._generate_anthropic(prompt)
            elif self.config.llm_provider == "openai":
                return self._generate_openai(prompt)
            else:
                return self._generate_action_fallback(query, action_result, context, pages)
        except Exception as e:
            self.logger.error(f"Error generating response with actions: {str(e)}")
            return self._generate_action_fallback(query, action_result, context, pages)
    
    def _generate_action_fallback(self, query: str, action_result: dict, context: str, pages: List[int]) -> str:
        details = action_result.get('details', {})
        formatted_details = "\n".join([f"- {k.replace('_', ' ').title()}: {v}" for k, v in details.items() if k != "status"])
        
        return f"""**Action Completed Successfully**

**Query:** {query}
**Action Type:** {action_result.get('action_type')}
**Status:** {action_result.get('status')}
**Action ID:** {action_result.get('action_id')}

**Details:**
{formatted_details}

**Relevant Documentation (Pages {pages}):**
{context[:400]}
"""