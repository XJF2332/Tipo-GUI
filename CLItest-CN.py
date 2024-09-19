from llama_cpp import Llama
import os


def list_model_files():
    models_dir = 'models'
    model_files = [f for f in os.listdir(models_dir) if f.endswith('.gguf')]
    return [os.path.join(models_dir, f) for f in model_files]


# 选择模型
available_models = list_model_files()
print("可用的模型：")
for model_file in available_models:
    if model_file.endswith('.gguf'):
        print(model_file)
        break
    else:
        print("未找到模型。请输入一个有效的模型名称。")

model = input(f"从可用的模型中选择一个模型名称: ")
if model not in available_models:
    print("无效的模型名称。退出...")
else:
    print("选中的模型：", model)

# 加载模型
print("-" * 10)
gpu = int(input("输入 n_gpu_layers，输入 0 使用 CPU，输入 -1 使用最大值: "))
llm = Llama(
    model_path=model,
    n_gpu_layers=gpu,
)

# 生成参数
print("-" * 10)
quality_tags = input("输入质量标签: ")

print("-" * 10)
print("""
可用的标签：
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
mode_tags = input("输入模式标签: ")

print("-" * 10)
print("""
可用的标签：
short
long
very long
""")
print("-" * 3)
length_tags = input("输入长度标签: ")

print("-" * 10)
general_tags = input("输入通用标签: ")

print("-" * 10)
maxtoken = int(input("输入最大令牌数: "))

print("-" * 10)
temp = float(input("输入温度: "))

print("-" * 10)
Seed = int(input("输入种子: "))

print("-" * 10)

output = llm(
    f"quality: {quality_tags}\naspect ratio: 1.0\ntarget: <|{length_tags}|> <|{mode_tags}|>\ntag: {general_tags}",
    # 提示
    max_tokens=maxtoken,
    temperature=temp,
    seed=Seed,
    echo=True
)

print(output['choices'][0]['text'])
