from llm_helper import llm
from few_shot_posts import PostDataset

few_shot = PostDataset()

def get_length_str(length):
    if length == "Short":
        # Keep short post concise
        return "1 to 5 lines. Keep sentences concise."
    if length == "Medium":
        # Request a single, full paragraph of text (6 to 10 lines long)
        return "6 to 10 lines. Output the text as a SINGLE, DENSE BLOCK OF TEXT (ONE PARAGRAPH). DO NOT use double line breaks (\\n\\n) or empty lines."
    if length == "Long":
        # Request a single, full paragraph of text (11 to 15 lines long)
        return "11 to 15 lines. Output the text as a SINGLE, DENSE BLOCK OF TEXT (ONE PARAGRAPH). DO NOT use double line breaks (\\n\\n) or empty lines."

def generate_post(length, language, tag):
    prompt = get_prompt(length, language, tag)
    response = llm.invoke(prompt)
    return response.content

def get_prompt(length, language, tag):
    length_str = get_length_str(length)
    
    # Base prompt with an explicit instruction for creativity and uniqueness
    prompt = f'''
Generate a professional and engaging LinkedIn post using the below information. The post must be unique and creative; do not repeat previous content or default to a simple translation. No preamble.

1) Topic: {tag}
2) Length: {length_str}
3) Language: {language}
'''

    # Only load few-shot examples if the selected language matches the examples' language.
    if language in ["English", "Hinglish"]:
        examples = few_shot.get_filtered_posts(length, language, tag)
    else:
        examples = []
        
    if examples:
        prompt += "\n\n4) Use the writing style as per the following examples."

        for i, post in enumerate(examples):
            prompt += f'\n\nExample {i+1}:\n{post["text"]}'
            if i == 1:  # Use max two samples
                break

    # Add specific instructions for Hinglish
    if language == "Hinglish":
        prompt += "\n\nNote: Hinglish is a mix of Hindi and English. The script for the generated post should always be English (Roman)."
    
    return prompt

if __name__ == "__main__":
    print(generate_post("Medium", "English", "Mental Health"))