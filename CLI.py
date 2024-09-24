print("正在加载库......")

from llama_cpp import Llama
import os


def list_model_files():
    models_dir = 'models'
    model_files = [f for f in os.listdir(models_dir) if f.endswith('.gguf')]
    return [os.path.join(models_dir, f) for f in model_files]


# 选择模型
available_models = list_model_files()
print("可用的模型：")
valid_models = [model for model in available_models if model.endswith('.gguf')]
if not valid_models:
    print("未找到模型。请输入一个有效的模型名称。")
else:
    for index, model_file in enumerate(valid_models, start=1):
        print(f"{index}. {model_file}")

    try:
        choice = int(input(f"请输入模型的序号选择一个模型: "))
        if 1 <= choice <= len(valid_models):
            model = valid_models[choice - 1]
            print("选中的模型：", model)
        else:
            print("无效的序号。退出...")
    except ValueError:
        print("输入的不是有效的数字。退出...")

# 加载模型
print("-" * 10)
gpu = int(input("输入 n_gpu_layers，输入 0 使用 CPU，输入 -1 使用最大值: "))
print("正在加载模型......")
llm = Llama(
    model_path=model,
    n_gpu_layers=gpu,
)


# 生成参数
def get_params():
    print("-" * 10)
    maxtoken = int(input("输入最大令牌数: "))

    print("-" * 10)
    temp = float(input("输入温度: "))

    print("-" * 10)
    Seed = int(input("输入种子: "))

    return maxtoken, temp, Seed


def get_prompt():
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

    return quality_tags, mode_tags, length_tags, general_tags


print("-" * 10)

while True:
    maxtoken, temp, Seed = get_params()
    while True:
        quality_tags, mode_tags, length_tags, general_tags = get_prompt()

        while True:
            output = llm(
                f"quality: {quality_tags}\naspect ratio: 1.0\ntarget: <|{length_tags}|> <|{mode_tags}|>\ntag: {general_tags}",
                max_tokens=maxtoken,
                temperature=temp,
                seed=Seed,
                echo=True
            )
            print(output['choices'][0]['text'])
            print("")

            # 询问用户是否重新生成
            user_input = input("是否重新生成？(y/n): ")
            if user_input.lower() != 'y':
                break

        # 询问用户是否继续获取新的提示
        user_input = input("是否获取新的提示？(y/n): ")
        if user_input.lower() != 'y':
            break

    # 询问用户是否重新获取参数
    user_input = input("是否重新获取参数？(y/n): ")
    if user_input.lower() != 'y':
        break
