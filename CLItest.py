from llama_cpp import Llama
import os


def list_model_files():
    models_dir = 'models'
    model_files = [f for f in os.listdir(models_dir) if f.endswith('.gguf')]
    return [os.path.join(models_dir, f) for f in model_files]


# select model
available_models = list_model_files()
print("Available models:")
for model_file in available_models:
    if model_file.endswith('.gguf'):
        print(model_file)
        break
    else:
        print("Model not found. Please enter a valid model name.")

model = input(f"Enter model name from available models: ")
if model not in available_models:
    print("Invalid model name. Exiting...")
else:
    print("selected model: ", model)

# load model
print("-" * 10)
gpu = int(input("Enter n_gpu_layers, enter 0 for CPU, enter -1 for Max: "))
llm = Llama(
    model_path=model,
    n_gpu_layers=gpu,
)

# generation parameters
print("-" * 10)
quality_tags = input("Enter quality tags: ")

print("-" * 10)
print("""
Avaliable tags:
None
tag_to_long
long_to_tag
short_to_long
short_to_tag
tag_to_short_to_long
short_to_tag_to_long
short_to_long_to_tag
""")
print("-" * 3)
mode_tags = input("Enter mode tags: ")

print("-" * 10)
print("""
Avaliable tags:
short
long
very long
""")
print("-" * 3)
length_tags = input("Enter length tags: ")

print("-" * 10)
general_tags = input("Enter general tags: ")

print("-" * 10)
maxtoken = int(input("Enter max token: "))

print("-" * 10)
temp = float(input("Enter temperature: "))

print("-" * 10)
Seed = int(input("Enter seed: "))

print("-" * 10)

output = llm(
    f"quality: {quality_tags}\naspect ratio: 1.0\ntarget: <|{length_tags}|> <|{mode_tags}|>\ntag: {general_tags}",
    # Prompt
    max_tokens=maxtoken,
    temperature=temp,
    seed = Seed,
    echo=True
)

print(output['choices'][0]['text'])
