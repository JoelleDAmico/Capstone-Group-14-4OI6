//
//  RecipeRunView.swift
//  AIpron
//
//  Created by Capstone on 2025-01-10.
//

import SwiftUI

struct RunRecipe: View {
    
    var individualRecipe: RecipeData
    
    var body: some View{
        
        
        VStack{
            TabView {
                ForEach(individualRecipe.instructions,id: \.self){ instruction in
                    
                    Text("\(instruction)")
                        .padding(20)
                }
                
                Text("Yippee, Food Time")
                
            }
            .tabViewStyle(PageTabViewStyle())
        
            timerView()
            
        }
        .background(Image("bg1")
                        .resizable()
                        .edgesIgnoringSafeArea(/*@START_MENU_TOKEN@*/.all/*@END_MENU_TOKEN@*/))
        
    }
}

struct timerView: View {
    @State private var hrs = 0 // state variable to store selected hrs
    @State private var mins = 0 // state variable to store selected mins
    @State private var secs = 0 // state variable to store selected secs
    @State private var timeRemaining = 0 // state variable to store selected hrs
    @State private var timerisActive = false // state variable to store selected mins
    @State private var timer: Timer? = nil // state variable to store selected secs
    var body: some View {
        
        VStack{
            HStack{
                Picker(selection: $hrs, label: Text("Hours"), content: {
                    ForEach(0..<24){ hour in
                        Text("\(hour)").tag(hour)
                        
                    }
                })
                .frame(width: 100,height: 75)
                .clipped()
                
                Picker(selection: $mins, label: Text("Minutes"), content: {
                    ForEach(0..<24){ minute in
                        Text("\(minute)").tag(minute)
                        
                    }
                })
                .frame(width: 100,height: 75)
                .clipped()

                Picker(selection: $secs, label: Text("Seconds"), content: {
                    ForEach(0..<24){ sec in
                        Text("\(sec)").tag(sec)
                    }
                })
                .frame(width: 100,height: 75)
                .clipped()

            }
            .pickerStyle(WheelPickerStyle())
            .labelsHidden()

            HStack{
            Button(action: startTimer){
                Text(timerisActive ? "Reset Timer":"Start Timer")
                    .font(.title3)
                    .padding()
                    .background(timerisActive ? Color.red : Color.blue)
                    .foregroundColor(.white)
                    .cornerRadius(30)
            }
            .padding()
            
            if timerisActive{
                Text("\(timeString(from: timeRemaining))")
                    .font(.title3)
                    .padding()
            }
            }
        }
    }
    func startTimer(){
        if timerisActive{
            timer?.invalidate() //stop timmer
            timer = nil
            timerisActive = false
            timeRemaining = 0
        }
        else{
            timeRemaining = hrs*3600 + mins*60 + secs
            timerisActive = true
            
            timer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true){ _ in
                if self.timeRemaining > 0 {
                    self.timeRemaining -= 1
                }else{
                    self.timer?.invalidate()
                    self.timerisActive = false
                }
            }
        }
    }
    
    func timeString(from secs: Int) ->String {
        let h = secs/3600
        let m = (secs%3600)/60
        let s = (secs%60)
        return String(format: "%02d:%02d:%02d",h,m,s)
        
    }
}
   


struct RunRecipeView_Previews: PreviewProvider{
    static var previews: some View{
        RunRecipe(individualRecipe: RecipeList.topTen.first!)
    }
}
