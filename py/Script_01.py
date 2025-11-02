import pandas as pd
import re
from transformers import pipeline

# 🚀 Use a reliable, instruction-following model (fast + accurate)
generator = pipeline(
    "text-generation",
    model="microsoft/Phi-3-mini-4k-instruct",
    torch_dtype="auto",
    device_map="auto"
)

def generate_testcases(feature_name: str, description: str, num_cases: int = 5):
    prompt = f"""
You are a senior QA engineer.

Generate exactly {num_cases} clear, structured, one-line manual test cases.

Feature: {feature_name}
Description: {description}

Each test case must be ONE SINGLE LINE in this format:
Test ID, Title, Preconditions, Steps, Expected Result, Type, Severity

Example:
TC001, Verify login with valid credentials, User must have valid account,
1. Open login page 2. Enter credentials 3. Click Login,
User should be redirected to dashboard, Positive, High

Rules:
- Write exactly {num_cases} test cases (TC001 to TC00{num_cases})
- Each must have exactly 6 commas (7 fields total)
- Output only the test case lines (no bullets, numbering, or comments)
- Order test cases from most complex to simplest
- Use concise QA-style language
"""

    result = generator(
        prompt,
        max_new_tokens=600,
        do_sample=False,
        temperature=0.2,
        top_p=0.9
    )
    text = result[0]['generated_text']
    return text.strip()


def parse_testcases(text):
    """Extract only valid, comma-separated test cases"""
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    data = []

    for line in lines:
        if re.match(r"^TC\d{3},", line) and line.count(",") == 6:
            parts = [p.strip() for p in line.split(",")]
            data.append(parts[:7])

    # Keep only first 5 valid lines
    return data[:5]


def save_to_excel(excel_file: str, text_output: str):
    header = ["Test ID", "Title", "Preconditions", "Steps", "Expected Result", "Type", "Severity"]
    data = parse_testcases(text_output)

    if not data:
        print("⚠️ No valid test cases found. Here's model output:\n")
        print(text_output)
        return

    df = pd.DataFrame(data, columns=header)
    df.to_excel(excel_file, index=False)
    print(f"✅ {len(data)} Test cases saved successfully to {excel_file}")


if __name__ == "__main__":
    feature = input("Enter feature/module name: ")
    desc = input("Enter short description: ")

    print("\n⚙️ Generating test cases... please wait ⏳\n")
    text_output = generate_testcases(feature, desc)

    print("---- MODEL OUTPUT ----")
    print(text_output)
    print("----------------------\n")

    save_to_excel("testcases.xlsx", text_output)
