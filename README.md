# ID-Guard: Identity Verification API 🛡️

A Dockerized Microservice for automated KYC (Know Your Customer) verification. It processes images of California Driver's Licenses and extracts the ID number using Computer Vision.

**Live API:** [https://id-guard-api.onrender.com/api/verify/](https://id-guard-api.onrender.com/api/verify/)

## 🚀 Tech Stack
- **Backend:** Python 3.10, Django Rest Framework (DRF)
- **Computer Vision:** OpenCV (Headless), Tesseract OCR
- **Infrastructure:** Docker, Docker Compose, Render (Cloud)
- **Database:** PostgreSQL

## 🛠️ The Architecture
The system uses a 3-stage pipeline to handle noisy real-world images:
1.  **Preprocessing:** Applies Bilateral Filtering (to remove holograms) and Adaptive Thresholding.
2.  **OCR Extraction:** Uses Tesseract with a custom configuration (`--psm 6`) optimized for block text.
3.  **Pattern Matching:** Validates output against the Strict California Schema (`1 Letter + 7 Digits`) and applies "Self-Healing" logic to fix common character confusions (e.g., repairing '8' to 'B').

## ⚡ Quick Start (Test via Curl)
You can test the live API directly from your terminal:

```bash
curl -X POST -F "image=@your_test_image.jpg" https://id-guard-api.onrender.com/api/verify/
