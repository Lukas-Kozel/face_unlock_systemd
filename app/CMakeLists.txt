cmake_minimum_required(VERSION 3.14)

# Set the project name and version
project(FaceRecognitionApp VERSION 1.0 LANGUAGES CXX)

# Ensure CMake processes the moc files
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

# Find required Qt packages
#set(CMAKE_PREFIX_PATH "/path/to/qt")  # Adjust this to your Qt installation path
find_package(Qt5 COMPONENTS Core Gui Widgets Network REQUIRED)

# Add the executable
add_executable(FaceRecognitionApp
    main.cpp
    MainWindow.cpp
    MainWindow.h
)

# Link Qt libraries
target_link_libraries(FaceRecognitionApp Qt5::Core Qt5::Gui Qt5::Widgets Qt5::Network)

# Include Qt headers
target_include_directories(FaceRecognitionApp PRIVATE ${Qt5Widgets_INCLUDE_DIRS})

