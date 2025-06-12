Color Analyzer 🎨
A web-based tool that analyzes images to extract dominant colors, provides color palette insights, and suggests design improvements. Built with Flask backend and vanilla JavaScript frontend.


Features
Image Upload: Drag-and-drop or click-to-upload interface
Color Extraction: Extract dominant colors from any image
Color Palette Analysis: Get comprehensive color palette breakdowns
Design Suggestions: Receive complementary and analogous color recommendations
Contrast Analysis: Evaluate color contrast ratios for accessibility
Real-time Preview: See color analysis results instantly
Tech Stack
Backend: Flask (Python)
Frontend: HTML5, CSS3, Vanilla JavaScript
Image Processing: PIL (Pillow), ColorThief
Color Analysis: NumPy, scikit-learn, webcolors
File Handling: Werkzeug
Installation
Prerequisites
Python 3.8 or higher
pip package manager
Setup
Clone the repository
bash
git clone https://github.com/yourusername/color-analyzer.git
cd color-analyzer
Create a virtual environment
bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies
bash
pip install -r requirements.txt
Create upload directory
bash
mkdir -p static/uploads
Run the application
bash
python app.py
Open your browser Navigate to http://127.0.0.1:5000
Usage
Upload an Image:
Drag and drop an image file into the upload zone
Or click the upload zone to select a file
Supported formats: PNG, JPG, JPEG, GIF
Analyze Colors:
Click the "Analyze Colors" button
Wait for the analysis to complete
View Results:
See dominant color palette
Review brightness and saturation metrics
Get design improvement suggestions
API Endpoints
POST /analyze
Analyzes an uploaded image and returns color data.

Request:

Method: POST
Content-Type: multipart/form-data
Body: image file
Response:

json
{
  "dominant_palette": ["#ff5733", "#33ff57", "#3357ff"],
  "palette_improvements": [
    {
      "type": "Complementary",
      "colors": ["#ff5733", "#33ff57"],
      "description": "Consider using this complementary color for accent elements"
    }
  ],
  "font_suggestions": [...]
}
Project Structure
color-analyzer/
├── app.py                 # Flask application main file
├── color_analyzer.py      # Color analysis logic
├── requirements.txt       # Python dependencies
├── static/
│   └── uploads/          # Image upload directory
├── templates/
│   └── index.html        # Frontend interface
└── README.md            # Project documentation
Contributing
Fork the repository
Create a feature branch (git checkout -b feature/amazing-feature)
Commit your changes (git commit -m 'Add some amazing feature')
Push to the branch (git push origin feature/amazing-feature)
Open a Pull Request
Development
Adding New Features
The project is structured to be easily extensible:

Color Analysis: Extend ImageColorAnalyzer class in color_analyzer.py
API Endpoints: Add new routes in app.py
Frontend: Modify index.html for UI changes
Testing
To test the application:

Start the Flask development server
Upload various image formats
Verify color analysis results
Check error handling with invalid files
Configuration
Upload Directory: static/uploads (configurable in app.py)
Max File Size: 16MB (configurable in app.py)
Allowed Extensions: PNG, JPG, JPEG, GIF
Troubleshooting
Common Issues
Import Errors: Make sure all dependencies are installed
bash
pip install -r requirements.txt
Upload Directory Missing: Create the uploads directory
bash
mkdir -p static/uploads
Port Already in Use: Change the port in app.py or kill the process using port 5000
Image Processing Errors: Ensure uploaded files are valid image formats
License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
ColorThief for color extraction
Flask for the web framework
Pillow for image processing
Future Enhancements
 Support for more image formats
 Color harmony analysis
 Export color palettes
 Color accessibility scoring
 Batch image processing
 Mobile app version
Made with ❤️ by Xyden

