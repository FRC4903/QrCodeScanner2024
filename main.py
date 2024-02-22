import cv2 as cv # pip install opencv-python
import csv
import os

csv_file_path = "Teams/dataTest1.csv"
lastValue = ""
teamNumDisplay = "No Team"
if not os.path.exists("Teams"):
    os.mkdir("Teams")

# Create or open the CSV file
if not os.path.exists(csv_file_path):
    open(csv_file_path, "a").close()
    with open(csv_file_path, "a", newline='') as f:
        w = csv.writer(f)
        w.writerow([
            'team', 'ScouterName', 'MatchNumber', 'UnderStage', 'Broke', 'StartPos', 'Taxi', 'AutoGroundPickup',
            'AutoSourcePickup', 'AutoSpeakerScore', 'AutoAmpScore', 'Defends', 'Defended', 'GroundPickup',
            'SourcePickup', 'ShotsFired', 'ShotsScored', 'ChainFit', 'ScoringAmplifiedSpeaker', 'ScoringUnAmpedSpeaker',
            'ScoringAmp', 'EndgamePark', 'OnstageClimb', 'Harmony', 'Trap', 'SpotLight', 'RP', 'Won', 'Parked',
            'OnStageClimb', 'NoteInTrap', 'autoAmpScore', 'autoSpeakerScore', 'PreLoaded', 'a', 'b', 'c', 'v', 'w', 'x',
            'y', 'z', 'ReliabilityComments', 'AutoComments', 'TeleOpComments'

        ])

# Start the video capture
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()


while True:
    ret, frame = cap.read()

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    detect = cv.QRCodeDetector()
    value, points, straight_qr = detect.detectAndDecode(frame)

    if len(value) > 0 and lastValue != value:
        lastValue = value
        Vl = value.split(",")
        data = Vl
        teamNumDisplay = data[0]

        # Append the data to the CSV file
        with open(csv_file_path, "a", newline='') as f:
            w = csv.writer(f)
            w.writerow(data)

        print("Data has been scanned")
        print(data)


    font = cv.FONT_HERSHEY_SIMPLEX
    fontScale = 1.25
    color = (255, 255, 255)
    frame = cv.flip(frame, 1)

    # Display the titles with adjusted spacing
    # title_display = "4903 Scanner"
    #
    # cv.putText(frame, title_display, (25, 60), font, fontScale, (0, 0, 0), 3, cv.LINE_AA)
    # cv.putText(frame, title_display, (25, 60), font, fontScale, color, 2, cv.LINE_AA)
    cv.putText(frame, teamNumDisplay + " Scanned", (25, 60), font, fontScale, (0, 0, 0), 3, cv.LINE_AA)
    cv.putText(frame, teamNumDisplay + " Scanned", (25, 60), font, fontScale, color, 2, cv.LINE_AA)
    cv.imshow('4903 Scanner', frame)

    if cv.waitKey(1) == ord('q'):
        break
cap.release()
cv.destroyAllWindows()


