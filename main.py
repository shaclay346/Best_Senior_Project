# main.py
# Main File for Virtual Assistant
# Do the following to properly run this script:
# brew install portaudio
# pip install 'speechrecognition', 'pyaudio', and 'pyttsx3' before running
import speech_recognition as sr
import widgits, pyttsx3

def main():
	recognizer = sr.Recognizer()

	# for index, name in enumerate(sr.Microphone.list_microphone_names()):
		# print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

	while True:
		try:
			with sr.Microphone() as mic:
				recognizer.adjust_for_ambient_noise(mic, duration=0.2)
				audio = recognizer.listen(mic)

				# Use Google's STT and Get Text Back
				text = recognizer.recognize_google(audio)
				text = text.lower()

				print(f"Recognized: {text}")

		except:# sr.UnknownValueError():
			# print("Error")
			# recognizer = sr.Recognizer()
			continue





if __name__ == '__main__':
	main()