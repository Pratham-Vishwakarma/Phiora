# Phiora - Image Scorer

Phiora is a desktop application that allows users to upload an image and analyzes the facial features to provide a score(out of 10) based on the golden ratio. The application uses OpenCV and Mediapipe libraries for face detection and landmark extraction, and then calculates various ratios to determine the overall score.

## Installation

To use Phiora, you will need to have the following dependencies installed:

- Python 3.x
- OpenCV
- Mediapipe
- Pillow (PIL)
- Tkinter

You can install these dependencies using pip:

```
pip install -r requirements.txt
```

## General Usage

1. You can download the [Phiora_Setup](https://github.com/Pratham-Vishwakarma/Phiora/releases/download/v1.5.0/Phiora_Setup_v1.5.0.exe) from releases.
2. Follow the setup instruction.
3. launch the Phiora application.
4.  Click the "Upload Image" button to select an image file.
5. The application will process the image, detect the face, and extract the facial landmarks.
6. The application will then calculate the ratios between various facial features and provide an overall score based on the golden ratio.
7. The processed image with the detected landmarks and the calculated score will be displayed in the application window.

## Developer Usage

1. Run the `main.py` script to launch the Phiora application.
2. Click the "Upload Image" button to select an image file.
3. The application will process the image, detect the face, and extract the facial landmarks.
4. The application will then calculate the ratios between various facial features and provide an overall score based on the golden ratio.
5. The processed image with the detected landmarks and the calculated score will be displayed in the application window.

## Contributing

If you would like to contribute to the Phiora project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes to your forked repository.
5. Submit a pull request to the main repository.

## License

Phiora is licensed under the [License](license.txt).