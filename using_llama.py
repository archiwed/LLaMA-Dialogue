import torch

from peft import PeftModel

from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import LLaMATokenizer, LLaMAForCausalLM, GenerationConfig

tokenizer = # Você pode inserir o tokenizer aqui
model = # Você pode inserir seu modelo aqui
    """ LLaMAForCausalLM.from_pretrained(,
    load_in_8bit=True,
    device_map='balanced',
)
"""

device = 'cuda' if torch.cuda.is_available() else 'cpu'

generate_params = {
    'do_sample': True,
    'temperature': 1,
    'top_p': 1,
    'typical_p': 1,
    'repetition_penalty': 1,
    'top_k': 50,
    'num_beams': 1,
    'penalty_alpha': 0,
    'min_length': 0,
    'length_penalty': 1,
    'no_repeat_ngram_size': 0,
    'early_stopping': False,
}

def generate_prompt(instruction, input=None):
    if input:
        return f"""Abaixo está uma instrução que descreve uma tarefa, juntamente com uma entrada que fornece mais contexto. Escreva uma resposta que complete adequadamente o pedido.

### Instrução:
{instruction}

### Entrada:
{input}

### Resposta:"""
    else:
        return f"""Abaixo está uma instrução que descreve uma tarefa. Escreva uma resposta que complete adequadamente o pedido.

### Instrução:
{instruction}

### Resposta:"""

def evaluate(instruction, input=None):
    prompt = generate_prompt(instruction, input)
    inputs = tokenizer(prompt, return_tensors="pt")
    input_ids = inputs["input_ids"].cuda()
    generation_output = model.generate(
        input_ids=input_ids,
        output_scores=True,
        max_new_tokens=256,
        **generate_params,
        return_dict_in_generate=True
    )
    for s in generation_output.sequences:
        output = tokenizer.decode(s)
        print(f"{robot_name}: {output.split('### Resposta:')[1].strip()}")      
        
robot_name = ':'
while True:
    user_input = input(f':')
    evaluate(user_input)
