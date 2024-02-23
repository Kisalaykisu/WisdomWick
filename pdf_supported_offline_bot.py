import spacy
import fitz  # PyMuPDF

# Initialize spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Function to extract text from all pages of a given PDF
def extract_text_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    pdf_text = {}
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        text = page.get_text()
        pdf_text[page_num] = text.lower()  # Store text as lowercase to ease comparison
    pdf_document.close()
    return pdf_text

# Simple search function for demonstration
def search_in_pdf(pdf_text, question):
    question_doc = nlp(question.lower())
    keywords = [token.text for token in question_doc if token.is_stop == False and token.is_punct == False]
    for page_num, text in pdf_text.items():
        if all(keyword in text for keyword in keywords):
            return f"The information might be on page {page_num+1} of the document."
    return "I couldn't find information related to your question in the document."

# Load the PDF and index its text
pdf_text = extract_text_from_pdf("C:/Users/Kisalay/Downloads/Jonas-html_CSS/html-css-course/starter/04-CSS-Layouts/bot_pdf/javabook.pdf")  # Replace with your PDF's path

# Main interaction loop
def interact_with_bot():
    print("Hello! I'm your PDF assistant. How can I help you with the document? (Type 'exit' to quit)")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye! Have a great day.")
            break
        # Search the PDF for text related to the user's question
        response = search_in_pdf(pdf_text, user_input)
        print(f"Bot: {response}")

if __name__ == "__main__":
    interact_with_bot()
