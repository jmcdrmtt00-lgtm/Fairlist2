import streamlit as st
import google.generativeai as genai

# 1. Configure the API Key
# We get this from the "Secrets" (safe storage) in Streamlit
# If you are running this locally, you might get an error until you set up the key.
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    st.warning("Please add your GOOGLE_API_KEY to the Streamlit Secrets!")

# 2. The "Chef" (The AI Logic)
def make_compliant(text_input):
    # The prompt you designed in AI Studio
    prompt = f"""
    You are a Fair Housing Compliance Expert. 
    Rewrite the following real estate description to be appealing but legally safe. 
    Strictly avoid phrases that violate fair housing laws (like 'bachelor pad', 'walking distance to church', 'perfect for families').
    
    Original Description: {text_input}
    
    Compliant Description:
    """
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text

# 3. The "Menu" (The Web Page Interface)
st.title("🏡 Fair Housing Listing Assistant")
st.write("Paste your draft listing below, and the AI will rewrite it to be compliant with Fair Housing laws.")

# Text area for user input
user_text = st.text_area("Draft Description", height=150, placeholder="E.g., Great bachelor pad near the church...")

# The "Order" Button
if st.button("Make Compliant"):
    if user_text:
        with st.spinner("Consulting the compliance expert..."):
            try:
                # Call the function
                result = make_compliant(user_text)
                st.success("Here is your compliant listing:")
                st.markdown(result)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter some text first.")
