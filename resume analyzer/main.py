from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from http import HTTPStatus

app = Flask(__name__)


genai.configure(api_key="your-gemini-api-key")

def create_analysis_prompt(resume_text):
    """Create a detailed prompt for resume analysis."""
    return """
    Please analyze this resume and provide specific, actionable feedback in the following areas:
    1. Content and Structure
    2. Skills and Qualifications
    3. Impact and Achievements
    4. Formatting and Presentation
    
    Resume to analyze:
    {resume_text}
    """.format(resume_text=resume_text)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/review", methods=["POST"])
def review_resume():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), HTTPStatus.BAD_REQUEST
        
        resume_text = data.get("resume")
        if not resume_text or not resume_text.strip():
            return jsonify({"error": "No resume text provided"}), HTTPStatus.BAD_REQUEST

        
        prompt = create_analysis_prompt(resume_text)

        
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)

        if not response or not response.text:
            return jsonify({"error": "Failed to generate analysis"}), HTTPStatus.INTERNAL_SERVER_ERROR

       
        formatted_text = (
            response.text
            .replace("**", "")
            .replace("<br>", "\n")
            .strip()
        )

        return jsonify({"feedback": formatted_text})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), HTTPStatus.INTERNAL_SERVER_ERROR

if __name__ == "__main__":
    app.run(debug=True)





