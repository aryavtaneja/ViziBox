import SwiftUI
import Starscream
import Vision
import AVFoundation

class WebSocketManager: ObservableObject, WebSocketDelegate {
    @Published var image: UIImage?
    @Published var recognizedText: String = "No text"
    let synthesizer = AVSpeechSynthesizer()

    var socket: WebSocket!
    private var imageData: Data = Data()

    init() {
        if let url = URL(string: "http://riadevice.local:8000") {
            socket = WebSocket(request: URLRequest(url: url))
            socket.delegate = self
            socket.connect()
        }
    }

    func disconnect() {
        socket.disconnect()
    }

    func didReceive(event: WebSocketEvent, client: WebSocket) {
        switch event {
        case .connected(let headers):
            print("websocket is connected: \(headers)")
        case .disconnected(let reason, let code):
            print("websocket is disconnected: \(reason) with code: \(code)")
        case .text(_):
            break
        case .binary(let data):
            self.processImageData(data)
        case .ping(_):
            client.write(pong: Data())
        case .pong(_):
            break
        case .viabilityChanged(_):
            break
        case .reconnectSuggested(_):
            break
        case .cancelled:
            break
        case .error(let error):
            print("error: \(String(describing: error))")
        }
    }

    func processImageData(_ data: Data) {
        if imageData.isEmpty {
            let imageSize = data.withUnsafeBytes { $0.load(as: UInt32.self) }
            if imageSize == 0 {
                return
            }
        }

        imageData.append(data)

        if imageData.count >= 4 {
            let imageSize = imageData.withUnsafeBytes { $0.load(as: UInt32.self) }

            if imageData.count - 4 >= Int(imageSize) {
                let imageDataWithoutSize = imageData[4...]
                if let uiImage = UIImage(data: imageDataWithoutSize) {
                    DispatchQueue.main.async {
                        self.image = uiImage
                        self.recognizeText(image: uiImage)
                    }
                    print("UIImage made")
                } else {
                    print("Couldn't make UIImage")
                }

                imageData.removeSubrange(0...Int(imageSize + 4) - 1)
            } else {
                print("Not all data")
            }
        } else {
            print("Not full image")
        }
    }

    func recognizeText(image: UIImage) {
        guard let cgImage = image.cgImage else { return }

        let requestHandler = VNImageRequestHandler(cgImage: cgImage)

        let textRecognitionRequest = VNRecognizeTextRequest { (request, error) in
            guard let observations =
                    request.results as? [VNRecognizedTextObservation] else { return }

            let recognizedStrings = observations.compactMap { observation in
                return observation.topCandidates(1).first?.string
            }

            DispatchQueue.main.async {
                self.recognizedText = recognizedStrings.joined(separator: "\n")
                if self.recognizedText.isEmpty {
                    self.recognizedText = "No text"
                }
                print("Recognized text: \(self.recognizedText)")

                if (self.synthesizer.isSpeaking) {
                    self.synthesizer.stopSpeaking(at: .immediate)
                } else {
                    let utterance = AVSpeechUtterance(string: self.recognizedText)
                    self.synthesizer.speak(utterance)
                }
            }
        }

        textRecognitionRequest.recognitionLevel = .accurate

        try? requestHandler.perform([textRecognitionRequest])
    }
}

struct ContentView: View {
    @StateObject private var webSocketManager = WebSocketManager()

    var body: some View {
        VStack {
            if let image = webSocketManager.image {
                Image(uiImage: image)
                    .resizable()
                    .aspectRatio(contentMode: .fit)
                    .padding()
            } else {
                ProgressView("Loading Image...")
                    .padding()
            }
        }
        .onAppear {
            // You can do any initialization logic here
        }
        .onReceive(NotificationCenter.default.publisher(for: UIApplication.willTerminateNotification)) { _ in
            // Perform your cleanup tasks here
            print("App is about to terminate. Performing cleanup...")
            webSocketManager.disconnect()
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
