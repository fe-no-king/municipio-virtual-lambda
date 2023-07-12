from dotenv import load_dotenv
import os

from src.app.individual_bpa import main as individual_bpa

load_dotenv()

# Main function
def main(IdBpaIndividual):

    individual_bpa(IdBpaIndividual)