import os
import json
from typing import Dict, AsyncGenerator, Optional
from langchain_openai import AzureChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import HumanMessage, AIMessage
import logging
from functools import lru_cache

logger = logging.getLogger(__name__)

class CodeAssistChatService:
    def __init__(self):
        self.llm = AzureChatOpenAI(
            openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            temperature=0.7,
            streaming=True,
        )
        # Memory storage keyed by user ID
        self.memories: Dict[str, ConversationBufferMemory] = {}
        # Response cache
        self.response_cache: Dict[str, str] = {}
        
    def get_memory(self, user_id: str) -> ConversationBufferMemory:
        if user_id not in self.memories:
            self.memories[user_id] = ConversationBufferMemory(
                return_messages=True,
                memory_key="chat_history"
            )
        return self.memories[user_id]

    def get_cache_key(self, message: str, context_hash: str) -> str:
        """Create a unique key for caching"""
        return f"{message}:{context_hash}"

    def get_cached_response(self, message: str, context_hash: str) -> Optional[str]:
        """Get response from cache"""
        cache_key = self.get_cache_key(message, context_hash)
        return self.response_cache.get(cache_key)

    def save_to_cache(self, message: str, context_hash: str, response: str) -> None:
        """Save response to cache"""
        cache_key = self.get_cache_key(message, context_hash)
        self.response_cache[cache_key] = response

    def create_context_hash(self, context: Dict) -> str:
        """Create a hash of the context for caching"""
        return json.dumps(context, sort_keys=True)

    async def get_chat_response(self, message: str, context: Dict) -> AsyncGenerator[str, None]:
        try:
            memory = self.get_memory(context['userId'])
            context_hash = self.create_context_hash(context)
            
            # Check cache first
            cached_response = self.get_cached_response(message, context_hash)
            if cached_response:
                yield cached_response
                return

            # Construct the prompt with context
            prompt = ChatPromptTemplate.from_messages([
                ("system", """You are a helpful Mentor who helps students learn programming and solve problems. 
                 Being a Mentor, you should be able to explain the concepts in a way that is easy to understand.
                 Always refer yourself as a Mentor and NOT a coding assistant, helpful assistant, etc.
                 Do not give the solution directly, but rather guide the student to solve the problem themselves.
                 Don't provide test cases as it is an online hackathon and they will be given the test cases.
                 Use the provided context to help answer questions about 
                the programming problem. Be concise but thorough in your explanations.
                
                Current problem context:
                - Title: {problemTitle}
                - Concept: {concept}
                - Complexity: {complexity}
                - Programming Language: {programmingLanguage}
                - Problem Description: {problemDescription}
                
                If code is provided:
                ```{programmingLanguage}
                {currentCode}
                ```
                
                Test Cases: {testCases}
                
                If there are submission results:
                Passed: {submissionResults}
                
                Remember to:
                1. Reference specific parts of the code or problem when relevant
                2. Don't give the solution directly, but rather guide the student to solve the problem themselves
                3. Provide concrete examples when explaining concepts
                4. Suggest improvements if reviewing code
                5. Be encouraging and supportive
                6. Focus on teaching and understanding
                 
                 IMPORTANT:
                 - If question is not related to the problem, politely decline in a humorous tone."
                """),
                ("human", "{input}"),
            ])
            
            # Get chat history
            chat_history = memory.load_memory_variables({})
            
            # Format the prompt with context
            formatted_prompt = prompt.format_messages(
                input=message,
                chat_history=chat_history.get("chat_history", []),
                **context
            )

            # Stream the response
            response_text = ""
            async for chunk in self.llm.astream(formatted_prompt):
                if hasattr(chunk, 'content'):
                    response_text += chunk.content
                    yield chunk.content
            
            # Save to memory after completion
            memory.save_context(
                {"input": message},
                {"output": response_text}
            )
            
            # Cache the response
            self.save_to_cache(message, context_hash, response_text)

        except Exception as e:
            logger.error(f"Error in chat response: {str(e)}", exc_info=True)
            yield f"I apologize, but I encountered an error: {str(e)}"
