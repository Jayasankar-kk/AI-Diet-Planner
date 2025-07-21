from fastapi import FastAPI, HTTPException
import google.generativeai as genai
from autogen import ConversableAgent
from pydantic import BaseModel

# Initialize FastAPI
app = FastAPI()

# Configure the LLM
llm_config = {
    "model": "gemini-1.5-flash",
    "api_key": "AIzafdw2_DZQY",  # Replace with your actual API key
    "api_type": "google"
}

# Nutritional recommendation agent
dietary_recommendation_agent = ConversableAgent(
    name="Dietary_Recommendation_Agent",
    system_message='''You are a dietary recommendation agent.
    Based on the user's age, activity level, and any dietary preferences provided,
    suggest a personalized meal plan for one day. 
    Ensure your recommendations are balanced and suitable for the user's profile.''',
    llm_config=llm_config,
    human_input_mode="NEVER"
)

# Request model for dietary recommendation
class DietaryRequest(BaseModel):
    age: int
    gender: str
    activity_level: str
    dietary_preferences: str = None  # Optional

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Dietary Recommendation API!"}

# Dietary recommendation endpoint
@app.post("/recommendation/")
def get_recommendation(request: DietaryRequest):
    try:
        # Generate the input message for the agent
        user_message = {
            "content": f"I am {request.gender.lower()} of age {request.age}, with {request.activity_level.lower()} level of activity."
                       + (f" My dietary preferences are: {request.dietary_preferences}" if request.dietary_preferences else ""),
            "role": "user"
        }

        # Get the agent's response
        reply = dietary_recommendation_agent.generate_reply(messages=[user_message])

        return {"dietary_plan": reply}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
