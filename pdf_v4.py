import spacy
import fitz  # PyMuPDF
import os
import glob

# Initialize spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Function to get a list of all PDF files in a category's directory
def get_pdfs_in_category(category_name, base_path="C:/Users/Kisalay/Downloads/Jonas-html_CSS/html-css-course/starter/04-CSS-Layouts/bot_pdf"):
    # Construct the path to the category directory
    category_dir = os.path.join(base_path, category_name)  # Adjust the base path as needed
    
    # Use glob to list all PDF files in the directory
    pdf_files = glob.glob(os.path.join(category_dir, "*.pdf"))
    return pdf_files

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
    print("Hello! I'm your PDF assistant. How can I assist you today?")
    print("Please specify the category followed by your question. (Type 'exit' to quit)")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye! Have a great day.")
            break
        
        # Assume user input is in the format "category: question"
        try:
            category, user_question = user_input.split(": ", 1)
            category = category.strip().replace(" ", "_")  # Replace spaces with underscores to match directory names
            user_question = user_question.strip()
        except ValueError:
            print("Please specify the category followed by your question. For example, 'weather: what is the forecast?'")
            continue
        
        category_pdfs = get_pdfs_in_category(category)
        if not category_pdfs:
            print(f"No documents found for category '{category}'. Please try a different category.")
            continue
        
        response = None
        for pdf_path in category_pdfs:
            text_by_page = extract_text_from_pdf(pdf_path)
            response = find_answer_in_pdf(text_by_page, user_question)
            if response:
                print(f"Found information in {os.path.basename(pdf_path)}:")
                break  # Break after finding the first relevant document
        
        if not response:
            response = "I couldn't find information related to your question in the documents."
        
        print(response)

if __name__ == "__main__":
    interact_with_bot()
