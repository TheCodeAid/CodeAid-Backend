import requests

API_URL = "https://n93vhujiweb948st.us-east-1.aws.endpoints.huggingface.cloud"
headers = {
	"Accept" : "application/json",
	"Authorization": "Bearer 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",
	"Content-Type": "application/json"
}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

output = query({
	"inputs": "Can you please let us know more details about your ",
	"parameters": {
		"max_new_tokens": 150
	}
})
print(output)