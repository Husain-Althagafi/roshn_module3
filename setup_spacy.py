"""
Script to download spaCy language model
"""
import subprocess
import sys

def download_spacy_model():
    """Download the English language model for spaCy"""
    try:
        import spacy
        # Try to load the model
        try:
            nlp = spacy.load("en_core_web_sm")
            print("✓ spaCy model 'en_core_web_sm' already installed")
        except OSError:
            # Model not found, download it
            print("Downloading spaCy model 'en_core_web_sm'...")
            subprocess.check_call([
                sys.executable,
                "-m",
                "spacy",
                "download",
                "en_core_web_sm"
            ])
            print("✓ Successfully downloaded en_core_web_sm")
    except Exception as e:
        print(f"Error downloading spaCy model: {e}")
        print("\nPlease run manually:")
        print("python -m spacy download en_core_web_sm")

if __name__ == "__main__":
    download_spacy_model()
