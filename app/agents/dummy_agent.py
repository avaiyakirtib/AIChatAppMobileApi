def get_dummy_response(system_prompt: str, user_prompt: str) -> str:
    """
    This is a dummy agent function that now receives a personalized system prompt.
    """
    print("--- Dummy Agent Log ---")
    print(f"Received Personalized System Prompt: '{system_prompt}'")
    print(f"Received User Prompt: '{user_prompt}'")
    print("-----------------------")
    
    return (
        f"This is a dummy response. My instructions are: '{system_prompt}'. "
        f"I will now respond to your message: '{user_prompt}'. "
        f"The real AI is coming soon!"
    )

