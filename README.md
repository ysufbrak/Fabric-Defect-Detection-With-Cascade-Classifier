
# Fabric Defect Detection Tool

An intuitive tool designed to detect fabric defects using a Cascade Classifier. With a user-friendly interface and customizable annotation tool, it empowers quality control in textile manufacturing by identifying common fabric defects in real-time.

## Features

- **Real-time Fabric Defect Detection**: Utilize your camera to instantly identify fabric defects using computer vision.
- **User-friendly Interface**: Powered by `customtkinter`, the tool offers a seamless experience with no command-line hassle.
- **Custom Annotation Tool**: Built-in tool to help users create annotations in specific formats for training purposes.

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Annotation Tool](#annotation-tool)
4. [Training Process](#training-process)
5. [Results](#results)
6. [Dataset](#dataset)
7. [Contributing](#contributing)

## Installation

### Dependencies

Ensure you have the following installed:
- [OpenCV](https://opencv.org/)
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)

```bash
pip install opencv-python-headless customtkinter
```

## Usage

Running the tool is simple thanks to its clear and interactive user interface. Follow these steps:

1. Clone the repository.
2. Run the `InspectionTool.py` file:
   ```bash
   python InspectionTool.py
   ```
3. The interface will guide you through the defect detection process, leveraging your camera for real-time analysis. No need for command-line arguments—the UI is self-explanatory and structured for ease of use.

## Annotation Tool

For those looking to create their own training data, the `AnnotTool.py` is designed to help you generate annotations in the required format.

- **Supported Formats**: YOLO format is fully supported, while the Cascade format is currently a work in progress (WIP).
- **How to Use**: Simply run the `AnnotTool.py` file and follow the on-screen instructions to annotate your images with ease.

```bash
python AnnotTool.py
```

## Training Process

The training process for the Cascade Classifier will be provided soon. Stay tuned for detailed instructions on how to train the model using your own dataset.

## Results

Once defects are detected, the tool highlights them directly on the camera feed. No complex outputs—just an easy-to-interpret visual representation of the detected defects in real-time.

## Dataset

The dataset used to train the model was created manually using Photoshop and contains common fabric defects.

> **Note**: If you need access to the dataset, please send an email to [yusuf.borak420@gmail.com](mailto:yusuf.borak420@gmail.com).

## Contributing

This tool is currently closed-source, but feel free to reach out if you'd like to contribute ideas or improvements. The interface and tools are designed with extensibility in mind, so modifications are welcome for future iterations.