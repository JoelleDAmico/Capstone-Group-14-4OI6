//
//  File.swift
//  AIpron
//
//  Created by Capstone on 2025-01-08.
//

import Foundation
import SwiftUI
import AuthenticationServices
// struct to show text field and link to add a new recipe

struct AddNewRecipeView: View {
    
    @EnvironmentObject var network: Network
    
    @State private var recipeUrl = "https://www.allrecipes.com/recipe/158968/spinach-and-feta-turkey-burgers/"
    @State private var alert = false
    
    @State var status = "No recipe found!! Try Again"
    
    var body: some View {
        NavigationView{
            VStack{
                
                //text field that takes in the recipe url
                TextField("Enter Recipe Link Here",text: $recipeUrl)
                    .padding(4)
                    .overlay(
                        RoundedRectangle(cornerRadius: 14)
                            .stroke(Color.blue, lineWidth: 2)
                    )
                    .padding()
                    
                    
                    NavigationLink(
                        destination: AddedRecipeView(recipe_url: "\(recipeUrl)"),
                       label: {
                           Text("View Recipe")
                               .bold()
                       })
                       .font(.title2)
                       .frame(width: 240, height: 40)
                       .background(Color(.systemRed))
                       .foregroundColor(.white)
                       .cornerRadius(/*@START_MENU_TOKEN@*/3.0/*@END_MENU_TOKEN@*/)
                        .padding(.top,10)
                
            }
        }
    }
}




struct NewRecipe_Previews: PreviewProvider {
    static var previews: some View {
        AddedRecipeView(recipe_url: "https://www.allrecipes.com/recipe/158968/spinach-and-feta-turkey-burgers/")
            .environmentObject(Network())
    }
}

struct AddedRecipeView: View {
    @EnvironmentObject var network: Network
    @State var recipe_url: String
    @State private var alert = false
    
    
    var body: some View {
        VStack(spacing:10){
            
            Text("\(network.user.title)")
                .font(.title)
                .fontWeight(.semibold)
                .lineLimit(/*@START_MENU_TOKEN@*/2/*@END_MENU_TOKEN@*/)
                .multilineTextAlignment(.center)
                .padding(.horizontal,4)
                .offset(x: 0, y: -20)
            
            Image(network.user.imageName)
                .resizable()
                .scaledToFit()
                .frame(height: 150)
                .cornerRadius(12)
                .foregroundColor(.secondary)
                .offset(x: /*@START_MENU_TOKEN@*/10.0/*@END_MENU_TOKEN@*/, y:-10)
            
            HStack(spacing: 100){
                Label("\(network.user.recipeYield)",systemImage: "eyes")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                Text("Cook Time: \(network.user.TotalRecipeTime) min")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                    .padding(.trailing,20)
                
            }
            .offset(x: /*@START_MENU_TOKEN@*/10.0/*@END_MENU_TOKEN@*/, y:0)
            
            HStack(spacing: 100){
                Text("Ingredients")
                    .font(.title3)
                
                Text("Instructions")
                    .font(.title3)
                    .padding(.trailing,20)
            }
            .offset(x: /*@START_MENU_TOKEN@*/10.0/*@END_MENU_TOKEN@*/, y:10)
            
            HStack{
                List(network.user.ingredients.trimmingCharacters(in: CharacterSet(charactersIn: "[]")).components(separatedBy: ","), id: \.self){ingredient in
                    
                    Text("\(ingredient)")
                        .font(.footnote)
                        .padding(10)
                }
                
                List(network.user.instructions.components(separatedBy: "\\n"), id: \.self){instruction in
                    
                    Text("\(instruction)")
                        .font(.footnote)
                        .padding(10)
                }
                
            }
            .offset(x: /*@START_MENU_TOKEN@*/10.0/*@END_MENU_TOKEN@*/, y:0)
            
            Link(destination: URL(string: "https://www.youtube.com/watch?v=gs8qfL9PNac")!, label: {
                Text("Visit Site")
                    .bold()
                    .font(.title2)
                    .frame(width: 240, height:40)
                    .background(Color(.systemRed))
                    .foregroundColor(.white)
                    .cornerRadius(/*@START_MENU_TOKEN@*/3.0/*@END_MENU_TOKEN@*/)
            })
            
            Button("Add Recipe "){
                self.alert = true
                // alerts are used in a different set defined here for trial purposes
            }
            .alert(isPresented: $alert, content: {
                //provides an alert and can be used for initating communication by calling required function in action
                Alert(title: Text("Wohoooo") ,
                      message: Text("Recipe Added"),
                      dismissButton: .default(Text("Bye"),action: buttonClicked))
            })
            
            
        }
        
        .padding(.vertical)
        .onAppear {
            network.getUsers(input_url: recipe_url)
        }
        
        
    }
    func buttonClicked(){
        
        RecipeList.topTen.append(RecipeData(imageName: network.user.imageName,
                                            title: network.user.title,
                                            recipe: network.user.recipe,
                                            TotalRecipeTime: network.user.TotalRecipeTime,
                                            chef: network.user.chef,
                                            ingredients: network.user.ingredients.trimmingCharacters(in: CharacterSet(charactersIn: "[]")).components(separatedBy: ","),
                                            instructions: network.user.instructions.components(separatedBy: "\\n"),
                                            yield: network.user.recipeYield,
                                            url: URL(string:network.user.url)!))
        
        
        
        
        
    }
    
}




class Network: ObservableObject {
    @Published var user: User = User(imageName: "", title: "",recipe: "",TotalRecipeTime: "", chef:"",ingredients: "", instructions: "" ,recipeYield:"",url: "")
    @Published var error: String = "hi"
    
    
    func getUsers(input_url: String) {
     
        guard let url = URL(string: "https://g0pifns1z5.execute-api.us-east-2.amazonaws.com/hopefully_valid_json/links?link_input=" + input_url) else { fatalError("Missing URL") }
        
        let urlRequest = URLRequest(url: url)
        
        let dataTask = URLSession.shared.dataTask(with: urlRequest) { (data, response, error) in
            
            if let error = error {
                print("Request error: ", error)
                return
            }
            
            
            guard let response = response as? HTTPURLResponse else { return }
            
            
            
            if response.statusCode == 200 {
                guard let data = data else { return }
                DispatchQueue.main.async {
                    do {
                        let decodedUser = try JSONDecoder().decode(User.self, from: data)
                        self.user = decodedUser
                    } catch let error {
                        print("Error decoding: ", error)
                    }
                }
            }
        }
        
        dataTask.resume()
    }
}


struct User: Decodable {
    var imageName: String
    var title: String
    var recipe: String
    var TotalRecipeTime: String
    var chef: String
    var ingredients: String
    var instructions: String
    var recipeYield: String
    var url: String
}
