import google.genai.types as types
import os

MODEL = "gemini-2.5-flash-lite"

GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")

retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)

# safety_settings = [
#     types.SafetySetting(
#         category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
#         threshold=types.HarmBlockThreshold.OFF,
#     ),
# ]

generate_content_config = types.GenerateContentConfig(
    #    safety_settings=safety_settings,
    temperature=0.28,
    max_output_tokens=1000,
    top_p=0.95,
)
