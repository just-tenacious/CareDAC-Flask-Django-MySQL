@echo off
echo ================================
echo Starting CareDac Project Services
echo ================================

REM ---- Activate Virtual Environment ----
echo Activating virtual environment...
call venv\Scripts\activate

REM ---- Start Website ----
echo Starting WEBSITE App...
start "WEBSITE" cmd /c "python website\app.py"

REM ---- Start Caregiver App ----
echo Starting CAREGIVER App...
start "CAREGIVER" cmd /c "python caregiverApp\caregiver.py"

REM ---- Start Patient App ----
echo Starting PATIENT App...
start "PATIENT" cmd /c "python patientApp\patient.py"

REM ---- Start Admin App ----
echo Starting ADMIN App...
start "ADMIN" cmd /c "python admin\admin.py"

echo ================================
echo All Apps Started Successfully!
echo ================================
pause
