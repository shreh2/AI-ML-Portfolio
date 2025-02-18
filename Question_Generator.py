import openai
import json
import os


openai.api_key = os.getenv("OPENAI_API_KEY")
print(openai.api_key)

# def generate_interview_questions(job_description, technologies=[]):
#     """
#     Generates interview questions based on job description and relevant technologies.
#     :param job_description: str - The job description pasted by the user.
#     :param technologies: list - List of technologies mentioned in the resume.
#     :return: dict - Categorized interview questions.
#     """
#     categories = {
#         "Target Company & Role Specific Questions": [],
#         "Questions from Other Companies with Similar Role": [],
#         "Technology-Specific Questions": [],
#         "General Role-Based Questions": []
#     }
    
#     prompt = f"""
#     Generate categorized interview questions based on the following job description:
#     {job_description}

#     Categories:
#     1. Company-Specific Questions (For Amazon if applicable)
#     2. Other Companies' Questions for the same role
#     3. Technology-Specific Questions ({', '.join(technologies)})
#     4. General Role-Based Questions
#     """

#     try:
#         response = openai.chat.completions.create(
#             model="gpt-4o-mini",  # Use the latest available model
#             messages=[
#                 {"role": "system", "content": "You are an AI trained to generate technical and behavioral interview questions."},
#                 {"role": "user", "content": prompt}
#             ]
#         )

#         output_text = response.choices[0].message.content.strip()

#         # Simple parsing to split categories
#         question_blocks = output_text.split("\n\n")
#         for block in question_blocks:
#             for category in categories:
#                 if category in block:
#                     categories[category] = block.split("\n")[1:]
#                     break

#         return categories

#     except Exception as e:
#         return {"error": str(e)}

# # Example Usage
# job_desc = "Business Intelligence Engineer at Amazon focusing on SQL, Python, and data pipelines."
# technologies = ["SQL", "Python", "Snowflake"]
# questions = generate_interview_questions(job_desc, technologies)
# print(json.dumps(questions, indent=2))
