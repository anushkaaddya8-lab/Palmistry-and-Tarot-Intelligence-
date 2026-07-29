from google import genai
from PIL import Image 

client = genai.Client(
    api_key=""
)

def analyze_palm(prompt, image_path=None):

    if image_path:
        image = Image.open(image_path)
        contents = [prompt, image]
    else:
        contents = prompt

    response = client.models.generate_content(
        model="models/gemini-3.6-flash",
        contents=contents
    )
    text = response.text
    text = text.replace("**", "")

    sections = ["Life", "Career", "Love", "Fortune","Personality","Recommendation","Life Trend"]
    result = {}

    for i, section in enumerate(sections):
        start = text.find(section + ":")

        if start == -1:
            result[section.lower()] = ""
            continue

        start += len(section) + 1

        if i < len(sections) - 1:
            end = text.find(sections[i + 1] + ":", start)
            value = text[start:end].strip()
        else:
            value = text[start:].strip()

        result[section.lower()] = value

    return result
def analyze_tarot(prompt):
    response = client.models.generate_content(
        model="models/gemini-3.6-flash",
        contents=prompt
    )

    text = response.text
    text = text.replace("**", "")

    return text