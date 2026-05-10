# Image Processing Web App

A simple, beginner-friendly web application for basic image processing operations. Upload an image and apply various filters, adjust brightness and contrast, and download the results—all in a clean, single-page interface.

## 🚀 Features

### Core Functionality
- **Image Upload**: Upload JPG, JPEG, or PNG images securely.
- **Real-time Preview**: View original and processed images side-by-side.
- **Download Processed Images**: Save filtered images with descriptive filenames.

### Filters
- **Grayscale**: Convert image to black and white.
- **Edge Detection (Canny)**: Highlight edges using Canny algorithm.
- **Gaussian Blur**: Apply smoothing blur effect.
- **Horizontal Flip**: Mirror the image horizontally.
- **Threshold (Binary)**: Convert to black-and-white using binary thresholding.
- **Sharpen**: Enhance image details with a sharpening kernel.
- **Sepia**: Apply a vintage sepia tone effect.

### Adjustments
- **Brightness & Contrast**: Adjust brightness (-100 to +100) and contrast (0.5 to 2.0) with sliders.
- **Reset**: Revert to the original uploaded image without deleting files.

### Comparison
- **Before/After Toggle**: Switch between original and processed views for easy comparison.

## 🛠️ Tech Stack

- **Backend**: Python with Flask (lightweight web framework)
- **Frontend**: HTML5, CSS3, vanilla JavaScript (no frameworks)
- **Image Processing**: OpenCV (cv2) for all operations
- **Dependencies**: Minimal - Flask, OpenCV, NumPy

## 📁 Project Structure

```
image-filter-app/
│
├── app.py                    # Flask application with routes and image processing logic
├── templates/
│   └── index.html            # Single-page HTML template with UI and JavaScript
├── static/
│   └── style.css             # CSS styles for clean, responsive design
├── uploads/                  # Directory for uploaded images
├── outputs/                  # Directory for processed images
└── README.md                 # This file
```

## 🏃‍♂️ Installation & Setup

### Prerequisites
- Python 3.7+ installed
- pip package manager

### Steps
1. **Clone or Download** the project files to your local machine.

2. **Navigate to the project directory**:
   ```bash
   cd path/to/image-filter-app
   ```

3. **Install dependencies**:
   ```bash
   pip install flask opencv-python numpy
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Open your browser** and go to:
   ```
   http://127.0.0.1:5000/
   ```

## 📖 Usage Guide

### Getting Started
1. Click "Choose an image" to select a JPG, JPEG, or PNG file.
2. Click "Upload Image" to load it into the app.
3. The original image will appear in the left preview pane.

### Applying Filters
1. Choose from the filter buttons (Grayscale, Edge Detection, etc.).
2. The processed image will appear in the right preview pane.
3. Click "Download Processed Image" to save the result.

### Adjusting Brightness & Contrast
1. Use the brightness slider (-100 to +100) and contrast slider (0.5 to 2.0).
2. Click "Apply" to see the changes.
3. The processed image updates in real-time.

### Comparing Images
- Click "Show Original" to toggle between the original and processed views.
- This helps compare before and after effects.

### Resetting
- Click "Reset Image" to return to the original uploaded image.
- All filters and adjustments are cleared, but files remain intact.

## 🔧 API Endpoints

The app uses the following Flask routes:

- `GET /` - Render the main page
- `POST /upload` - Handle image uploads
- `POST /process/<filter_name>` - Apply a filter (grayscale, edge, blur, flip, threshold, sharpen, sepia)
- `POST /adjust` - Apply brightness and contrast adjustments
- `POST /reset` - Reset to original image
- `GET /uploads/<filename>` - Serve uploaded images
- `GET /outputs/<filename>` - Serve processed images

## 🛡️ Error Handling

- Invalid file types are rejected with an error message.
- Actions requiring an uploaded image show alerts if attempted prematurely.
- File reading failures are handled gracefully without crashes.

## 🎨 UI Design

- **Single Page**: No page reloads; all interactions are AJAX-based.
- **Responsive**: Works on desktop and mobile devices.
- **Minimalist**: Clean design with intuitive controls.
- **Accessibility**: Proper labels and keyboard navigation.

## 📝 Code Comments

All code includes beginner-friendly comments explaining:
- Function purposes
- Variable meanings
- Step-by-step logic
- OpenCV operations

## 🚫 Limitations

- No user authentication or multi-user support.
- Images are processed in memory; large files may cause performance issues.
- No database; session data is stored temporarily.
- Designed for educational/demo purposes, not production use.

## 🤝 Contributing

This is a simple demo project. For improvements:
1. Fork the repository.
2. Make changes with clear comments.
3. Test thoroughly.
4. Submit a pull request.

## 📄 License

This project is open-source and available under the MIT License. Feel free to use, modify, and distribute.

## 📞 Support

If you encounter issues:
- Check the browser console for JavaScript errors.
- Ensure all dependencies are installed correctly.
- Verify Python and Flask versions.

Enjoy processing images! 🎉