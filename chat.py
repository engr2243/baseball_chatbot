import openai


# Set up the OpenAI API client
openai.api_key = "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"

# Define a function to generate a response from GPT-3
def generate_response(question,chat_log) -> str:
    prompt = f"{chat_log}Human: {question}\nAI:"

    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt,
      temperature=0,
      max_tokens=500,
      top_p=1,
      frequency_penalty=0.0,
      presence_penalty=0.14,
      stop=[" Human:", " AI:"])

    return response.choices[0].text