
 
# pip install openai 
# if you saved the key under a different environment variable name, you can do something like:
from openai import OpenAI

client = OpenAI(
  api_key="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"
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": "write what is coding"}
  ]
)

print(completion.choices[0].message.content);
