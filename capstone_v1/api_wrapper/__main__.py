"""
Main entry point for the API wrapper package
Can be run as: python -m api_wrapper
"""

from .examples import *

if __name__ == "__main__":
    print("Chatbot API Wrapper - Examples")
    print("=" * 50)
    print("\nRun individual examples from examples.py or use the wrapper directly.\n")
    print("Quick start:")
    print("  from api_wrapper import ChatbotWrapper")
    print("  wrapper = ChatbotWrapper(openai_api_key='your-key')")
    print("  response = wrapper.chat(model='gpt-3.5-turbo', messages='Hello!')")
    print()

