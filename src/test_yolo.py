from ultralytics import YOLO

# Load a pre-trained YOLO model
MODEL = YOLO("yolo11n.pt")

# Run object detection on a sample image
results = MODEL("bus.jpg", save=True, project="outputs", name="detection")

# Display the detection results
for result in results: 
    result.show() 
    