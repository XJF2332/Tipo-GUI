import os
import random
from llama_cpp import Llama

def list_model_files():
    models_dir = 'models'
    model_files = [f for f in os.listdir(models_dir) if f.endswith('.gguf')]
    return [os.path.join(models_dir, f) for f in model_files]

def random_seed():
    return random.randint(1, 100000)

def load_model(model_path, gpu):
    return Llama(model_path=model_path, n_gpu_layers=gpu)

def upsampling_prompt(llm, quality_tags, mode_tags, length_tags, general_tags, max_token, temp, Seed):
    output = llm(
        f"quality: {quality_tags}\naspect ratio: 1.0\ntarget: <|{length_tags}|> <|{mode_tags}|>\ntag: {general_tags}",
        max_tokens=max_token,
        echo=True,
        temperature=temp,
        seed=Seed,
    )
    return output['choices'][0]['text']

def get_user_input(prompt, default=None):
    user_input = input(f"{prompt} (default: {default}): ")
    return user_input if user_input else default

def main_interactive():
    # List available models
    available_models = list_model_files()
    print("Available models:")
    for i, model in enumerate(available_models, 1):
        print(f"{i}. {model}")

    # Get user input with defaults
    model_path = get_user_input("Enter the path to the model file", available_models[0])
    n_gpu_layers = int(get_user_input("Enter the number of GPU layers to use", -1))
    quality_tags = get_user_input("Enter quality tags for the prompt", "high quality")
    mode_tags = get_user_input("Enter mode tags for the prompt (e.g., 'tag_to_long')", "tag_to_long")
    length_tags = get_user_input("Enter length tags for the prompt (e.g., 'long')", "long")
    general_tags = get_user_input("Enter general tags for the prompt", "text generation")
    max_tokens = int(get_user_input("Enter the maximum number of tokens", 1024))
    temperature = float(get_user_input("Enter the temperature for the model", 0.8))
    seed = int(get_user_input("Enter a random seed for reproducibility (or leave blank for a random seed)", random_seed()))

    # Load the model
    llm = load_model(model_path, n_gpu_layers)

    # Perform upsampling
    output = upsampling_prompt(llm, quality_tags, mode_tags, length_tags, general_tags, max_tokens, temperature, seed)
    print("Output:", output)

if __name__ == "__main__":
    main_interactive()
