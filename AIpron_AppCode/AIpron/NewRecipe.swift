//
//  File.swift
//  AIpron
//
//  Created by Capstone on 2025-01-08.
//

import Foundation
import SwiftUI

// struct to show text field and link to add a new recipe

struct NewRecipe: View {
    
    @State private var recipeUrl = ""
    @State private var alert = false
    
    var body: some View {
        VStack{
            
            //text field that takes in the recipe url
            TextField("Enter Recipe Link Here",text: $recipeUrl)
                .padding(4)
                .overlay(
                        RoundedRectangle(cornerRadius: 14)
                .stroke(Color.blue, lineWidth: 2)
                )
                .padding()
            
            // will raise a request or use aws to communicate with data scraping tool
            Button("Enter"){
                self.alert = true // alerts are used in a different set defined here for trial purposes
            }
            .alert(isPresented: $alert, content: {
                //provides an alert and can be used for initating communication by calling required function in action
                Alert(title: Text("Beware") ,
                      message: Text("Psych"),
                      dismissButton: .default(Text("Bye"),action: buttonClicked))
            })

        }
    }
}

private func buttonClicked(){
    print("Button Clicked")
    
}
