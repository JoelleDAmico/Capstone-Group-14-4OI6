//
//  RData.swift
//  AIpron
//
//  Created by Capstone on 2025-01-09.
//

import SwiftUI


class RecipeData: Identifiable, ObservableObject{
    
    let id = UUID()
    let imageName: String
    let title: String
    let recipe: String
    let TotalRecipeTime: String
    let chef: String
    let ingredients: Array<String>
    let instructions: Array<String>
    let yield: String
    let url: URL
    
    
    init(imageName: String,title: String,recipe: String, TotalRecipeTime: String,chef: String, ingredients: Array<String>,instructions: Array<String>,yield: String,url: URL){
        
        
        self.imageName = imageName
        self.title = title
        self.recipe = recipe
        self.TotalRecipeTime = TotalRecipeTime
        self.chef = chef
        self.ingredients = ingredients
        self.instructions = instructions
        self.yield = yield
        self.url = url
    }
    

}


struct RecipeList {
    var data: [RecipeData]
    
    static var topTen = [
        RecipeData(imageName: "appstore",
              title: "Pasta Bolegnese with Gluton free Spagetti",
              recipe: "In this video I discuss 9 things I wish I knew before I started programming. Knowing these things would have made my journey in becoming a full-time iOS developer so much faster and easier. I hope this advice helps someone out there that's early in their career as a software developer.",
              TotalRecipeTime: "5",
              chef: "Ankit",
              ingredients: [
                "1 lb chicken thighs or breasts (boneless, skinless)",
                "Salt and pepper to taste",
                "1/4 cup all-purpose flour (for coating)",
                "2 tbsp butter",
                "3-4 cloves garlic, minced",
                "1/3 cup honey",
                "1/4 cup soy sauce (low-sodium preferred)",
                "2 tbsp water (optional, to adjust sauce consistency)",
                "1 tsp cornstarch (optional, mixed with 1 tbsp water for thickening)",
                "Sesame seeds for garnish (optional)",
                "Green onions, chopped for garnish (optional)"
            ],
              instructions: [
                  "Season the chicken pieces with salt and pepper.",
                  "Lightly coat the chicken in flour, shaking off excess.",
                  "Heat butter in a large skillet over medium heat.",
                  "Add the chicken and sear for 3-4 minutes on each side until golden brown. Remove and set aside.",
                  "In the same skillet, reduce heat to medium and add minced garlic. Sauté for 30 seconds until fragrant.",
                  "Stir in honey and soy sauce. (Add water if the sauce seems too thick.)",
                  "Bring the mixture to a simmer.",
                  "Return the chicken to the skillet, coating it with the sauce.",
                  "Cover and simmer for 10-12 minutes until the chicken is fully cooked (internal temperature reaches 165°F/74°C).",
                  "If a thicker sauce is desired, mix cornstarch and water, then stir it into the skillet. Cook for another minute.",
                  "Sprinkle sesame seeds and chopped green onions on top.",
                  "Serve hot over steamed rice, noodles, or alongside vegetables."
              ],
              yield: "2 Servings",
              url: URL(string: "https://www.youtube.com/watch?v=gs8qfL9PNac")!),
        
              
        
        RecipeData(imageName: "appstore",
              title: "Sushi",
              recipe: "In the first video of my Swift Beginner Series, you will build your first iOS App in Swift in 30 minutes in Xcode. Together, we will build a basic music player app that will play random songs from your iTunes library filtered by whatever genre you like.",
              TotalRecipeTime: "5",
              chef: "Ankit",
              ingredients: [
                "1 lb chicken thighs or breasts (boneless, skinless)",
                "Salt and pepper to taste",
                "1/4 cup all-purpose flour (for coating)",
                "2 tbsp butter",
                "3-4 cloves garlic, minced",
                "1/3 cup honey",
                "1/4 cup soy sauce (low-sodium preferred)",
                "2 tbsp water (optional, to adjust sauce consistency)",
                "1 tsp cornstarch (optional, mixed with 1 tbsp water for thickening)",
                "Sesame seeds for garnish (optional)",
                "Green onions, chopped for garnish (optional)"
            ],
              instructions: [
                  "Season the chicken pieces with salt and pepper.",
                  "Lightly coat the chicken in flour, shaking off excess.",
                  "Heat butter in a large skillet over medium heat.",
                  "Add the chicken and sear for 3-4 minutes on each side until golden brown. Remove and set aside.",
                  "In the same skillet, reduce heat to medium and add minced garlic. Sauté for 30 seconds until fragrant.",
                  "Stir in honey and soy sauce. (Add water if the sauce seems too thick.)",
                  "Bring the mixture to a simmer.",
                  "Return the chicken to the skillet, coating it with the sauce.",
                  "Cover and simmer for 10-12 minutes until the chicken is fully cooked (internal temperature reaches 165°F/74°C).",
                  "If a thicker sauce is desired, mix cornstarch and water, then stir it into the skillet. Cook for another minute.",
                  "Sprinkle sesame seeds and chopped green onions on top.",
                  "Serve hot over steamed rice, noodles, or alongside vegetables."
              ],
              yield: "2 Servings",
              url: URL(string: "https://www.youtube.com/watch?v=gs8qfL9PNac")!),
        
        RecipeData(imageName: "appstore",
              title: "Sweet Potato",
              recipe: "In the latest installment of my Swift Beginner Series, we'll discuss UITableView and custom UITableView Cells in Swift using Xcode. UITableViews are a fundamental part of iOS Development and knowing them well is invaluable. You will build these all the time in your iOS development career.",
              TotalRecipeTime: "5",
              chef: "Ankit",
              ingredients: [
                "1 lb chicken thighs or breasts (boneless, skinless)",
                "Salt and pepper to taste",
                "1/4 cup all-purpose flour (for coating)",
                "2 tbsp butter",
                "3-4 cloves garlic, minced",
                "1/3 cup honey",
                "1/4 cup soy sauce (low-sodium preferred)",
                "2 tbsp water (optional, to adjust sauce consistency)",
                "1 tsp cornstarch (optional, mixed with 1 tbsp water for thickening)",
                "Sesame seeds for garnish (optional)",
                "Green onions, chopped for garnish (optional)"
            ],
              instructions: [
                  "Season the chicken pieces with salt and pepper.",
                  "Lightly coat the chicken in flour, shaking off excess.",
                  "Heat butter in a large skillet over medium heat.",
                  "Add the chicken and sear for 3-4 minutes on each side until golden brown. Remove and set aside.",
                  "In the same skillet, reduce heat to medium and add minced garlic. Sauté for 30 seconds until fragrant.",
                  "Stir in honey and soy sauce. (Add water if the sauce seems too thick.)",
                  "Bring the mixture to a simmer.",
                  "Return the chicken to the skillet, coating it with the sauce.",
                  "Cover and simmer for 10-12 minutes until the chicken is fully cooked (internal temperature reaches 165°F/74°C).",
                  "If a thicker sauce is desired, mix cornstarch and water, then stir it into the skillet. Cook for another minute.",
                  "Sprinkle sesame seeds and chopped green onions on top.",
                  "Serve hot over steamed rice, noodles, or alongside vegetables."
              ],
              yield: "2 Servings",
              url: URL(string: "https://www.youtube.com/watch?v=gs8qfL9PNac")!),
              
        RecipeData(imageName: "appstore",
              title: "Shahi Paneer",
              recipe: "The next topic in my series on iOS Interview questions explains the Delegate Protocol Communication Pattern in Swift. This is a fundamental question in iOS development and I was asked about it a lot during my interviews. In this tutorial I'll walk you through how the delegate protocol pattern in Swift works, using Xcode.",
              TotalRecipeTime: "5",
              chef: "Ankit",
              ingredients: [
                "1 lb chicken thighs or breasts (boneless, skinless)",
                "Salt and pepper to taste",
                "1/4 cup all-purpose flour (for coating)",
                "2 tbsp butter",
                "3-4 cloves garlic, minced",
                "1/3 cup honey",
                "1/4 cup soy sauce (low-sodium preferred)",
                "2 tbsp water (optional, to adjust sauce consistency)",
                "1 tsp cornstarch (optional, mixed with 1 tbsp water for thickening)",
                "Sesame seeds for garnish (optional)",
                "Green onions, chopped for garnish (optional)"
            ],
              instructions: [
                  "Season the chicken pieces with salt and pepper.",
                  "Lightly coat the chicken in flour, shaking off excess.",
                  "Heat butter in a large skillet over medium heat.",
                  "Add the chicken and sear for 3-4 minutes on each side until golden brown. Remove and set aside.",
                  "In the same skillet, reduce heat to medium and add minced garlic. Sauté for 30 seconds until fragrant.",
                  "Stir in honey and soy sauce. (Add water if the sauce seems too thick.)",
                  "Bring the mixture to a simmer.",
                  "Return the chicken to the skillet, coating it with the sauce.",
                  "Cover and simmer for 10-12 minutes until the chicken is fully cooked (internal temperature reaches 165°F/74°C).",
                  "If a thicker sauce is desired, mix cornstarch and water, then stir it into the skillet. Cook for another minute.",
                  "Sprinkle sesame seeds and chopped green onions on top.",
                  "Serve hot over steamed rice, noodles, or alongside vegetables."
              ],
              yield: "2 Servings",
              url: URL(string: "https://www.youtube.com/watch?v=gs8qfL9PNac")!),
        
        RecipeData(imageName: "appstore",
              title: "Gobi Manchurian",
              recipe: "I went from no programming experience to getting my first job as an iOS Developer in 7 months. In this video I explain specifically what I did to make that happen. I talk about the online courses I took as well as the developer bootcamp I attended. Many people wonder how to become an iOS Developer with no programming experience, if it's possible, and how long it takes.",
              TotalRecipeTime: "5",
              chef: "Ankit",
              ingredients: [
                "1 lb chicken thighs or breasts (boneless, skinless)",
                "Salt and pepper to taste",
                "1/4 cup all-purpose flour (for coating)",
                "2 tbsp butter",
                "3-4 cloves garlic, minced",
                "1/3 cup honey",
                "1/4 cup soy sauce (low-sodium preferred)",
                "2 tbsp water (optional, to adjust sauce consistency)",
                "1 tsp cornstarch (optional, mixed with 1 tbsp water for thickening)",
                "Sesame seeds for garnish (optional)",
                "Green onions, chopped for garnish (optional)"
            ],
              instructions: [
                  "Season the chicken pieces with salt and pepper.",
                  "Lightly coat the chicken in flour, shaking off excess.",
                  "Heat butter in a large skillet over medium heat.",
                  "Add the chicken and sear for 3-4 minutes on each side until golden brown. Remove and set aside.",
                  "In the same skillet, reduce heat to medium and add minced garlic. Sauté for 30 seconds until fragrant.",
                  "Stir in honey and soy sauce. (Add water if the sauce seems too thick.)",
                  "Bring the mixture to a simmer.",
                  "Return the chicken to the skillet, coating it with the sauce.",
                  "Cover and simmer for 10-12 minutes until the chicken is fully cooked (internal temperature reaches 165°F/74°C).",
                  "If a thicker sauce is desired, mix cornstarch and water, then stir it into the skillet. Cook for another minute.",
                  "Sprinkle sesame seeds and chopped green onions on top.",
                  "Serve hot over steamed rice, noodles, or alongside vegetables."
              ],
              yield: "2 Servings",
              url: URL(string: "https://www.youtube.com/watch?v=gs8qfL9PNac")!),
        
        RecipeData(imageName: "appstore",
              title: "Enchiladas",
              recipe: "In this video I give 37 tips to Jr. Software Engineers. Everything from getting job interviews, interacting with teammates, what language to choose, remote work, contracting, and so much more.",
              TotalRecipeTime: "5",
              chef: "Ankit",
              ingredients:[
                "1 lb chicken thighs or breasts (boneless, skinless)",
                "Salt and pepper to taste",
                "1/4 cup all-purpose flour (for coating)",
                "2 tbsp butter",
                "3-4 cloves garlic, minced",
                "1/3 cup honey",
                "1/4 cup soy sauce (low-sodium preferred)",
                "2 tbsp water (optional, to adjust sauce consistency)",
                "1 tsp cornstarch (optional, mixed with 1 tbsp water for thickening)",
                "Sesame seeds for garnish (optional)",
                "Green onions, chopped for garnish (optional)"
            ],
              instructions: [
                  "Season the chicken pieces with salt and pepper.",
                  "Lightly coat the chicken in flour, shaking off excess.",
                  "Heat butter in a large skillet over medium heat.",
                  "Add the chicken and sear for 3-4 minutes on each side until golden brown. Remove and set aside.",
                  "In the same skillet, reduce heat to medium and add minced garlic. Sauté for 30 seconds until fragrant.",
                  "Stir in honey and soy sauce. (Add water if the sauce seems too thick.)",
                  "Bring the mixture to a simmer.",
                  "Return the chicken to the skillet, coating it with the sauce.",
                  "Cover and simmer for 10-12 minutes until the chicken is fully cooked (internal temperature reaches 165°F/74°C).",
                  "If a thicker sauce is desired, mix cornstarch and water, then stir it into the skillet. Cook for another minute.",
                  "Sprinkle sesame seeds and chopped green onions on top.",
                  "Serve hot over steamed rice, noodles, or alongside vegetables."
              ],
              yield: "2 Servings",
              url: URL(string: "https://www.youtube.com/watch?v=gs8qfL9PNac")!),
        
        RecipeData(imageName: "appstore",
              title: "Pakode",
              recipe: "My technical skills as a software developer with 5 years experience are average. They're fine. Nothing special, but not bad either. However, I believe I'm a REALLY good overall software developer because of very good soft skills. In this video I wanted to discuss that topic for those developers out there who may be self-conscience about their lack (or perceived lack) of technical skills and knowledge.",
              TotalRecipeTime: "5",
              chef: "Ankit",
              ingredients: [
                "1 lb chicken thighs or breasts (boneless, skinless)",
                "Salt and pepper to taste",
                "1/4 cup all-purpose flour (for coating)",
                "2 tbsp butter",
                "3-4 cloves garlic, minced",
                "1/3 cup honey",
                "1/4 cup soy sauce (low-sodium preferred)",
                "2 tbsp water (optional, to adjust sauce consistency)",
                "1 tsp cornstarch (optional, mixed with 1 tbsp water for thickening)",
                "Sesame seeds for garnish (optional)",
                "Green onions, chopped for garnish (optional)"
            ],
              instructions: [
                  "Season the chicken pieces with salt and pepper.",
                  "Lightly coat the chicken in flour, shaking off excess.",
                  "Heat butter in a large skillet over medium heat.",
                  "Add the chicken and sear for 3-4 minutes on each side until golden brown. Remove and set aside.",
                  "In the same skillet, reduce heat to medium and add minced garlic. Sauté for 30 seconds until fragrant.",
                  "Stir in honey and soy sauce. (Add water if the sauce seems too thick.)",
                  "Bring the mixture to a simmer.",
                  "Return the chicken to the skillet, coating it with the sauce.",
                  "Cover and simmer for 10-12 minutes until the chicken is fully cooked (internal temperature reaches 165°F/74°C).",
                  "If a thicker sauce is desired, mix cornstarch and water, then stir it into the skillet. Cook for another minute.",
                  "Sprinkle sesame seeds and chopped green onions on top.",
                  "Serve hot over steamed rice, noodles, or alongside vegetables."
              ],
              yield: "2 Servings",
              url: URL(string: "https://www.youtube.com/watch?v=gs8qfL9PNac")!),
        
        RecipeData(imageName: "appstore",
              title: "Rice and Dal",
              recipe: "What I call the 90/90 Rule of Software Development usually bites new inexperienced developers in the ass. It's the concept that there's the first 90% of building the app... and then there's the second 90%. Let's talk about it.",
              TotalRecipeTime: "5",
              chef: "Ankit",
              ingredients: [
                "1 lb chicken thighs or breasts (boneless, skinless)",
                "Salt and pepper to taste",
                "1/4 cup all-purpose flour (for coating)",
                "2 tbsp butter",
                "3-4 cloves garlic, minced",
                "1/3 cup honey",
                "1/4 cup soy sauce (low-sodium preferred)",
                "2 tbsp water (optional, to adjust sauce consistency)",
                "1 tsp cornstarch (optional, mixed with 1 tbsp water for thickening)",
                "Sesame seeds for garnish (optional)",
                "Green onions, chopped for garnish (optional)"
            ],
              instructions: [
                  "Season the chicken pieces with salt and pepper.",
                  "Lightly coat the chicken in flour, shaking off excess.",
                  "Heat butter in a large skillet over medium heat.",
                  "Add the chicken and sear for 3-4 minutes on each side until golden brown. Remove and set aside.",
                  "In the same skillet, reduce heat to medium and add minced garlic. Sauté for 30 seconds until fragrant.",
                  "Stir in honey and soy sauce. (Add water if the sauce seems too thick.)",
                  "Bring the mixture to a simmer.",
                  "Return the chicken to the skillet, coating it with the sauce.",
                  "Cover and simmer for 10-12 minutes until the chicken is fully cooked (internal temperature reaches 165°F/74°C).",
                  "If a thicker sauce is desired, mix cornstarch and water, then stir it into the skillet. Cook for another minute.",
                  "Sprinkle sesame seeds and chopped green onions on top.",
                  "Serve hot over steamed rice, noodles, or alongside vegetables."
              ],
              yield: "2 Servings",
              url: URL(string: "https://www.youtube.com/watch?v=gs8qfL9PNac")!),
        
        RecipeData(imageName: "appstore",
              title: "Palak Paneer",
              recipe: "In this video I showcase the new features in Xcode 12. I am running the macOS Big Sur beta, but that is NOT required to download the Xcode 12 beta (although you must be in Apple's Developer Program to download).",
              TotalRecipeTime: "5",
              chef: "Ankit",
              ingredients:[
                "1 lb chicken thighs or breasts (boneless, skinless)",
                "Salt and pepper to taste",
                "1/4 cup all-purpose flour (for coating)",
                "2 tbsp butter",
                "3-4 cloves garlic, minced",
                "1/3 cup honey",
                "1/4 cup soy sauce (low-sodium preferred)",
                "2 tbsp water (optional, to adjust sauce consistency)",
                "1 tsp cornstarch (optional, mixed with 1 tbsp water for thickening)",
                "Sesame seeds for garnish (optional)",
                "Green onions, chopped for garnish (optional)"
            ],
              instructions: [
                  "Season the chicken pieces with salt and pepper.",
                  "Lightly coat the chicken in flour, shaking off excess.",
                  "Heat butter in a large skillet over medium heat.",
                  "Add the chicken and sear for 3-4 minutes on each side until golden brown. Remove and set aside.",
                  "In the same skillet, reduce heat to medium and add minced garlic. Sauté for 30 seconds until fragrant.",
                  "Stir in honey and soy sauce. (Add water if the sauce seems too thick.)",
                  "Bring the mixture to a simmer.",
                  "Return the chicken to the skillet, coating it with the sauce.",
                  "Cover and simmer for 10-12 minutes until the chicken is fully cooked (internal temperature reaches 165°F/74°C).",
                  "If a thicker sauce is desired, mix cornstarch and water, then stir it into the skillet. Cook for another minute.",
                  "Sprinkle sesame seeds and chopped green onions on top.",
                  "Serve hot over steamed rice, noodles, or alongside vegetables."
              ],
              yield: "2 Servings",
              url: URL(string: "https://www.youtube.com/watch?v=gs8qfL9PNac")!),
        
        RecipeData(imageName: "appstore",
              title: "Chicken Biryani",
              recipe: "This video is a compilation of the first 8 videos in my SwiftUI Fundamentals course as a free preview. In this set of videos we learn the basics of building your app with SwiftUI by creating the user interface for a standard weather app.",
              TotalRecipeTime: "5",
              chef: "Ankit",
              ingredients: [
                "1 lb chicken thighs or breasts (boneless, skinless)",
                "Salt and pepper to taste",
                "1/4 cup all-purpose flour (for coating)",
                "2 tbsp butter",
                "3-4 cloves garlic, minced",
                "1/3 cup honey",
                "1/4 cup soy sauce (low-sodium preferred)",
                "2 tbsp water (optional, to adjust sauce consistency)",
                "1 tsp cornstarch (optional, mixed with 1 tbsp water for thickening)",
                "Sesame seeds for garnish (optional)",
                "Green onions, chopped for garnish (optional)"
            ],
              instructions: [
                  "Season the chicken pieces with salt and pepper.",
                  "Lightly coat the chicken in flour, shaking off excess.",
                  "Heat butter in a large skillet over medium heat.",
                  "Add the chicken and sear for 3-4 minutes on each side until golden brown. Remove and set aside.",
                  "In the same skillet, reduce heat to medium and add minced garlic. Sauté for 30 seconds until fragrant.",
                  "Stir in honey and soy sauce. (Add water if the sauce seems too thick.)",
                  "Bring the mixture to a simmer.",
                  "Return the chicken to the skillet, coating it with the sauce.",
                  "Cover and simmer for 10-12 minutes until the chicken is fully cooked (internal temperature reaches 165°F/74°C).",
                  "If a thicker sauce is desired, mix cornstarch and water, then stir it into the skillet. Cook for another minute.",
                  "Sprinkle sesame seeds and chopped green onions on top.",
                  "Serve hot over steamed rice, noodles, or alongside vegetables."
              ],
              yield: "2 Servings",
            url: URL(string: "https://www.youtube.com/watch?v=gs8qfL9PNac")!),
    ]
}




