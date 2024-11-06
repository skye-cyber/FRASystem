# FRASystem (``Face Recognition Attendance System``)

This project is a Face Recognition Attendance System built using Django for the backend and OpenCV and face-recognition libraries for facial matching. The system captures video frames from a webcam, processes each frame to detect and recognize faces, and marks attendance if a match is found. This solution is ideal for tracking attendance in environments like offices, classrooms, and other restricted access areas.

## Features

- Real-time face detection and recognition using OpenCV.
- Automatic attendance marking and logging in the database.
- CSRF-protected endpoints for secure frame data submission.
- Easy setup with a web-based interface for live camera streaming.

## Technologies Used

- **Backend**: Django
- **Frontend**: HTML, JavaScript, Tailwindcss
- **Libraries**: OpenCV, face-recognition, Numpy
- **Database**: SQLite (default, can be configured for other databases)

## Prerequisites

- ```Python 3.8>>```
- ```Django```
- ```OpenCV``` (`cv2`)
- ```openpyxl```
- ```pandas```
- ```playsound```
- ```pickle```
- ```face-recognition``` library
- ```Numpy```

To install dependencies, you can use the following:
```bash
pip install django opencv-python face-recognition numpy pandas openpyxl playsound pickle
```

## Project Structure
- `DetectionAlgorithms` - Encapsulates recognision algorithms attendance handlers
- `middleware` - Implements Ratelimit and other security measures
- `migrations` - Encapsulates database handling for clockins and account management
- `static/` - Static files (CSS, JavaScript)
- `templates/` - HTML templates for web interface
- `media` - Temporary store of enrollment data during enrollment phrase, also stores csv & xlsx regisry for clockin details
- `manage.py` - Django management script

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/skye-cyber/FRASystem.git
   cd FRASystem
   ```

2. **Set up Django**:
   Initialize the database and run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Prepare Face Encodings**:
   - Store face encodings of authorized individuals by running an initial script or manually adding to the `encodings.pickle` file in the project.
   - Use the `face_recognition` library to generate encodings from a dataset of images of authorized individuals.

4. **Run the Server**:
   Start the Django development server:
   ```bash
   python manage.py runserver
   ```

5. **Access the Web Interface**:
   Open a browser and navigate to `http://127.0.0.1:8000/` to access the attendance system.

## Interface

1. **Login & Signup page**
   You must Register your account inorder to access the site

2. **Home page**
   This is the welcome page for the project, under the navigation menu you access your profile, Enroll to attendance system
   
4. **Profile**
   A display of the user details, including Enrollment status
   From the menu you can access:
     `Clockin Page` inorder to clockin
     `Delete Account` beware this is permanent
     `Uenroll from the clockin system` your account will still be available but you have no acess to clockin, this will delete your previous clockin data
## Usage
1. **Enrolling**
   Upon loading the page, the camera starts automatically (you may need to grant permissions).
   Atmost 3 snaps are taken and encoded for recognision.
   Your photos are nolonger stored after encoding they are deleted permanently.
   
2. **Clocking in**:
   Upon loading the page, the camera starts automatically (you may need to grant permissions).
   The camera captures frames, and each frame is processed to detect faces. If a recognized face is detected, attendance is marked and logged in the system.

3. **View Attendance Logs**:
   Attendance records are stored in the database and can be accessed through the Django admin panel or an additional route for attendance logs.

## API Endpoints

- **/process_frames/** - Receives frames from the client for face processing and returns the result.
- **/mark_attendance/** - Processes and logs attendance data upon successful face recognition.

## Example Code Snippets

### JavaScript (Frontend)
The following snippet captures frames and sends them to the Django server:

```javascript
async function sendFrameToDjango(frameData) {
    const csrftoken = getCookie('csrftoken');  // Implement getCookie function to retrieve the CSRF token
    await fetch('/process_frames/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken
        },
        body: 'frame=' + encodeURIComponent(frameData)
    });
}
```

### Django View (Backend)
This view processes incoming frames and matches them with stored face encodings:

```python
@csrf_exempt
def process_frames(request):
    if request.method == 'POST':
        frame_data = request.POST.get('frame', '')
        # Process frame data and perform face recognition
        return JsonResponse({'status': 'success'})
    return JsonResponse({'error': 'Invalid request'}, status=400)
```

## Troubleshooting

- **CSRF Token Missing**: Ensure the CSRF token is correctly passed in each POST request. Implement `getCookie` to retrieve CSRF tokens from cookies.
- **Camera Access Issues**: Check browser permissions for camera access and ensure secure context (HTTPS) if using on a server.

## Future Enhancements

- Implement role-based access for different user types.
- Add support for multiple cameras.
- Enable reporting and analytics for attendance data.

## License

This project is licensed under the MIT License.
