import pdfplumber
import re
from flask import Flask, request, jsonify

app = Flask(__name__)

def extract_details_from_pdf(file_content):
    try:
        with pdfplumber.open(file_content) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()

        if not text:
            return {"error": "No text found in the PDF."}

        lines = text.splitlines()[:4]

        names = []

        name_match_1 = re.search(r"(Name|Full Name|Applicant)\s*[:\-\s]*([^\n]+)", "\n".join(lines))
        if name_match_1:
            names.append(name_match_1.group(2))

        name_match_2 = re.findall(r"\b[\w'\-]+ [\w'\-]+\b", "\n".join(lines))
        if name_match_2:
            names.extend(name_match_2)

        name_match_3 = re.findall(r"^[A-Z][a-z]+ [A-Z][a-z]+", lines[0])
        if name_match_3:
            names.extend(name_match_3)

        name_match_4 = re.findall(r"\b(Mr\.|Dr\.|Mrs\.|Prof\.)\s+[^\n]+", "\n".join(lines))
        if name_match_4:
            names.extend(name_match_4)

        name_match_5 = re.findall(r"\b[\wÀ-ſ]+(?:[\s'\-][\wÀ-ſ]+)*\b", "\n".join(lines))
        if name_match_5:
            names.extend(name_match_5)

        common_keywords = ["Address", "Phone", "Email"]
        filtered_lines = [line for line in lines if not any(keyword in line for keyword in common_keywords)]
        name_match_6 = re.findall(r"\b[\wÀ-ſ]+(?:[\s'\-][\wÀ-ſ]+)*\b", "\n".join(filtered_lines))
        if name_match_6:
            names.extend(name_match_6)

        extracted_name = names[0] if names else "Not Found"

        phone_match = re.findall(r"\+?\d{1,2}[-\s]?\(?\d{3}\)?[-\s]?\d{3}[-\s]?\d{4}", text)
        phone = phone_match[0] if phone_match else "Not Found"

        address_match = re.search(r"Address\s*[:\-\s]*([\w\s,]+(?:\s*\d+)?[\w\s,]+)", text)
        address = address_match.group(1) if address_match else "Not Found"

        email_match = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zAZ0-9.-]+\.[a-zA-Z]{2,}", text)
        email = email_match[0] if email_match else "Not Found"

        extracted_data = {
            "name": extracted_name,
            "address": address,
            "phoneNumber": phone,
            "email": email,
        }

        return extracted_data

    except Exception as e:
        return {"error": f"Failed to extract from PDF: {str(e)}"}

@app.route('/api/extract', methods=['POST'])
def extract():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file:
        try:
            extracted_data = extract_details_from_pdf(file)
            return jsonify(extracted_data)
        except Exception as e:
            return jsonify({"error": f"Error processing file: {str(e)}"}), 500
    else:
        return jsonify({"error": "Invalid file"}), 400

if __name__ == '__main__':
    app.run(debug=True)