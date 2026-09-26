from ultralytics import YOLO
import cv2

# Load YOLO model
model = YOLO("yolo11n.pt")

# Open laptop webcam
cap = cv2.VideoCapture(0)

while True:
    people_count = 0

    # Capture a frame
    success, frame = cap.read()

    if not success:
        print("Could not access the camera.")
        break

    # Detect and track objects
    results = model.track(frame, persist=True)

    # Count people
    if results[0].boxes.id is not None:
        track_ids = results[0].boxes.id.int().cpu().tolist()
        class_ids = results[0].boxes.cls.int().cpu().tolist()

        for class_id in class_ids:
            if class_id == 0:
                people_count += 1

        print("Tracking IDs:", track_ids)

    # Draw detection boxes and tracking IDs
    annotated_frame = results[0].plot()

    # Display customer count
    cv2.putText(
        annotated_frame,
        f"Customers: {people_count}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    # Show live video
    cv2.imshow("Smart Retail - Live Detection", annotated_frame)

    # Press Q to stop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Close everything
cap.release()
cv2.destroyAllWindows()