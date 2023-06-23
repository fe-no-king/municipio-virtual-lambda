from dotenv import load_dotenv
import os

from app.individual_bpa import main as individual_bpa

load_dotenv()

# Main function
def main():

    individual_bpa(5)

# Execution of the main function
if __name__ == "__main__":
    main()