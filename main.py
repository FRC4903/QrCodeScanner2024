import cv2 as cv  # pip install opencv-python
import csv
import os
import openpyxl

# pyinstaller --onefile --icon=icon.ico main.py
csv_file_path = "Teams/RawData.csv"
xlsx_flie_path = "Teams/Match_Prediction_Sheet.xlsx"
# import openpyxl as xl
# wb = openpyxl.Workbook()
# ws = wb.active
# mylist = ['dog', 'cat', 'fish', 'bird']
# ws.append(mylist)
# wb.save('myFile.xlsx')
# wb.close()

wb = openpyxl.load_workbook("Teams/Match_Prediction_Sheet.xlsx")
# Get the current Active Sheet
wb.active = wb['Raw Data']
ws = wb.active

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
            'team', 'ScouterName', 'MatchNumber', 'UnderStage', 'Broke',
            'autoAmpScore', 'autoSpeakerScore', 'StartPos', 'Taxi', 'AutoGroundPickup', 'AutoSourcePickup',
            'AutoSpeakerScore', 'AutoAmpScore',
            'Defended', 'DefenseScale', 'GroundPickup', 'SourcePickup', 'ChainFit',
            'SpeakerMisses', 'AmpMisses', 'ScoringAmplifiedSpeaker', 'ScoringUnAmpedSpeaker', 'ScoringAmp',
            'EndgamePark', 'OnstageClimb',
            'Harmony', 'Trap', 'SpotLight', 'RP', 'Won', 'Parked', 'OnStageClimb', 'NoteInTrap',
            'a', 'b', 'c', 'v', 'w', 'x', 'y', 'z',
            'ReliabilityComments', 'AutoComments', 'TeleOpComments'

        ])

# Start the video capture
cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()
    frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

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
        while len(data[2]) < 2:
            data[2] = '0' + data[2]
        # Append the data to the CSV file
        ws.append(data)
        wb.save('Teams/Match_Prediction_Sheet.xlsx')
        wb.close()
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
    # title_display = "4903 Scanner"    #
    # cv.putText(frame, title_display, (25, 60), font, fontScale, (0, 0, 0), 3, cv.LINE_AA)
    # cv.putText(frame, title_display, (25, 60), font, fontScale, color, 2, cv.LINE_AA)
    cv.putText(frame, teamNumDisplay + " Scanned", (25, 60), font, fontScale, (0, 0, 0), 3, cv.LINE_AA)
    cv.putText(frame, teamNumDisplay + " Scanned", (25, 60), font, fontScale, color, 2, cv.LINE_AA)
    cv.imshow('4903 Scanner', frame)

    if cv.waitKey(1) == ord('q'):
        break
cap.release()
cv.destroyAllWindows()
