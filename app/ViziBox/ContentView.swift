import SwiftUI
import Vision
import AVFoundation

struct ContentView: View {
    @State var image: UIImage? = nil
    @State var recognizedText: String = "No text"
    let timer = Timer.publish(every: 0.5, on: .main, in: .common).autoconnect() // interval set to 0.5 seconds
    let synthesizer = AVSpeechSynthesizer()

    var body: some View {
        VStack {
            if let uiImage = image {
                Image(uiImage: uiImage)
                    .resizable()
                    .aspectRatio(contentMode: .fit)
            } else {
                Text("Loading image...")
            }
        }
        .onReceive(timer) { _ in
            fetchImage()
        }
    }

    func fetchImage() {
        guard let url = URL(string: "http://riadevice.local:8080") else {
            print("Invalid URL")
            return
        }

        print("Valid URL")

        let task = URLSession.shared.downloadTask(with: url) { (localURL, response, error) in
            if let error = error {
                print("New Error: \(error)")
                return
            }

            // Check the response status code
            guard let httpResponse = response as? HTTPURLResponse,
                  httpResponse.statusCode == 200,
                  let localURL = localURL else {
                print("Invalid response")
                return
            }

            print("OK Response")

            do {
                let data = try Data(contentsOf: localURL)

                // Create a UIImage from the received image data
                if let image = UIImage(data: data) {
                    DispatchQueue.main.async {
                        self.image = image
                        recognizeText(image: image)
                    }
                } else {
                    print("Invalid image data")
                }
            } catch {
                print("File read error: \(error)")
            }
        }

        // Start the download task
        task.resume()
    }
    
    func recognizeText(image: UIImage) {
        guard let cgImage = image.cgImage else { return }
        
        // Create a new image-request handler.
        let requestHandler = VNImageRequestHandler(cgImage: cgImage)

        // Create a new request to recognize text.
        let request = VNRecognizeTextRequest { (request, error) in
            guard let observations =
                    request.results as? [VNRecognizedTextObservation] else { return }
            
            let recognizedStrings = observations.compactMap { observation in
                // Returns the string of the top VNRecognizedText instance.
                return observation.topCandidates(1).first?.string
            }
            
            DispatchQueue.main.async {
                self.recognizedText = recognizedStrings.joined(separator: "\n")
                if self.recognizedText.isEmpty {
                    self.recognizedText = "No text"
                }
                
                // Speak the recognized text immediately after recognition
                speakText()
            }
        }
        
        request.recognitionLevel = .accurate
        try? requestHandler.perform([request])
    }
    
    func speakText() {
        let utterance = AVSpeechUtterance(string: recognizedText)
        synthesizer.speak(utterance)
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
