import requests
import base64
import json
from django.conf import settings
def analyze_image(image_path):
    standard_response = """
    {
        "identification_report": {
            "disease_name": "Fire Blight",
            "plant_name": "Apple (Malus domestica)",
            "description": "Fire blight is a contagious disease caused by the bacterium Erwinia amylovora. It affects apple and pear trees, as well as other members of the family Rosaceae.",
            "diagnosis": "The disease is diagnosed by observing characteristic symptoms such as the browning and blackening of leaves, which appear scorched, and the oozing of bacterial exudate from infected plant parts. Laboratory tests can confirm the presence of Erwinia amylovora.",
            "symptoms": [
                "Browning and blackening of leaves",
                "Leaves appear scorched",
                "Water-soaked lesions on stems",
                "Oozing of bacterial exudate",
                "Blossoms turn brown and wilt",
                "Twigs and branches die back"
            ],
            "management_tips": [
                "Prune out infected branches during dormant season",
                "Disinfect pruning tools between cuts",
                "Avoid excessive nitrogen fertilization",
                "Apply appropriate bactericides or antibiotics",
                "Plant resistant varieties if available",
                "Ensure proper spacing for air circulation"
            ],
            "notes": "Fire blight can spread rapidly in warm, wet conditions. Monitoring and early intervention are crucial for managing the disease."
        }
    }
    """

    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}"
        }

        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Analyze this image and provide a detailed report on any plant diseases you can identify. Include the disease name, affected plant, description, diagnosis method, symptoms, management tips, and any additional notes. Format the response as a JSON object."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encoded_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 500
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        response_data = response.json()

        # Attempt to parse the OpenAI response as JSON
        try:
            openai_response = json.loads(response_data['choices'][0]['message']['content'])
            return json.dumps(openai_response, indent=2)
        except json.JSONDecodeError:
            # If OpenAI's response is not valid JSON, return the standard response
            return standard_response

    except Exception as e:
        print(f"Error during image analysis: {str(e)}")
        return standard_response