//
//  FullRecipeView.swift
//  AIpron
//
//  Created by Capstone on 2025-01-09.
//

import SwiftUI

struct DetailedRecipeView: View {
    
    var recipe: RecipeData
    
    var body: some View{
        
            VStack(spacing:10){
                
                Text(recipe.title)
                    .font(.title)
                    .fontWeight(.semibold)
                    .lineLimit(/*@START_MENU_TOKEN@*/2/*@END_MENU_TOKEN@*/)
                    .multilineTextAlignment(.center)
                    .padding(.horizontal,4)
                    .offset(x: 0, y: -50)
                
                Image(recipe.imageName)
                    .resizable()
                    .scaledToFit()
                    .frame(height: 150)
                    .cornerRadius(12)
                    .foregroundColor(.secondary)
                    .offset(x: /*@START_MENU_TOKEN@*/10.0/*@END_MENU_TOKEN@*/, y:-40)
                
                HStack(spacing: 100){
                    Label(recipe.yield,systemImage: "eyes")
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                    Text("Cook Time: \(recipe.TotalRecipeTime) min")
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                        .padding(.trailing,20)
                    
                }
                .offset(x: /*@START_MENU_TOKEN@*/10.0/*@END_MENU_TOKEN@*/, y:-30)
                
                HStack(spacing: 100){
                    Text("Ingredients")
                        .font(.title3)
                    
                    Text("Instructions")
                        .font(.title3)
                        .padding(.trailing,20)
                }
                .offset(x: /*@START_MENU_TOKEN@*/10.0/*@END_MENU_TOKEN@*/, y:-20)
                
                HStack{
                    List(recipe.ingredients, id: \.self){ingredient in
                        
                        Text("\(ingredient)")
                            .font(.footnote)
                            .padding(10)
                    }
                    
                    List(recipe.instructions, id: \.self){instruction in
                        
                        Text("\(instruction)")
                            .font(.footnote)
                            .padding(10)
                    }
                }
                .offset(x: /*@START_MENU_TOKEN@*/10.0/*@END_MENU_TOKEN@*/, y:-30)
                
                Link(destination: recipe.url, label: {
                    Text("Visit Site")
                        .bold()
                        .font(.title2)
                        .frame(width: 240, height:40)
                        .background(Color(.systemRed))
                        .foregroundColor(.white)
                        .cornerRadius(/*@START_MENU_TOKEN@*/3.0/*@END_MENU_TOKEN@*/)
                })
                
                NavigationLink(
                    destination: RunRecipe(individualRecipe: recipe),
                    label: {
                        Text("Lets Get Cooking")
                            .bold()
                    })
                    .font(.title2)
                    .frame(width: 240, height: 40)
                    .background(Color(.systemRed))
                    .foregroundColor(.white)
                    .cornerRadius(/*@START_MENU_TOKEN@*/3.0/*@END_MENU_TOKEN@*/)
                    .padding(.bottom,5)
                    
            }

    }
}



struct RecipeSDetailView_Previews: PreviewProvider{
    static var previews: some View{
        DetailedRecipeView(recipe: RecipeList.topTen.first!)
    }
}
