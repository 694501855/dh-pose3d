import launch

if not launch.is_installed("cvzone"):
    launch.run_pip("install cvzone==1.5.5", "requirements for MagicPrompt")