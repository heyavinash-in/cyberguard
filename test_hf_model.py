import sys
from transformers import pipeline

def test_huggingface_model(url):
    print(f"Loading kmack/malicious-url-detection model...")
    # Initialize pipeline
    pipe = pipeline("text-classification", model="kmack/malicious-url-detection")
    
    print(f"\nAnalyzing URL: {url}")
    result = pipe(url)
    print(f"Result: {result}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_url = sys.argv[1]
    else:
        test_url = "http://paypal.secure-login.verify.update.hacked-server.xyz:8081/login/verify/account?session=abcdefg@"
        
    test_huggingface_model(test_url)
