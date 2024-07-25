from openai import OpenAI
import json
import time


_API_KEY = "sk-None-p9ffPPgzyXVw4yHAcFOuT3BlbkFJiH7T2cTVFg0pWNEsC7ee"


client = OpenAI(api_key=_API_KEY)


def ask_batch_gpt(file_path):
    batch_input_file = client.files.create(file=open(file_path, "rb"), purpose="batch")

    batch_input_file_id = batch_input_file.id

    resp = client.batches.create(
        input_file_id=batch_input_file_id,
        endpoint="/v1/chat/completions",
        completion_window="24h",
        metadata={"description": "batalha de dados"},
    )
    return resp


def read_batch_gpt(id):
    resp_status = ["failed", "completed", "expired", "cancelled"]
    status = client.batches.retrieve(id)

    while status.status not in resp_status:
        time.sleep(5)
        print(f"Consultando em 5 segundos")
        status = client.batches.retrieve(id)

    file_response = client.files.content(status.output_file_id)
    json_resp = json.loads(file_response.text)
    print(json_resp["response"]["body"]["choices"][0]["message"]["content"])


jsonl_path = "dados.jsonl"
resp = ask_batch_gpt(jsonl_path)
read_batch_gpt(resp.id)
