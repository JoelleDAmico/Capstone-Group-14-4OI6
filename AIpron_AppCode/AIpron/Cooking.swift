//
//  RecipeRunView.swift
//  AIpron
//
//  Created by Capstone on 2025-01-10.
//

import SwiftUI

struct RunRecipe: View {
    @StateObject private var webSocketManager = WebSocketManager()
    @State private var showAlert = false
    @State private var selectedPage = 0 // Track the current page
    var individualRecipe: RecipeData
    
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
    
    var body: some View{
        
        VStack{
            TabView(selection: $selectedPage) {
                ForEach(individualRecipe.instructions.indices,id: \.self){ instruction in
                    
                    Text("\(individualRecipe.instructions[instruction])")
                        .padding(20)
                    
                    .tag(instruction)
                }
                
                Text("Yippee, Food Time")
                .tag(individualRecipe.instructions.count)
                
            }
            .tabViewStyle(PageTabViewStyle(indexDisplayMode: .always))
            
            HStack{
            Button(action: {
               if selectedPage > 0 {
                   selectedPage -= 1
                   webSocketManager.createSendMessage(ui: "PR")
               }
            }){
               Text("Previous")
                   .padding()
                   .background(selectedPage > 0 ? Color.blue : Color.gray)
                   .foregroundColor(.white)
                   .cornerRadius(8)
            }
            .disabled(selectedPage == 0) // Disable when at the first page
           
            Spacer()
           // Next Button
           Button(action: {
               if selectedPage < individualRecipe.instructions.count {
                   selectedPage += 1
                   webSocketManager.createSendMessage(ui: "N")
               }
           }) {
               Text("Next")
                   .padding()
                   .background(selectedPage < individualRecipe.instructions.count ? Color.green : Color.gray)
                   .foregroundColor(.white)
                   .cornerRadius(8)
           }
           .disabled(selectedPage == individualRecipe.instructions.count)
        }
            
          //  timerView()
            
        }
        .background(Image("bg1")
                        .resizable()
                        .edgesIgnoringSafeArea(/*@START_MENU_TOKEN@*/.all/*@END_MENU_TOKEN@*/))
        .navigationBarItems(trailing: Button(action: {
            print("Custom Button Tapped")
            selectedPage = 0
            webSocketManager.createSendMessage(ui: "R")
            }) {
            HStack {
               Image(systemName: "star.fill")
               Text("Reset")
           }
           .foregroundColor(.blue)
       })
        .onAppear{
            webSocketManager.connect()
            webSocketManager.createSendMessage(ui: "IS")
        }
        .alert(isPresented: $showAlert) {
            Alert(title: Text("AIpron Talks"),
                  message: Text(webSocketManager.receivedMessage),
                  dismissButton: .default(Text("OK")){
                    
                    let parts  = webSocketManager.receivedMessage.components(separatedBy: "!")
                    
                    print(parts)
                    
                    if parts[0] == "Step Complete"{
                        print("hi")
                        selectedPage += 1
                        let msg  = webSocketManager.format_message(header: "\(self.headers["ACK"] ?? "")", payload: "\(self.headers["NEXT"] ?? "")")
                        print(msg)
                        webSocketManager.sendMessage(msg)
                    }
                    
                    if parts[0] == "ALERT"{
                        webSocketManager.createSendMessage(ui: "IP")
                    }
                    
                  })
        }
        .onChange(of: webSocketManager.interrupt_command) { _ in
            showAlert = true // Show alert when a new message is received
        }
        .onDisappear {
            webSocketManager.createSendMessage(ui: "R")
            webSocketManager.disconnect()
        }
    }
}
   
struct RunRecipeView_Previews: PreviewProvider{
    static var previews: some View{
        RunRecipe(individualRecipe: RecipeList.topTen.first!)
    }
}


//struct timerView: View {
//    @State private var hrs = 0 // state variable to store selected hrs
//    @State private var mins = 0 // state variable to store selected mins
//    @State private var secs = 0 // state variable to store selected secs
//    @State private var timeRemaining = 0 // state variable to store selected hrs
//    @State private var timerisActive = false // state variable to store selected mins
//    @State private var timer: Timer? = nil // state variable to store selected secs
//    var body: some View {
//
//        VStack{
//            HStack{
//                Picker(selection: $hrs, label: Text("Hours"), content: {
//                    ForEach(0..<24){ hour in
//                        Text("\(hour)").tag(hour)
//
//                    }
//                })
//                .frame(width: 100,height: 75)
//                .clipped()
//
//                Picker(selection: $mins, label: Text("Minutes"), content: {
//                    ForEach(0..<24){ minute in
//                        Text("\(minute)").tag(minute)
//
//                    }
//                })
//                .frame(width: 100,height: 75)
//                .clipped()
//
//                Picker(selection: $secs, label: Text("Seconds"), content: {
//                    ForEach(0..<24){ sec in
//                        Text("\(sec)").tag(sec)
//                    }
//                })
//                .frame(width: 100,height: 75)
//                .clipped()
//
//            }
//            .pickerStyle(WheelPickerStyle())
//            .labelsHidden()
//
//            HStack{
//            Button(action: startTimer){
//                Text(timerisActive ? "Reset Timer":"Start Timer")
//                    .font(.title3)
//                    .padding()
//                    .background(timerisActive ? Color.red : Color.blue)
//                    .foregroundColor(.white)
//                    .cornerRadius(30)
//            }
//            .padding()
//
//            if timerisActive{
//                Text("\(timeString(from: timeRemaining))")
//                    .font(.title3)
//                    .padding()
//            }
//            }
//        }
//    }
//    func startTimer(){
//        if timerisActive{
//            timer?.invalidate() //stop timmer
//            timer = nil
//            timerisActive = false
//            timeRemaining = 0
//        }
//        else{
//            timeRemaining = hrs*3600 + mins*60 + secs
//            timerisActive = true
//
//            timer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true){ _ in
//                if self.timeRemaining > 0 {
//                    self.timeRemaining -= 1
//                }else{
//                    self.timer?.invalidate()
//                    self.timerisActive = false
//                }
//            }
//        }
//    }
//
//    func timeString(from secs: Int) ->String {
//        let h = secs/3600
//        let m = (secs%3600)/60
//        let s = (secs%60)
//        return String(format: "%02d:%02d:%02d",h,m,s)
//
//    }
//}
