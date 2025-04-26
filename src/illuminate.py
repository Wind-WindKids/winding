import openai
from PIL import Image
import cv2

def main():
    print("Illuminate module loaded.")
    print("openai version:", openai.__version__)
    print("PIL version:", Image.__version__)
    print("cv2 version:", cv2.__version__)

if __name__ == "__main__":
    main()
