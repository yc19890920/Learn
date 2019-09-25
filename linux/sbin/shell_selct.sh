#!/bin/bash

select choice in 1yuan 2yuan 5yuan Quit ;do
    case $choice in
        1yuan)
            echo "You can buy a glass of water "
            ;;
        2yuan)
            echo "You can buy  an ice cream "
            ;;
        5yuan)
            echo "You can buy  a chicken leg "
            echo "Choice $REPLY"
            ;;
        Quit)
            echo "Bye"
            break
            ;;
        *)
            echo "Enter error!"
            exit 2

    esac
done