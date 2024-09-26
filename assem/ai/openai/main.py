from openai import OpenAI
client = OpenAI(api_key="sk-QniG_izcAmzWlqy4R4t7xERI3ABYfk4hgAhBustuaXT3BlbkFJGcGlSqNKssmg49im_ZiJHL21o-hlBEzbuAe2pj6U0A")


def generateAnswereAI():
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[

        ]
    )