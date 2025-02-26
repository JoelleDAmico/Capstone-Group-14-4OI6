//
//  OldRecipe.swift
//  AIpron
//
//  Created by Capstone on 2025-01-09.
//

import SwiftUI

// dynamic list view 
struct OldRecipeView: View {
    var a = 0
    var individualRecipe: [RecipeDataView] = RecipeList.topTen
    
    var body: some View{
        NavigationView{
            List(individualRecipe,id: \.id){Recipe in
                
                NavigationLink(
                    destination: RecipeDetailView(recipe: Recipe),
                    label: {
                       RecipeCellView(individualRecipe: Recipe)
                        }
                    )
            }
                .navigationTitle(Text("Recipe List"))
            .navigationBarTitleDisplayMode(.automatic)
           
            
            
        }
        .navigationViewStyle(StackNavigationViewStyle())
    }

}


struct RecipeCellView: View{
    
    var individualRecipe: RecipeDataView
    var body: some View{
        HStack{
            Image(individualRecipe.imageName)
                .resizable()
                .scaledToFit()
                .frame(height: 70)
                .cornerRadius(4)
                .padding(.vertical,5)
            
            VStack(alignment: .leading, spacing:5){
                Text(individualRecipe.title)
                    .fontWeight(.semibold)
                    .lineLimit(/*@START_MENU_TOKEN@*/2/*@END_MENU_TOKEN@*/)
                    .minimumScaleFactor(0.5)
                
                HStack{
                Text("By \(individualRecipe.chef)")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                    
                Spacer()
                Text("Cook Time: \(individualRecipe.TotalRecipeTime) min")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                    
                    
                        
                }
            }
        }
    }
}



struct RecipeDetailView_Previews: PreviewProvider{
    static var previews: some View{
        OldRecipeView()
    }
}

