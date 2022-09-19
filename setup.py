from setuptools import setup, find_packages

setup(
    include_package_data=True,
    name="FSCVA",
    version="1.0.0",
    description="A virtual assistant for florida southern students.",
    author="Shane Claycomb, Nickolas Auen, William Davidson",
    packages=find_packages(),
    install_requires=["speechrecognition",
    "pyaudio",
    "pyttsx3",
    "bs4",
    "google",
    "keyboard",
    "pandas",
    "requests_html",
    "requests",
    "playsound==1.2.2",
    "nltk",
    "sklearn",
    "openpyxl",
    "numpy"]
)