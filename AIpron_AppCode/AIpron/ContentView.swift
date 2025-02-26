//
//  ContentView.swift
//  AIpron
//
//  Created by Capstone on 2025-01-08.
//

import SwiftUI

// Sign in Page for the App
struct ContentView: View {
    
    @State var ready = false
    
    var body: some View{
        
        // ready false when not signed it
        if ready == false{
            Button("Sign In"){
                self.ready = true
            }
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
            OldRecipeView()
                .tabItem {
                    //design or edit tab view
                    Image(systemName: "house")
                    Text("Old Recipies")
                }
                
            //shows view for safety tips
            Text("List Safety Tips")
                //design or edit tab view
                .tabItem {
                    Image(systemName: "a")
                    Text("Menu")
                }
            //shows view for adding a new recipe
            NewRecipe()
                .tabItem {
                    //design or edit tab view
                    Image(systemName: "car")
                    Text("New Recipe")
                }
        }
       
    }
    
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
