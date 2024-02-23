import spacy
import fitz  # PyMuPDF
import os
import glob

# Initialize spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Function to get a list of all PDF files in a category's directory
def get_pdfs_in_category(category_name, base_path="path/to/categories"):
    # Construct the path to the category directory
    category_dir = os.path.join(base_path, category_name)  # Adjust the base path as needed
    
    # Use glob to list all PDF files in the directory
    pdf_files = glob.glob(os.path.join(category_dir, "*.pdf"))
    return pdf_files

# Function to determine the category of a question
def determine_question_category(question):
    # Lowercase the question for better matching
    question_lower = question.lower()
    if "weather" in question_lower:
        return "Weather_Related"
    elif any(prog_term in question_lower for prog_term in ["programming", "code", "java", "python"]):
        return "Programming"
    elif any(agri_term in question_lower for agri_term in ["agriculture", "farming", "cultivation"]):
        return "Agriculture"
    elif "space" in question_lower:
        return "Space"
    elif any(sport_term in question_lower for sport_term in ["sport", "football", "soccer", "basketball"]):
        return "Sports"
    return None

# Function to extract text from all pages of a given PDF
def extract_text_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    text_by_page = {}
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        text = page.get_text()
        text_by_page[page_num] = text  # Store text without lowering to show original content
    pdf_document.close()
    return text_by_page

# Function to analyze question and search PDF text for an answer
def find_answer_in_pdf(text_by_page, question):
    # Analyze the question
    question_doc = nlp(question.lower())
    question_keywords = [token.lemma_ for token in question_doc if not token.is_stop and not token.is_punct]
    
    # Search for the best match
    best_match = None
    highest_score = 0
    for page_num, page_text in text_by_page.items():
        page_doc = nlp(page_text.lower())  # Lowercase page text for matching
        score = sum(1 for token in page_doc if token.lemma_ in question_keywords)
        if score > highest_score:
            highest_score = score
            best_match = page_text
    
    return best_match or "I couldn't find information related to your question in the document."

# Main interaction loop
def interact_with_bot():
    print("Hello! I'm your PDF assistant. How can I help you with the document? (Type 'exit' to quit)")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye! Have a great day.")
            break
        
        category = determine_question_category(user_input)
        if category:
            category_pdfs = get_pdfs_in_category(category)
            response = None
            for pdf_path in category_pdfs:
                text_by_page = extract_text_from_pdf(pdf_path)
                response = find_answer_in_pdf(text_by_page, user_input)
                if response:
                    print(f"Bot: Found information in {os.path.basename(pdf_path)}")
                    break  # Break after finding the first relevant document
            if not response:
                response = "I couldn't find information related to your question in the documents."
        else:
            response = "I'm not sure which category your question falls into. Could you be more specific?"
        
        print(f"Bot: {response}")

if __name__ == "__main__":
    interact_with_bot()
