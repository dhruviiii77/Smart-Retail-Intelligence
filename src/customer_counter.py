import csv
import os
from datetime import datetime

# CSV file for customer data
csv_file = "customer_data.csv"

# Create CSV file with headers if it doesnt exist
if not os.path.exists(csv_file):
    with open(csv_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Event", "Entered", "Exited", "Customers Inside"])

from ultralytics import YOLO 
import cv2

# Load YOLO model
model = YOLO("yolo11n.pt")

# Open Webcam
cap = cv2.VideoCapture(0)

entered = set()
exited = set()

previous_positions = {}
last_entered_count = 0
last_exited_count = 0

while True:

    success, frame = cap.read()

    if not success:
        print("Could not access the camera.")
        break

    # Resize frame
    frame = cv2.resize(frame, (1000, 700))

    # Run YOLO tracking
    results = model.track(frame, persist=True, classes=[0])

    # Create annotated frame
    annotated_frame = results[0].plot()

    # Virtual counting line
    line_y = 350

    cv2.line(
        annotated_frame,
        (0, line_y),
        (1000, line_y),
        (255, 0, 0),
        3
    )

    # Count people
    if results[0].boxes.id is not None:

        boxes = results[0].boxes.xyxy.cpu().tolist()
        track_ids = results[0].boxes.id.int().cpu().tolist()

        for box, track_id in zip(boxes, track_ids):

            x1, y1, x2, y2 = box

            centre_y = int((y1 + y2)/2)

            # Previous position of the person
            previous_y =  previous_positions.get(track_id, centre_y)

            # Detect line crossing

            if previous_y is not None:

                # Moving DOWN across the line = ENTERED
                if previous_y < line_y and centre_y >= line_y:
                    if track_id not in exited:
                        entered.add(track_id)

                # Moving UP across the line = EXITED
                elif previous_y > line_y and centre_y <= line_y:
                    if track_id not in entered:
                        exited.add(track_id)
                  
            # Store current position
            previous_positions[track_id] = centre_y

    # Display counts
    cv2.putText(
        annotated_frame,
        f"Entered: {len(entered)}",
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.putText(
        annotated_frame,
        f"Exited: {len(exited)}",
        (20, 95),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 255),
        2
    )

    cv2.putText(
        annotated_frame,
        "Press Q to Quit",
        (20, 140),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

         # Check if a new customer entered or exited
    if len(entered) != last_entered_count or len(exited) != last_exited_count:
        if len(entered) > last_entered_count:
            event = "Entered"
        else:
            event = "Exited"

        print(f"Customer {event}")
                
        # Save customer data
        with open(csv_file, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                len(entered),
                len(exited),
                max(0, len(entered) - len(exited))
            ])

        last_entered_count = len(entered)
        last_exited_count = len(exited) 

    # Show camera    
    cv2.imshow(
        "Smart Retail - Customer Counter",
        annotated_frame
    )

    # Stop with Q 
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release camera
cap.release()
cv2.destroyAllWindows() 