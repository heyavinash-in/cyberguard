from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import os

def generate_pdf():
    pdf_path = os.path.join(os.getcwd(), "CyberGuard_Simple_Guide.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        alignment=TA_CENTER,
        fontSize=24,
        spaceAfter=20,
        textColor="#1a365d"
    )
    
    heading_style = ParagraphStyle(
        'HeadingStyle',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        spaceBefore=16,
        textColor="#2b6cb0"
    )
    
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        spaceAfter=14,
        leading=16,
        alignment=TA_LEFT
    )

    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leftIndent=20,
        bulletIndent=10,
        spaceAfter=8,
        leading=16
    )

    Story = []
    
    Story.append(Paragraph("CyberGuard: A Simple Guide", title_style))
    Story.append(Paragraph("This guide explains how the CyberGuard project works in simple, non-technical terms. Read this to easily understand the project and confidently explain it to the jury.", body_style))
    
    # Section 1
    Story.append(Paragraph("1. What is CyberGuard?", heading_style))
    Story.append(Paragraph("CyberGuard is a security application that acts like a digital bodyguard. When you receive a suspicious link or text message, you paste it into CyberGuard. It instantly tells you if the link is a dangerous phishing attempt, or if it is safe to click.", body_style))
    
    # Section 2
    Story.append(Paragraph("2. The Two Halves of the Project", heading_style))
    Story.append(Paragraph("Think of the project like a restaurant:", body_style))
    Story.append(Paragraph("&bull; <b>The Frontend (The Dining Area):</b> This is the part the user sees on their screen. We built this using 'Next.js' and 'React'. It provides the beautiful design, the input boxes, and the red/green warning dials.", bullet_style))
    Story.append(Paragraph("&bull; <b>The Backend (The Kitchen):</b> This is the hidden engine that does all the hard work. We built this using 'Python' and 'FastAPI'. When the user pastes a link on the screen, the frontend sends it to the backend kitchen to be inspected.", bullet_style))

    # Section 3
    Story.append(Paragraph("3. How does it spot a fake link?", heading_style))
    Story.append(Paragraph("When the backend receives a link, it doesn't just guess. It passes the link through two layers of security:", body_style))
    
    Story.append(Paragraph("<b>Layer A: The Rule-Checker (Heuristics)</b>", body_style))
    Story.append(Paragraph("First, the program checks the link against a strict set of human rules. It looks for obvious red flags:", body_style))
    Story.append(Paragraph("&bull; <i>Typosquatting:</i> Is it trying to trick you by spelling a brand wrong? (e.g., 'net-flix.com' instead of 'netflix.com')", bullet_style))
    Story.append(Paragraph("&bull; <i>Hidden Subdomains:</i> Is the real website hiding? (e.g., 'paypal.com.scam-site.com')", bullet_style))
    Story.append(Paragraph("&bull; <i>Direct Downloads:</i> Will clicking the link instantly force you to download an .exe virus?", bullet_style))

    Story.append(Paragraph("<b>Layer B: The Artificial Intelligence (Machine Learning)</b>", body_style))
    Story.append(Paragraph("If the link passes the basic rules, we hand it over to the AI (Artificial Intelligence).", body_style))
    Story.append(Paragraph("&bull; We trained our AI model on over 800,000 real-world examples of safe and malicious links.", bullet_style))
    Story.append(Paragraph("&bull; The AI turns the words in the URL into mathematics (a process called 'TF-IDF').", bullet_style))
    Story.append(Paragraph("&bull; The AI then acts like a detective, recognizing hidden mathematical patterns that humans can't see, and gives the link a 'Threat Score' out of 100.", bullet_style))

    # Section 4
    Story.append(Paragraph("4. The Failsafe (Whitelisting)", heading_style))
    Story.append(Paragraph("Sometimes, Artificial Intelligence gets confused and flags a safe website as dangerous. To prevent this, we added a 'Whitelist Override'. If our Rule-Checker sees that a link is exactly 'paypal.com' or 'github.com', it immediately overrides the AI and forces the threat score to 0 (Safe).", body_style))

    # Section 5
    Story.append(Paragraph("5. The Final Output", heading_style))
    Story.append(Paragraph("Once the Python backend finishes checking the rules and asking the AI, it gathers all its findings and sends a report back to the frontend screen.", body_style))
    Story.append(Paragraph("The user doesn't see the complicated math. They just see a clean dashboard telling them exactly WHY the link is dangerous (e.g., 'Warning: This link is hiding its true destination.').", body_style))

    # Section 6
    Story.append(Paragraph("6. Key Takeaways for the Jury", heading_style))
    Story.append(Paragraph("&bull; <b>Hybrid System:</b> Emphasize that you didn't just use AI. You used AI combined with strict rules, which is how professional cybersecurity companies build tools.", bullet_style))
    Story.append(Paragraph("&bull; <b>Explainability:</b> Emphasize that your tool doesn't just say 'Bad Link'. It explains exactly WHY the link is bad, which helps educate users.", bullet_style))
    Story.append(Paragraph("&bull; <b>Full-Stack:</b> You built a complete product. A modern React user interface connected to a high-speed Python AI engine.", bullet_style))
    
    doc.build(Story)
    print(f"Simple Guide PDF generated successfully at {pdf_path}!")

if __name__ == '__main__':
    generate_pdf()
