# Imports
from openai import OpenAI
# Update with your API key
client = OpenAI(api_key="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")
# Create a thread where the conversation will happen
thread = client.beta.threads.create()
# Create the user message and add it to the thread
message = client.beta.threads.messages.create(thread_id=thread.id,role="user",content="gloves",)
# Create the Run, passing in the thread and the assistant
run = client.beta.threads.runs.create(thread_id=thread.id,assistant_id="asst_gJj5caPDYuPdxgOY4pIuVdBu")

# Periodically retrieve the Run to check status and see if it has completed
# Should print "in_progress" several times before completing
while run.status != "completed":
    keep_retrieving_run = client.beta.threads.runs.retrieve(thread_id=thread.id,run_id=run.id)
    print(f"Run status: {keep_retrieving_run.status}")
    if keep_retrieving_run.status == "completed":
        print("\n")
        break
# Retrieve messages added by the Assistant to the thread
all_messages = client.beta.threads.messages.list(thread_id=thread.id)
# Print the messages from the user and the assistant
print("###################################################### \n")
print(f"USER: {message.content[0].text.value}")
print(f"Expanded Query: {all_messages.data[0].content[0].text.value}")