#!/bin/bash

echo "================================================"
echo "          Satellite Vision Launcher"
echo "================================================"
echo

show_menu() {
    echo "Choose an option:"
    echo "1. Setup Environment (First time setup)"
    echo "2. Run Basic Satellite Processing"
    echo "3. Run Full AI Analysis"
    echo "4. Install Requirements Only"
    echo "5. Exit"
    echo
}

while true; do
    show_menu
    read -p "Enter your choice (1-5): " choice
    
    case $choice in
        1)
            echo
            echo "Running setup..."
            python3 setup.py
            echo
            read -p "Press Enter to continue..."
            ;;
        2)
            echo
            echo "Starting basic satellite processing..."
            python3 main_fixed.py
            echo
            read -p "Press Enter to continue..."
            ;;
        3)
            echo
            echo "Starting full AI analysis..."
            python3 main_complete_fixed.py
            echo
            read -p "Press Enter to continue..."
            ;;
        4)
            echo
            echo "Installing requirements..."
            pip3 install -r requirements.txt
            echo
            read -p "Press Enter to continue..."
            ;;
        5)
            echo
            echo "Thank you for using Satellite Vision!"
            exit 0
            ;;
        *)
            echo "Invalid choice. Please try again."
            echo
            ;;
    esac
done