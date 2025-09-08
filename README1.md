<p align="center">
  <img src="./public/phiora_logo.ico" alt="Phiora Logo" width="120" height="120"/>
</p>
<h1 align="center">Phiora</h1>
<p align="center"><em>Facial Beauty Analysis Using the Golden Ratio</em></p>

Phiora is a **Python-based facial analysis app** that evaluates facial aesthetics using the **golden ratio**. It detects key facial landmarks with **OpenCV** and neural networks, computes proportional ratios, and provides a **beauty score from 1 to 10**. Beyond scoring, Phiora offers insights like **face shape analysis** and **personalized hairstyle suggestions**, making it useful for **cosmetic science, AR/VR, digital fashion, and educational tools**.

---
  

<div align="center">

[![GitHub Release](https://img.shields.io/github/v/release/Pratham-Vishwakarma/Phiora?style=flat)](https://github.com/Pratham-Vishwakarma/Phiora/releases/latest)
[![Stars](https://img.shields.io/github/stars/Pratham-Vishwakarma/Phiora)](https://github.com/Pratham-Vishwakarma/Phiora/stargazers)
[![Forks](https://img.shields.io/github/forks/Pratham-Vishwakarma/Phiora)](https://github.com/Pratham-Vishwakarma/Phiora/network/members)
[![License](https://img.shields.io/badge/License-MIT-green)](https://github.com/Pratham-Vishwakarma/Phiora/blob/main/license.txt)
[![Download](https://img.shields.io/badge/Download-Setup-blue)](https://github.com/Pratham-Vishwakarma/Phiora/releases/latest)
[![Report Issue](https://img.shields.io/badge/Report%20Issue-red)](https://github.com/Pratham-Vishwakarma/Phiora/issues)
[![View Code](https://img.shields.io/badge/View%20Code-gray)](https://github.com/Pratham-Vishwakarma/Phiora)

![Python](https://img.shields.io/badge/-Python-437CAC?logo=python&logoColor=white&style=flat)
![OpenCV](https://img.shields.io/badge/-OpenCV-5C3EE8?logo=opencv&logoColor=white&style=flat)
![Mediapipe](https://img.shields.io/badge/-Mediapipe-FF6F61?style=flat)
![Tkinter](https://img.shields.io/badge/-Tkinter-blue?style=flat)

</div>

---

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Features](#features)
- [Installation / Setup](#installation--setup)
- [Usage](#usage)
  - [General User](#general-user)
  - [Developer](#developer)
- [Screenshots / Demo](#screenshots--demo)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Contributing Guidelines](#contributing-guidelines)
- [Roadmap](#roadmap)
- [Built With / Tech Stack](#built-with--tech-stack)
- [Authors / Acknowledgements](#authors--acknowledgements)
- [License](#license)
- [Support / Contact](#support--contact)

---

## Features

✅ **Upload an image** and detect facial landmarks automatically
✅ **Calculate golden ratio-based facial scores**
✅ **Visualize processed images** with highlighted landmarks
✅ **User-friendly GUI** with Tkinter
✅ **Easy installation** and setup

---

## Installation / Setup

**Prerequisites:**

* Python 3.11 or lower
* OpenCV
* Mediapipe
* Pillow (PIL)
* Tkinter
* Pandas

**Steps:**

```bash
# Clone repository
git clone https://github.com/Pratham-Vishwakarma/Phiora.git
cd Phiora

# Install dependencies
pip install -r requirements.txt
```

---

## Usage

### General User

1. Download the [Phiora Setup](https://github.com/Pratham-Vishwakarma/Phiora/releases/download/v1.5.0/Phiora_Setup_v2.0.0.exe).
2. Follow installation instructions.
3. Launch the Phiora application.
4. Click **Upload Image** and select your image.
5. The app detects landmarks, calculates the golden ratio-based score, and displays results.

### Developer

```bash
python main.py
```

* Click **Upload Image** and select an image.
* Facial landmarks and beauty score are calculated and displayed in-app.

---

## Screenshots / Demo

<div align="center">
<img src="https://via.placeholder.com/400x250" alt="Phiora Screenshot 1" />  
<img src="https://via.placeholder.com/400x250" alt="Phiora Screenshot 2" />
</div>  

*(Replace with actual screenshots or GIFs of your app)*

---

## Project Structure

```
/src        -> Source code
/docs       -> Documentation
/tests      -> Unit tests
/main.py    -> Entry point of the application
/requirements.txt -> Dependencies
```

---

## Configuration

* No mandatory config files required.
* Optional: Add custom parameters in `config.py` for advanced usage.

---

## Contributing Guidelines

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-name`).
5. Open a Pull Request.

---

## Roadmap

* [ ] Add **real-time webcam scoring**
* [ ] Support **batch image processing**
* [ ] Improve GUI with **interactive visualizations**
* [ ] Add **additional facial scoring metrics**

---

## Built With / Tech Stack

| Component    | Purpose                   |
| ------------ | ------------------------- |
| Python 3.11  | Core programming language |
| OpenCV       | Image processing          |
| Mediapipe    | Facial landmark detection |
| Pillow (PIL) | Image handling            |
| Tkinter      | GUI                       |
| Pandas       | Data processing           |

---

## Authors / Acknowledgements

* **Pratham Vishwakarma** – Developer & Maintainer
* Thanks to **OpenCV** and **Mediapipe** communities for their contributions.

---

## License

Phiora is licensed under the [MIT License](license.txt).

---

## Support / Contact

* **Email:** [pratham@example.com](mailto:pratham@example.com)
* **GitHub:** [Pratham-Vishwakarma](https://github.com/Pratham-Vishwakarma)
* **LinkedIn:** [Pratham Vishwakarma](https://www.linkedin.com/in/pratham1826/)

---

✅ This version has:

* Aligned badges at the top for quick recognition
* Checkmarks in features for readability
* Placeholder images for demo/screenshots
* Tables for tech stack for clarity
* Bold highlights and clean headings

---

If you want, I can **also design a visually modern “GitHub README header section” with your logo, tagline, badges, and buttons** like professional projects have—it will look very premium.

Do you want me to do that next?
