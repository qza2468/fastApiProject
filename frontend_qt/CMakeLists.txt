cmake_minimum_required(VERSION 3.21)
project(untitled)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

set(CMAKE_PREFIX_PATH "/home/qza2468/Qt/6.2.3/gcc_64")

find_package(Qt6 COMPONENTS
        Core
        Gui
        Widgets
        Network
        REQUIRED)

add_executable(untitled main.cpp LoginWin.cpp LoginWin.h globals.cpp globals.h QzaFile.cpp QzaFile.h Path.cpp Path.h)
target_link_libraries(untitled
        Qt::Core
        Qt::Gui
        Qt::Widgets
        Qt::Network
        )

