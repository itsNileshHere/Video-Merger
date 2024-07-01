#!/bin/bash

while true; do
    clear
    echo "Select Python script to run:"
    echo "1. Video_Merge.py"
    echo "2. Video_Format.py"
    echo "3. Exit"
    echo
    echo "** No Compression will be performed in any of the scripts."
    echo "** Video_Format.py only converts .ts video file to any format."
    echo

    read -p "Enter your choice: " choice

    case $choice in
        1)
            python3 Video_Merge.py
            ;;
        2)
            python3 Video_Format.py
            ;;
        3)
            exit 0
            ;;
        *)
            echo "Invalid choice. Please select a valid option."
            sleep 2
            ;;
    esac
done

