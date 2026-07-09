import os
import dotenv
from pathlib import Path

from openai import OpenAI

dotenv.load_dotenv()

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")


def read_contracts_from_directory(directory):
    context = ''
    dir_path = Path(directory)
    # List all files recursively (excluding folders)
    files = [str(p) for p in dir_path.rglob("*") if p.is_file()]
    for file in files:
        if not file.endswith(".sol"):
            continue
        with open(file, "r") as f:
            source_code = f.read()
            context += f"\n\nFile: {file}\n{source_code}"
    return context

def read_audit_history_from_directory(directory):
    context = ''
    dir_path = Path(directory)
    # List all files recursively (excluding folders)
    files = [str(p) for p in dir_path.rglob("*") if p.is_file()]
    for file in files:
        if not file.endswith(".txt"):
            continue
        with open(file, "r") as f:
            source_code = f.read()
            context += f"\n\nFile: {file}\n{source_code}"
    return context


def main():
    # Code: Read the entire source codes from all files in ./target directory
    # LLM: Determine the entry function for auditing
    # LLM: Analyze the entry function for potential security vulnerabilities
    # LLM: Generate a report summarizing the findings and recommendations for improving security
    # Code: save the report to history/report.txt
    context = read_contracts_from_directory("./target")
    context += "\n\n--- Audit History --- Do not provide any previous audit findings or recommendations. Only new findings should be included in our answer ---\n\n"
    context += read_audit_history_from_directory("./history")

    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=[
            {"role": "system", "content": "You are a security auditor for smart contracts"},
            {"role": "user", "content": context},
        ],
        stream=True,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}}
    )

    answer = ""

    for chunk in response:
        # Check for the thinking phase content
        if hasattr(chunk.choices[0].delta, 'reasoning_content') and chunk.choices[0].delta.reasoning_content:
            print(chunk.choices[0].delta.reasoning_content, end="", flush=True)

        # Check for the final answer content
        elif chunk.choices[0].delta.content:
            answer += chunk.choices[0].delta.content
    print("\n\n--- Final Answer ---\n")
    print(answer)
    with open(f"history/report_{len(os.listdir('history'))}.txt", "a") as f:
        f.write(answer)
      
if __name__ == "__main__":
    main()