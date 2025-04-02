//
//  webSocketHandler.swift
//  AIpron
//
//  Created by Capstone on 2025-03-30.
//

import SwiftUI
import Combine
import Foundation

class WebSocketManager: ObservableObject {
    @Published var receivedMessage: String = ""
    @Published var interrupt_command = false
    @Published var step_index: Int = 0
    @Published var interrupt_code: Int = 0
    
    private var webSocketTask: URLSessionWebSocketTask?
//    private let serverURL =  "ws://localhost:8765"
    private let serverIP = "172.17.196.244"
    private let port = "8765"
    
    private var cancellables = Set<AnyCancellable>()
    
    let headers: [String: String] = [
        "ACK": "1",
        "SYN": "10",
        "DATA": "11",
        "NEXT": "12",
        "PRV": "13",
        "FIN": "20",
        "RST": "30",
        "HEARTBEAT": "40",
        "INTR": "60",
        "PASS": "70",
        "INVALID": "FF"
    ]
    
    let dangerCodes: [Int: String] = [
        1: "FIRE",
        2: "CHOPPING TECHNIQUE",
        3: "LACERATION",
        4: "BURNS"
    ]
    
//    init() {
//        connect()
//    }
    
    func updateReciveMessage(){
        receivedMessage = ""
    }
    
    func format_message(header: String, payload: String) ->String {
        return "\(header):\(payload)"
    }
    
    func format_chopped_message(header: String, sequence: String, payload: String) -> String {
        return "\(header):\(sequence):\(payload)"
    }
    
    func parse_message(message: String) -> (header:String, sequence: String, payload: String){
        let parts = message.components(separatedBy: ":")
        let header = parts[0]
        let sequence = parts.count > 2 ? parts[1] : ""
        let payload = parts.count > 2 ? parts[2] : (parts.count > 1 ? parts[1] : "")
        return (header,sequence,payload)
    }
    
    
    func recieve_message(ws:URLSessionWebSocketTask?){
        print("[RECEIVE] Listening for messages...")
    }
    
    
        
    func connect() {
//        guard let url = URL(string: serverURL) else { return }
        guard let url = URL(string: "ws://\(serverIP):\(port)") else { return }
        let session = URLSession(configuration: .default)
        webSocketTask = session.webSocketTask(with: url)
        webSocketTask?.resume()
        print("✅ Connected to WebSocket")
        receiveMessages()
    }
        
    
    private func processReceivedMessage(message: String) {
        let components = parse_message(message: message)
    
        DispatchQueue.main.async { [self] in
            if components.header == self.headers["INTR"], let code = Int(components.payload) {
                    print("Interrupt Received: \(self.dangerCodes[code] ?? "UNKOWN") Take action.")
                    self.interrupt_code = code
                    let msg  = self.format_message(header: "\(self.headers["ACK"] ?? "")", payload: "\(self.headers["INTR"] ?? "")")
                    self.receivedMessage = "ALERT!!! \(self.dangerCodes[code] ?? "UNKOWN")"
                    self.sendMessage(msg)
                    interrupt_command.toggle()
                    print(interrupt_command)
            }
            
            else if components.header == self.headers["NEXT"], let step = Int(components.payload) {
                print("Machine initiated next to step: \(components.payload). Reported Result: \(components.sequence).")
                self.step_index = step
                self.receivedMessage = ""
                self.receivedMessage = "Step Complete!!! Go to Page \(step_index)"
                interrupt_command.toggle()
                print(interrupt_command)
                
            }
            else if components.header == self.headers["ACK"] && components.payload == self.headers["SYN"] {
                self.receivedMessage = ""
                self.receivedMessage = "System Connected"
                interrupt_command.toggle()
                print(interrupt_command)
            }
            else {
                print("Received: \(message)")
            }
        }
    }
    
    
    private func receiveMessages() {
        webSocketTask?.receive { [weak self] result in
            guard let self = self else { return }

            switch result {
            case .success(let message):
                switch message {
                case .string(let text):
                    DispatchQueue.main.async {
                        self.processReceivedMessage(message: text)
                        
                            //   self.receivedMessage = text
                    }
                case .data(let data):
                    print("📩 Received data: \(data)")
                @unknown default:
                    print("Unknown message format")
                }
                self.receiveMessages()
            case .failure(let error):
                print("[RECEIVE] Error receiving message: \(error)")
                DispatchQueue.main.async {
                self.receivedMessage = " Device not connected"
                self.interrupt_command.toggle()
                }
            }
        }
    }

        
    
        
    func sendMessage(_ sent_message: String) {
            let sent_message = URLSessionWebSocketTask.Message.string(sent_message)
            webSocketTask?.send(sent_message) { error in
                if let error = error {
                    
                    print("❌ Error sending message: \(error)")
                    DispatchQueue.main.async {
                    self.interrupt_command.toggle()
                    self.receivedMessage = " Device not connected"
                    }
                } else {
                    print("📨 Message sent: \(sent_message)")
                }
            }
        }
    
    
    func createSendMessage(ui: String){
        
        if ui == "IS"{
            sendMessage("\(headers["SYN"] ?? ""):")
            sendMessage(format_chopped_message(header: "\(headers["DATA"] ?? "")",sequence: "0", payload: "roughly chop onion"))
            sendMessage(format_chopped_message(header: "\(headers["DATA"] ?? "")",sequence: "1",payload: "slice onion"))
            sendMessage(format_chopped_message(header: "\(headers["DATA"] ?? "")",sequence: "2",payload: "caramelize onion"))
            sendMessage(format_chopped_message(header: "\(headers["DATA"] ?? "")",sequence: "3",payload: "All Done!"))
            sendMessage(format_message(header: "\(headers["FIN"] ?? "")", payload: "" ))
            
        }
        
        if ui == "N"{
            step_index += 1
            let sent_msg = format_message(header: "\(headers["NEXT"] ?? "")",payload: "\(step_index)")
            sendMessage(sent_msg)
            print("Sent N: " + sent_msg)
            
        }
        
        if ui == "PR"{
            step_index = max(0, step_index - 1)
            let sent_msg = format_message(header: "\(headers["PRV"] ?? "")",payload: "\(step_index)")
            sendMessage(sent_msg)
            print("Sent PR: " + sent_msg)
            
        }
        
        if ui == "IP"{
            let sent_msg = format_message(header: "\(headers["PASS"] ?? "")", payload: "\(interrupt_code)")
            sendMessage(sent_msg)
            print("Sent PASS: " + sent_msg)
        }
        
        if ui == "R"{
            step_index = 0
            interrupt_code = 0
            let sent_msg = format_message(header: "\(headers["RST"] ?? "")",payload: "")
            sendMessage(sent_msg)
            print("Sent RST: " + sent_msg)
        }
        
//     testing
        if ui == "INTR"{
            let sent_msg = format_message(header: "\(headers["INTR"] ?? "")", payload: "2")
            sendMessage(sent_msg)
            print("Sent NEXT: " + sent_msg)
        }
        
        if ui == "NEXT"{
            let sent_msg = format_chopped_message(header: "\(headers["NEXT"] ?? "")",sequence: "\(step_index)",payload: "\(step_index+1)")
            sendMessage(sent_msg)
            print("Sent INTR: " + sent_msg)
        }
        
    }
    
    func disconnect() {
        webSocketTask?.cancel(with: .goingAway, reason: nil)
        self.receivedMessage = " Device not connected"
        self.interrupt_command.toggle()
        print("🔴 WebSocket Disconnected")
    }
    

}

