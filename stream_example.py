from anthropic import Anthropic

client = Anthropic()

def add_message(role:str, content:str, messages:list[str]) -> None:
    """Add a message to the conversation history
    
    Args:
        role (str): The role of the message sender, i.e. "user" or "assistant"
        content (str): The content of the message
        messages (list[str]): The list of messages in the conversation
    """
    messages.append({"role": role, "content": content})
    
    
def main(model:str="claude-sonnet-4-0", num_tokens:int=1000, system_prompt:str=None, temperature:float=0.5) -> None:
    """Main function to run the conversation
    
    Args:
        model (str): The model to use for the response, defaults to "claude-sonnet-4-0"
        num_tokens (int): The maximum number of tokens in the response, defaults to 1000
        system_prompt (str): The system prompt to use for the response, defaults to None
        temperature (float): The temperature to use for the response, defaults to 0.5
        
    Returns:
        None
    """
    params = {
        "model": model,
        "max_tokens": num_tokens,
        "temperature": temperature
    }
    if system_prompt:
        params["system"] = system_prompt

    print("Type 'exit' to end the conversation")
    messages = []
    
    while True:
        print()
        user_input = input("You: ")
        add_message("user", user_input, messages)
        if user_input.lower() == "exit":
            print("Claude: Goodbye!")
            break
        
        with client.messages.stream(**params, messages=messages) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
                
            final_message = stream.get_final_message()
            add_message("assistant", final_message.content[0].text, messages)

                
      
if __name__ == "__main__":
    main()