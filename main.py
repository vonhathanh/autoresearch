import os
import dotenv
from pathlib import Path

from openai import OpenAI

dotenv.load_dotenv()

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")


def main():
  # Code: Read the entire source codes from all files in ./target directory
  # LLM: Determine the entry function for auditing
  # LLM: Analyze the entry function for potential security vulnerabilities
  # LLM: Generate a report summarizing the findings and recommendations for improving security
  # Code: save the report to history/security_audit_report.txt
  context = ''
  dir_path = Path("target")
  # List all files recursively (excluding folders)
  files = [str(p) for p in dir_path.rglob("*") if p.is_file()]
  for file in files:
    if not file.endswith(".sol"):
      continue

    with open(file, "r") as f:
      source_code = f.read()
      context += f"\n\nFile: {file}\n{source_code}"

  print("Context:", context)

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

  for chunk in response:
    # Check for the thinking phase content
    if hasattr(chunk.choices[0].delta, 'reasoning_content') and chunk.choices[0].delta.reasoning_content:
        print(chunk.choices[0].delta.reasoning_content, end="", flush=True)
    
    # Check for the final answer content
    elif chunk.choices[0].delta.content:
        # You can add a visual divider when switching from thinking to answering
        if 'printed_divider' not in locals():
            print("\n\n--- Final Answer ---")
            printed_divider = True
        print(chunk.choices[0].delta.content, end="", flush=True)
      
if __name__ == "__main__":
  main()