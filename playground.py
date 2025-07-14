import streamlit as st
import requests
from typing import List, Dict, Any
import os

# Constants
# API_BASE = os.getenv('BASE_API', "http://web:8000")
API_BASE = "http://web:8000"
DEFAULT_OPTION = "Select an option"


def fetch_data(endpoint: str, params: Dict[str, Any] = None) -> List[str]:
    """
    Fetch data from API endpoint with error handling

    Args:
        endpoint: API endpoint path
        params: Optional query parameters

    Returns:
        List of items or empty list if request fails
    """
    try:
        url = f"{API_BASE}/{endpoint}"
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()

        data = response.json()
        # Handle different response structures
        if endpoint == "grades":
            return data.get("grades", [])
        elif endpoint == "topics":
            return data.get("topics", [])
        return []

    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch {endpoint}: {str(e)}")
        return []
    except ValueError as e:
        st.error(f"Invalid response format from {endpoint}: {str(e)}")
        return []


def create_selectbox_options(items: List[str], default_text: str = DEFAULT_OPTION) -> List[str]:
    """Create selectbox options with default option"""
    if not items:
        return [default_text]
    return [default_text] + items


def initialize_sidebar():
    """Initialize and render the sidebar with AI Tutor settings"""

    with st.sidebar:
        st.title("📚 AI Tutor Settings")

        # Persona selection
        persona_options = ["Select persona", "friendly", "strict", "humorous"]
        persona = st.selectbox("Select Persona", persona_options)

        # Grade selection
        with st.spinner("Loading grades..."):
            grades_data = fetch_data("grades")

        grade_options = create_selectbox_options(grades_data, "Select grade")
        grade = st.selectbox("Select Grade", grade_options)

        # Topic selection (only if grade is selected)
        topic = "Select topic"  # Default value

        if grade and grade != "Select grade":
            with st.spinner("Loading topics..."):
                topic_params = {"grade": grade if grade != "All" else ""}
                topics_data = fetch_data("topics", topic_params)

            topic_options = create_selectbox_options(
                topics_data, "Select topic")
            topic = st.selectbox("Select Topic", topic_options)
        else:
            # Show disabled topic selectbox
            st.selectbox("Select Topic", ["Select topic"], disabled=True,
                         help="Please select a grade first")

        # Debug information (remove in production)
        if st.checkbox("Show Debug Info"):
            st.write("**Debug Information:**")
            st.write(f"Persona: {persona}")
            st.write(f"Grade: {grade}")
            st.write(f"Topic: {topic}")
            st.write(f"Grades available: {len(grades_data)}")

    return {
        "persona": persona if persona != "Select persona" else None,
        "grade": grade if grade != "Select grade" else None,
        "topic": topic if topic != "Select topic" else None
    }


# Usage
if __name__ == "__main__":
    # Initialize sidebar and get selections
    selections = initialize_sidebar()

    # ---- Chat UI ----
    if all(selections.values()):
        st.header("💬 Ask a Question")
        # Session state to store chat history
        # if "chat_history" not in st.session_state:
        #     st.session_state.chat_history = []

        # Message input
        user_input = st.chat_input("Type your question here...")
        # Even simpler version - just replace your existing chat section:

        if user_input:
            if not selections["persona"]:
                st.error("Please select a persona before asking a question.")
            else:
                with st.spinner("Thinking..."):
                    try:
                        payload = {
                            "query": user_input,
                            "persona": selections["persona"]
                        }

                        response = requests.post(
                            f"{API_BASE}/ask/",
                            json=payload,
                            headers={
                                "Content-Type": "application/json",
                                "Accept": "application/json"
                            },
                            timeout=120
                        )

                        # Handle response based on status code
                        if response.status_code == 200:
                            data = response.json()
                            ai_response = data.get(
                                "message", "No answer returned.")

                        elif response.status_code == 400:
                            try:
                                error_data = response.json()
                                if "No Information found" in error_data.get("message", ""):
                                    ai_response = "🤔 I don't have information about that topic in my knowledge base. Try asking about different topics or using more general terms."
                                else:
                                    ai_response = f"❌ {error_data.get(
                                        'error', error_data.get('message', 'Invalid request'))}"
                            except ValueError:
                                ai_response = "❌ Invalid response format"

                        else:
                            ai_response = f"❌ Request failed with status {
                                response.status_code}"

                    except requests.exceptions.Timeout:
                        ai_response = "⏱️ Request timed out. Please try again with a shorter question."
                    except requests.exceptions.ConnectionError:
                        ai_response = "🔌 Connection failed. Please check if the server is running."
                    except Exception as e:
                        ai_response = f"❌ Unexpected error: {str(e)}"

                # Always display the response
                with st.chat_message("assistant"):
                    if ai_response.startswith("❌"):
                        st.error(ai_response)
                    elif ai_response.startswith("🤔"):
                        st.warning(ai_response)
                    elif ai_response.startswith("⏱️") or ai_response.startswith("🔌"):
                        st.info(ai_response)
                    else:
                        st.markdown(ai_response)

    # Use the selections in your main app
    if all(selections.values()):
        st.success("All selections made! Ready to proceed.")
        # Your main application logic here
    else:
        st.info("Please make all selections in the sidebar to continue. All the response are from the file that are in knowledge base.")
