# import cv2
# import time
# from flask import Flask, Response, jsonify, render_template
# from threading import Thread

# app = Flask(__name__)

# # Shared data structure for signal timers and vehicle counts
# timer_data = {"road1": 60, "road2": 60}
# vehicle_counts = {"road1": 0, "road2": 0}

# # Global video capture objects
# road1_video = cv2.VideoCapture("road1.mp4")
# road2_video = cv2.VideoCapture("road2.mp4")

# # Function to count vehicles
# def count_vehicles(video_capture):
#     background_subtractor = cv2.createBackgroundSubtractorMOG2()
#     vehicle_count = 0

#     ret, frame = video_capture.read()
#     if not ret:
#         return vehicle_count, None

#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     mask = background_subtractor.apply(gray)
#     _, mask = cv2.threshold(mask, 244, 255, cv2.THRESH_BINARY)

#     contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#     for contour in contours:
#         if cv2.contourArea(contour) > 500:
#             vehicle_count += 1

#     return vehicle_count, frame

# # Function to process videos and update counts
# def process_videos():
#     global vehicle_counts
#     while True:
#         # Count vehicles for road1
#         vehicle_counts["road1"], _ = count_vehicles(road1_video)
#         # Count vehicles for road2
#         vehicle_counts["road2"], _ = count_vehicles(road2_video)

#         time.sleep(1)

# # Stream video for a road
# def generate_video(video_capture, road):
#     while True:
#         vehicle_count, frame = count_vehicles(video_capture)
#         vehicle_counts[road] = vehicle_count

#         # Encode the frame as JPEG
#         _, buffer = cv2.imencode('.jpg', frame)
#         frame_bytes = buffer.tobytes()

#         # Stream the video frame
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# # Routes to stream videos
# @app.route('/video_feed/road1')
# def video_feed_road1():
#     return Response(generate_video(road1_video, "road1"), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/video_feed/road2')
# def video_feed_road2():
#     return Response(generate_video(road2_video, "road2"), mimetype='multipart/x-mixed-replace; boundary=frame')

# # API to get vehicle counts
# @app.route('/vehicle_counts', methods=['GET'])
# def get_vehicle_counts():
#     return jsonify(vehicle_counts)

# # Main route
# @app.route('/')
# def index():
#     return render_template('index.html')

# if __name__ == "__main__":
#     video_thread = Thread(target=process_videos)
#     video_thread.daemon = True
#     video_thread.start()
#     app.run(debug=True)

#############################################################@second



# import cv2
# import torch
# from flask import Flask, Response, jsonify, render_template
# from flask_cors import CORS
# from threading import Thread

# app = Flask(__name__)
# CORS(app)

# # Load YOLOv5 model
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# # Shared data structure for vehicle counts
# vehicle_counts = {"road1": 0, "road2": 0}

# # Global video capture objects
# road1_video = cv2.VideoCapture("road1.mp4")
# road2_video = cv2.VideoCapture("road2.mp4")

# # Function to detect vehicles using YOLOv5
# def detect_vehicles(frame):
#     results = model(frame)
#     detections = results.xyxy[0]  # Get detection results
#     count = 0

#     for det in detections:
#         # Detection format: [x1, y1, x2, y2, confidence, class]
#         if int(det[5]) in [2, 3, 5, 7]:  # Vehicle classes: car, motorcycle, bus, truck
#             count += 1
#             x1, y1, x2, y2 = map(int, det[:4])
#             cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#             cv2.putText(frame, f"Vehicle", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

#     return count, frame

# # Function to process video and update counts
# def process_videos():
#     global vehicle_counts
#     while True:
#         ret1, frame1 = road1_video.read()
#         ret2, frame2 = road2_video.read()

#         if not ret1:
#             road1_video.set(cv2.CAP_PROP_POS_FRAMES, 0)
#             continue
#         if not ret2:
#             road2_video.set(cv2.CAP_PROP_POS_FRAMES, 0)
#             continue

#         # Detect vehicles in each road
#         vehicle_counts["road1"], _ = detect_vehicles(frame1)
#         vehicle_counts["road2"], _ = detect_vehicles(frame2)

# # Stream video for a road
# def generate_video(video_capture, road):
#     while True:
#         ret, frame = video_capture.read()
#         if not ret:
#             video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
#             continue

#         vehicle_count, frame = detect_vehicles(frame)
#         vehicle_counts[road] = vehicle_count

#         _, buffer = cv2.imencode('.jpg', frame)
#         frame_bytes = buffer.tobytes()

#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# # Routes to stream videos
# @app.route('/video_feed/road1')
# def video_feed_road1():
#     return Response(generate_video(road1_video, "road1"), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/video_feed/road2')
# def video_feed_road2():
#     return Response(generate_video(road2_video, "road2"), mimetype='multipart/x-mixed-replace; boundary=frame')

# # API to get vehicle counts
# @app.route('/vehicle_counts', methods=['GET'])
# def get_vehicle_counts():
#     return jsonify(vehicle_counts)

# # Main route
# @app.route('/')
# def index():
#     return render_template('index.html')

# if __name__ == "__main__":
#     video_thread = Thread(target=process_videos)
#     video_thread.daemon = True
#     video_thread.start()
#     app.run(debug=True)
###################################################################################Third


# import cv2
# import torch
# from flask import Flask, Response, jsonify, render_template
# from flask_cors import CORS
# from threading import Thread
# import time

# app = Flask(__name__)
# CORS(app)

# # Load YOLOv5 model
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# # Shared state for traffic management
# traffic_data = {
#     "road1": {"time": 30, "vehicle_count": 0, "signal": "green"},
#     "road2": {"time": 30, "vehicle_count": 0, "signal": "red"}
# }

# # Global video capture objects
# road1_video = cv2.VideoCapture("road1.mp4")
# road2_video = cv2.VideoCapture("road2.mp4")

# # Function to detect vehicles using YOLOv5
# def detect_vehicles(frame):
#     results = model(frame)
#     detections = results.xyxy[0]  # Get detection results
#     count = 0

#     for det in detections:
#         # Detection format: [x1, y1, x2, y2, confidence, class]
#         if int(det[5]) in [2, 3, 5, 7]:  # Vehicle classes: car, motorcycle, bus, truck
#             count += 1
#             x1, y1, x2, y2 = map(int, det[:4])
#             cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#             cv2.putText(frame, f"Vehicle", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

#     return count, frame

# # Function to manage traffic signals
# def manage_traffic():
#     global traffic_data

#     while True:
#         road1 = traffic_data["road1"]
#         road2 = traffic_data["road2"]

#         if road1["signal"] == "green":
#             road1["time"] -= 1
#             if road1["vehicle_count"] > 20:
#                 road1["time"] -= 5  # Reduce additional time for heavy traffic
#             if road1["time"] <= 0:
#                 road1["time"] = 30
#                 road1["signal"] = "red"
#                 road2["signal"] = "green"
#         elif road2["signal"] == "green":
#             road2["time"] -= 1
#             if road2["vehicle_count"] > 20:
#                 road2["time"] -= 5  # Reduce additional time for heavy traffic
#             if road2["time"] <= 0:
#                 road2["time"] = 30
#                 road2["signal"] = "red"
#                 road1["signal"] = "green"

#         time.sleep(1)

# # Function to process video feeds and update vehicle counts
# def process_videos():
#     global traffic_data
#     while True:
#         ret1, frame1 = road1_video.read()
#         ret2, frame2 = road2_video.read()

#         if not ret1:
#             road1_video.set(cv2.CAP_PROP_POS_FRAMES, 0)
#             continue
#         if not ret2:
#             road2_video.set(cv2.CAP_PROP_POS_FRAMES, 0)
#             continue

#         traffic_data["road1"]["vehicle_count"], _ = detect_vehicles(frame1)
#         traffic_data["road2"]["vehicle_count"], _ = detect_vehicles(frame2)

# # Stream video for a road
# def generate_video(video_capture, road):
#     while True:
#         ret, frame = video_capture.read()
#         if not ret:
#             video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
#             continue

#         vehicle_count, frame = detect_vehicles(frame)
#         traffic_data[road]["vehicle_count"] = vehicle_count

#         # Add signal and timer display on video
#         signal = traffic_data[road]["signal"].upper()
#         timer = traffic_data[road]["time"]
#         cv2.putText(frame, f"Signal: {signal}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) if signal == "GREEN" else (0, 0, 255), 2)
#         cv2.putText(frame, f"Timer: {timer}s", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

#         _, buffer = cv2.imencode('.jpg', frame)
#         frame_bytes = buffer.tobytes()

#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# # Routes to stream videos
# @app.route('/video_feed/road1')
# def video_feed_road1():
#     return Response(generate_video(road1_video, "road1"), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/video_feed/road2')
# def video_feed_road2():
#     return Response(generate_video(road2_video, "road2"), mimetype='multipart/x-mixed-replace; boundary=frame')

# # API to get traffic data
# @app.route('/traffic_data', methods=['GET'])
# def get_traffic_data():
#     return jsonify(traffic_data)

# # Main route
# @app.route('/')
# def index():
#     return render_template('index.html')

# if __name__ == "__main__":
#     video_thread = Thread(target=process_videos)
#     video_thread.daemon = True
#     video_thread.start()

#     traffic_thread = Thread(target=manage_traffic)
#     traffic_thread.daemon = True
#     traffic_thread.start()

#     app.run(debug=True)



##########################################################################fourth






# from flask import Flask, render_template, Response, jsonify
# import cv2
# import threading
# import time

# app = Flask(__name__)

# # Global variables for video capture and data sharing
# road1_video = cv2.VideoCapture("road1.mp4")
# road2_video = cv2.VideoCapture("road2.mp4")

# frame_road1 = None
# frame_road2 = None
# vehicle_count_road1 = 0
# vehicle_count_road2 = 0
# timer_data = {"road1": 60, "road2": 60}
# signal_status = {"road1": "green", "road2": "red"}
# lock = threading.Lock()


# def count_vehicles(frame):
#     """Dummy vehicle counting function."""
#     # Add your ML model here
#     return 10  # Replace with actual detection logic


# def process_videos():
#     global frame_road1, frame_road2, vehicle_count_road1, vehicle_count_road2, timer_data, signal_status

#     while True:
#         # Read frames from the videos
#         ret1, frame1 = road1_video.read()
#         ret2, frame2 = road2_video.read()

#         if not ret1 or not ret2:
#             break

#         # Vehicle counting logic (simplified for every nth frame)
#         vehicle_count_road1 = count_vehicles(frame1)
#         vehicle_count_road2 = count_vehicles(frame2)

#         # Update timers and signal status
#         with lock:
#             if timer_data["road1"] > 0:
#                 signal_status["road1"] = "green"
#                 signal_status["road2"] = "red"
#                 timer_data["road1"] -= 1
#             else:
#                 signal_status["road1"] = "red"
#                 signal_status["road2"] = "green"
#                 timer_data["road2"] -= 1

#             # Reset timers after they reach 0
#             if timer_data["road1"] <= 0 and timer_data["road2"] <= 0:
#                 timer_data["road1"] = 60
#                 timer_data["road2"] = 60

#         # Update shared frame variables
#         with lock:
#             frame_road1 = frame1
#             frame_road2 = frame2

#         time.sleep(0.03)  # Add a small delay to simulate real-time processing


# def generate_frames(video_source):
#     """Video streaming generator function."""
#     while True:
#         with lock:
#             frame = frame_road1 if video_source == "road1" else frame_road2
#             if frame is None:
#                 continue
#             _, buffer = cv2.imencode('.jpg', frame)
#             frame_data = buffer.tobytes()

#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')


# @app.route('/video_feed/<string:road>')
# def video_feed(road):
#     return Response(generate_frames(road), mimetype='multipart/x-mixed-replace; boundary=frame')


# @app.route('/traffic_data')
# def traffic_data():
#     """Endpoint to get the current traffic status."""
#     with lock:
#         return jsonify({
#             "road1": {
#                 "vehicle_count": vehicle_count_road1,
#                 "time": timer_data["road1"],
#                 "signal": signal_status["road1"]
#             },
#             "road2": {
#                 "vehicle_count": vehicle_count_road2,
#                 "time": timer_data["road2"],
#                 "signal": signal_status["road2"]
#             }
#         })


# if __name__ == '__main__':
#     # Start the video processing thread
#     video_thread = threading.Thread(target=process_videos)
#     video_thread.daemon = True
#     video_thread.start()

#     # Run Flask app
#     app.run(debug=True)



######################################################################################fifth



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
road1_video = cv2.VideoCapture("road1.mp4")
road2_video = cv2.VideoCapture("road1.mp4")

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

# Function to manage traffic signals
def manage_traffic():
    global traffic_data

    while True:
        road1 = traffic_data["road1"]
        road2 = traffic_data["road2"]

        if road1["signal"] == "green":
            road1["time"] -= 1
            if road1["vehicle_count"] > 20:
                road1["time"] -= 5  # Reduce additional time for heavy traffic
            if road1["time"] <= 0:
                road1["time"] = 30
                road1["signal"] = "red"
                road2["signal"] = "green"
        elif road2["signal"] == "green":
            road2["time"] -= 1
            if road2["vehicle_count"] > 20:
                road2["time"] -= 5  # Reduce additional time for heavy traffic
            if road2["time"] <= 0:
                road2["time"] = 30
                road2["signal"] = "red"
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
    while True:
        # Fetch the next frame from the queue (waiting if necessary)
        frame = frame_queue.get()

        # Add signal and timer display on video
        signal = traffic_data[road]["signal"].upper()
        timer = traffic_data[road]["time"]
        cv2.putText(frame, f"Signal: {signal}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) if signal == "GREEN" else (0, 0, 255), 2)
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

