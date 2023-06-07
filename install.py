import launch


if not launch.is_installed("cvzone"):
    launch.run_pip("install cvzone==1.5.6", "requirements for MagicPrompt")
if not launch.is_installed("mediapipe"):
    launch.run_pip("install mediapipe", "requirements for MagicPrompt")