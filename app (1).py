
import cv2
import torch
from flask import Flask, Response, jsonify, render_template
from flask_cors import CORS
from threading import Thread
import time
import queue

app = Flask(__name__)
CORS(app)

# Load YOLOv5 model (ensure you're using the correct model for your use case)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Shared state for traffic management
traffic_data = {
    "road1": {"time": 30, "vehicle_count": 0, "signal": "green"},
    "road2": {"time": 30, "vehicle_count": 0, "signal": "red"}
}

# Global video capture objects
road1_video = cv2.VideoCapture("roads.mp4")
road2_video = cv2.VideoCapture("roads.mp4")

# Video frame queues to store frames for streaming
frame_queue_road1 = queue.Queue(maxsize=10)
frame_queue_road2 = queue.Queue(maxsize=10)

# Function to detect vehicles using YOLOv5
def detect_vehicles(frame):
    results = model(frame)  # Detect vehicles using YOLOv5
    detections = results.xyxy[0]  # Get detection results
    count = 0

    for det in detections:
        if int(det[5]) in [2, 3, 5, 7]:  # Vehicle classes: car, motorcycle, bus, truck
            count += 1
            x1, y1, x2, y2 = map(int, det[:4])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"Vehicle", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return count, frame



##########################################

# Function to manage traffic signals
def manage_traffic():
    global traffic_data

    while True:
        road1 = traffic_data["road1"]
        road2 = traffic_data["road2"]

        # Prioritize roads with vehicle count >= 10
        if road1["vehicle_count"] >= 10 and road1["signal"] == "red":
            road1["signal"] = "green"
            road1["time"] = 30
            road2["signal"] = "red"
            road2["time"] = 0
            time.sleep(30)  # Hold green for road1 for 30 seconds
            continue

        if road2["vehicle_count"] >= 10 and road2["signal"] == "red":
            road2["signal"] = "green"
            road2["time"] = 30
            road1["signal"] = "red"
            road1["time"] = 0
            time.sleep(30)  # Hold green for road2 for 30 seconds
            continue

        # Default signal switching logic
        if road1["signal"] == "green":
            road1["time"] -= 1
            if road1["time"] <= 0:
                road1["signal"] = "red"
                road1["time"] = 30
                road2["signal"] = "green"
        elif road2["signal"] == "green":
            road2["time"] -= 1
            if road2["time"] <= 0:
                road2["signal"] = "red"
                road2["time"] = 30
                road1["signal"] = "green"

        time.sleep(1)



# Function to process video frames and update vehicle counts
def process_videos():
    global traffic_data
    while True:
        # Read frames from both roads
        ret1, frame1 = road1_video.read()
        ret2, frame2 = road2_video.read()

        if not ret1:
            road1_video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        if not ret2:
            road2_video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        # Process frames and count vehicles using YOLOv5
        traffic_data["road1"]["vehicle_count"], _ = detect_vehicles(frame1)
        traffic_data["road2"]["vehicle_count"], _ = detect_vehicles(frame2)

        # Add processed frames to queues for streaming
        if not frame_queue_road1.full():
            frame_queue_road1.put(frame1)
        if not frame_queue_road2.full():
            frame_queue_road2.put(frame2)

# Stream video for a road
def generate_video(video_capture, road, frame_queue):
    last_frame = None  # Store the last processed frame
    red_signal_start_time = None  # Track the time when the red signal started

    while True:
        # Check the signal status
        signal = traffic_data[road]["signal"].upper()

        if signal == "RED":
            # If the signal just turned red, record the current time
            if red_signal_start_time is None:
                red_signal_start_time = time.time()

            # Calculate elapsed time since the signal turned red
            elapsed_time = time.time() - red_signal_start_time

            # Pause the video feed if the signal is red for less than 30 seconds
            if elapsed_time < 30:
                if last_frame is not None:
                    frame = last_frame.copy()
                else:
                    # If no frame exists yet, wait until one is available
                    time.sleep(0.1)
                    continue
            else:
                # Reset the timer when the red signal ends
                red_signal_start_time = None
        else:
            # Fetch the next frame from the queue if the signal is green
            red_signal_start_time = None
            frame = frame_queue.get()
            last_frame = frame.copy()  # Update the last frame

        # Add signal and timer display on video
        timer = traffic_data[road]["time"]
        cv2.putText(frame, f"Signal: {signal}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, 
                    (0, 255, 0) if signal == "GREEN" else (0, 0, 255), 2)
        cv2.putText(frame, f"Timer: {timer}s", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Encode the frame as a JPEG image
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        # Yield the frame in the appropriate format for video streaming
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


# Routes to stream videos
@app.route('/video_feed/road1')
def video_feed_road1():
    return Response(generate_video(road1_video, "road1", frame_queue_road1),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed/road2')
def video_feed_road2():
    return Response(generate_video(road2_video, "road2", frame_queue_road2),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# API to get traffic data
@app.route('/traffic_data', methods=['GET'])
def get_traffic_data():
    return jsonify(traffic_data)

# Main route
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    # Start the video processing thread
    video_thread = Thread(target=process_videos)
    video_thread.daemon = True
    video_thread.start()

    # Start the traffic management thread
    traffic_thread = Thread(target=manage_traffic)
    traffic_thread.daemon = True
    traffic_thread.start()

    app.run(debug=True, threaded=True)

    