from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.core.chat_engine import SimpleChatEngine
from llama_index.core.memory.chat_memory_buffer import ChatMemoryBuffer
from typing import List 
from llama_index.core import Settings



def _messages_to_prompt(messages):
        prompt = ""
        system_found = False
        for message in messages:
            if message.role == "system":
                prompt += f"<|system|>\n{message.content}<|end|>\n"
                system_found = True
            elif message.role == "user":
                prompt += f"<|user|>\n{message.content}<|end|>\n"
            elif message.role == "assistant":
                prompt += f"<|assistant|>\n{message.content}<|end|>\n"
            else:
                prompt += f"<|user|>\n{message.content}<|end|>\n"

        # trailing prompt
        prompt += "<|assistant|>\n"

        if not system_found:
            prompt = (
                "<|system|>\nYou are a helpful AI assistant.<|end|>\n" + prompt
            )

        return prompt

class Completions():
    def __init__(self, simple_chat_engine:SimpleChatEngine) -> None:
        self.engine = simple_chat_engine

    def create(self, messages:List, model, max_tokens):
        h = messages
        m = h.pop()
        return self.engine.chat(message=m, chat_history=h)

class ChatEngine():
    # Wrapper to mimic OpenAI library
    def __init__(self, max_context_size) -> None:
        self.memory = ChatMemoryBuffer.from_defaults(token_limit=max_context_size * 0.9)
        self.chat_engine = SimpleChatEngine.from_defaults()
        self.completions = Completions(self.chat_engine)

class Phi3():
    def __init__(self, model_name, max_context_size=4096):
        self.llm = HuggingFaceLLM(
                model_name=model_name,
                model_kwargs={
                    "trust_remote_code": True,
                },
                generate_kwargs={"do_sample": False},
                tokenizer_name=model_name,
                query_wrapper_prompt=(
                    "<|system|>\n"
                    "You are a professional Financial and Business analyst working for a hedge fund.<|end|>\n"
                    "<|user|>\n"
                    "{query_str}<|end|>\n"
                    "<|assistant|>\n"
                ),
                messages_to_prompt=_messages_to_prompt,
                is_chat_model=True,
            )
        
        Settings.llm = self.llm
        self.chat = ChatEngine(max_context_size=max_context_size)

    def get_llm(self):
        return self.llm
    