//
//  ContentView.swift
//  AIpron
//
//  Created by Capstone on 2025-01-08.
//

import SwiftUI

// Sign in Page for the App
struct SignInView: View {
    
    @State var ready = false
    
    var body: some View{
        
        // ready false when not signed it
        if ready == false{
            Button("Sign In with Apple "){
                self.ready = true
            }
            .font(.title2)
            .frame(width: 240, height: 40)
            .background(Color(.black))
            .foregroundColor(.white)
            .cornerRadius(/*@START_MENU_TOKEN@*/3.0/*@END_MENU_TOKEN@*/)
             .padding(.top,10)
        }
        //button clicked,ready set to true, move to main menu page
        else{
            MainMenuView()
        }
    }
}

//botom tab structer which leads to recipe data list, new recipe set and safety tips

struct MainMenuView: View {
    
    var body: some View {
        TabView(){
            //shows view for recipe list
            AddNewRecipeView()
                .tabItem {
                    //design or edit tab view
                    Image(systemName: "car")
                    Text("New Recipe")
                }
                
            //shows view for safety tips
            Text("List Safety Tips")
                //design or edit tab view
                .tabItem {
                    Image(systemName: "a")
                    Text("Menu")
                }
            //shows view for adding a new recipe
            
            RecipeDatabaseView()
            .tabItem {
                //design or edit tab view
                Image(systemName: "house")
                Text("Old Recipies")
            }
        }
       
    }
    
}

struct SignInView_Previews: PreviewProvider {
    static var previews: some View {
        SignInView()
    }
}
