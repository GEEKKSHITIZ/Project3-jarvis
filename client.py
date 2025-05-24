from openai import OpenAI

client = OpenAI(
    api_key="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",
)

completion = client.chat.completions.create( 
    model="gpt-3.5-turbo", 
    messages=[
        {"role": "system", "content": "You are a virtual assistant named Jarvis, skilled in general tasks"},
        {"role": "user", "content": "What is coding?"}
    ]
)

print(completion.choices[0].message.content)
