//
//  OldRecipe.swift
//  AIpron
//
//  Created by Capstone on 2025-01-09.
//

import SwiftUI

// dynamic list view 
struct RecipeDatabaseView: View {
     
    @State var individualRecipe: [RecipeData] = RecipeList.topTen
    
    var body: some View{
        NavigationView{
            List(individualRecipe,id: \.id){Recipe in
                
                NavigationLink(
                    destination: DetailedRecipeView(recipe: Recipe),
                    label: {
                       RecipeCellView(individualRecipe: Recipe)
                        }
                    )
            }
            .navigationTitle(Text("Recipe List"))
            .navigationBarTitleDisplayMode(.automatic)
            .toolbar(content: {
                ToolbarItem(placement: .navigationBarTrailing){
    
                    Button("Refresh"){
                        
                        individualRecipe = RecipeList.topTen
                        
                    }
                }
            })
            
           
            
            
        }
        .navigationViewStyle(StackNavigationViewStyle())
        
    }

}


struct RecipeCellView: View{
    
    var individualRecipe: RecipeData
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
        RecipeDatabaseView()
    }
}

