from sklearn.decomposition import TruncatedSVD
import pandas as pd
import numpy as np
import csv
import os

class restrec:
   def __init__(self):
     self.totalPrice=0
     self.puchasedItem={}
     self.username=""
     self.items= {2:['biriyani',199,[['coke',19],['grilled_fish',32]]],
          3: ['dosa',10 ,[['chutney',8],['sambar',9]]],
          4: ['naan',15 ,[['chutney',8],['sambar',9]]],
          5: ['tandoori_chicken',299],
          6: ['chapati',12 ,[['chicken curry',26],['sambar',9]]],
          7: ['bhel_puri',49 ,[['chutney',8],['sambar',9]]],
          8: ['chutney',29],
          9: ['sambar', 29],
          10: ['burger',189, [['fries',18],['coke',19]]],
          11: ['pizza',299, [['fries',18],['coke',19]]],
          12: ['sandwich', 169,[['fries',18],['coke',19]]],
          13: ['pancake',196],
          14: ['hotdog',99],
          15: ['ice_cream',69],
          16: ['cheeseburger',259,[['fries',18],['coke',19]]],
          17: ['hot_wings',299,[['fries',18],['coke',19]]],
          18: ['fries',99,[['sauce',20],['coke',19]]],
          19: ['coke',69],
          20: ['sauce',9],
          21: ['sushi',198],
          22: ['fried_rice',189,[['sauce',20],['coke',19]]],
          23: ['pasta',149,[['sauce',20],['coke',19]]],
          24: ['salad',99],
          25: ['steak',499,[['sauce',20],['coke',19]]],
          26: ['chicken curry',219 ],
          27: ['fried_chicken',599,[['sauce',20],['coke',19]]],
          28: ['lassi',99],
          29: ['samosa',29],
          30: ['smoothie',149],
          31: ['fruit_salad',189],
          32: ['grilled_fish',259,[['sauce',20],['coke',19]]],
          33: ['falafel',90] ,
          34: ['shawarma',159],
          35: ['Alfam',449,[['Kuboos',38],['coke',19]]],
          36: ['Kabsa',399],
          37: ['Mandi',799],
          38: ['Kuboos',15],
          39: ['Kabab',199]}
     try:
       self.infofile=pd.read_csv('info.csv')
       self.df=pd.DataFrame(self.infofile)
     except pd.errors.EmptyDataError:
           print("The CSV file is empty or cannot be read Check the csv .")
           return

   def login_signup(self):

      print("Welcome to Los Pollos Hermanos")
      print("_______________________________")
      print("Press one for Sign up ")
      choice=int(input("Press two for Log in "))
      if choice==1:
          i=0
          while i==0:
           self.username=input(str("Enter a user name "))
           password=input(str("Enter a password  "))
           search_value = self.username
           search_column ='userid'
           results = self.df[self.df[search_column] == search_value]
           if results.empty:
             with open('info.csv','a',newline='') as file:
               writer = csv.writer(file)
               newacd=[self.username,password,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
               writer.writerow(newacd)
             self.infofile=pd.read_csv('info.csv')
             self.df=pd.DataFrame(self.infofile)
             i=1
             print("Your success fully signed up into Los Pollos Hermanos")
             results = self.df[self.df[search_column] == search_value]
             os.system('cls')
             self.display_menu(False,results)
               
              
             break
           else: 
              
              print("try another  user name already exisit")
      else:
        o=0
        while o==0:
         search_value=str(input("enter your user name  "))
         self.username=search_value
         search_column='userid'
         results = self.df[self.df[search_column] == search_value]
         if  results.empty:
            print("The user name does not exist try again")

         else :
            password=str(input("enter your password  "))
            if results.iloc[0]['password']==password:
              os.system('cls')
              self.display_menu(True,results)
              break
            else:
               print("wrong password try again")


   def fooditems_rec(self):
     j=1
     while j==1:
       code=int(input("Enter the item code "))
       if code==0:
          j=5
          break
       if code not in self.items:
          print("invalid code")
          
       quantity=int(input("enter the quantity "))
       #sub rec
       if len(self.items[code])>2:
          print("would you like to add combo of the item")
          for i in range(len(self.items[code][2])):
            print(f"{i+1} {self.items[code][2][i][0]:<14} code :{self.items[code][2][i][1]:<4} price : {self.items[self.items[code][2][i][1]][1]:<6}")
          z=input("press y to add the combo ")
          if z=="y":
           for i in range(len(self.items[code][2])):
            
               subcode=self.items[code][2][i][1]
               subquan=1
               if subcode in self.puchasedItem:
                    self.puchasedItem[subcode][2]+=subquan
                    self.totalPrice+=self.puchasedItem[subcode][1]*subquan
               else:
                    self.puchasedItem[subcode] =[self.items[subcode][0], self.items[subcode][1], subcode,subquan]
                    self.totalPrice+=subquan*self.puchasedItem[subcode][1]
               item_code = self.puchasedItem[subcode][2]
               quantity_purchased = self.puchasedItem[subcode][3]
               food_item_name = self.items[item_code][0]
               self.df.loc[self.df['userid'] == self.username, food_item_name] += quantity_purchased     
       #main item merge to cart
       if code in self.puchasedItem:
         self.puchasedItem[code][2]+=quantity
         self.totalPrice+=self.puchasedItem[code][1]*quantity
       else:
          self.puchasedItem[code] =[self.items[code][0], self.items[code][1], code,quantity]
          self.totalPrice+=quantity*self.puchasedItem[code][1]
       item_code = self.puchasedItem[code][2]
       quantity_purchased = self.puchasedItem[code][3]
       food_item_name = self.items[item_code][0]
       self.df.loc[self.df['userid'] == self.username, food_item_name] += quantity_purchased       
       os.system('cls')
       self.recommend_items()    
       print("Press 0(ZERO) to Checkout ")
      
       for key in self.puchasedItem:
          print(f"                                     item purchased  : {self.puchasedItem[key][0]:<10} |price {self.puchasedItem[key][1]:<4}| quatity {self.puchasedItem[key][3]} |Rs {self.puchasedItem[key][1]*self.puchasedItem[key][3]}")
       print( f"                                     TOTAL Rs : {self.totalPrice}") 

     self.df.to_csv('info.csv', index=False)
     print("Thank you for shopping with us   ")
     print("______________________________")
     print()
           
          

   def display_menu(self,ON,dataf):
     print("Los Pollos Hermanos")
     if ON==False:
       p="c"
       for key in self.items:
          print(f"item code : {key:>2}   | item name : {self.items[key][0]:<17} | price : {self.items[key][1]:>4}")
          if key==19:
            p="f"
            print("pree c to see more items   ")
            print("Just press ENTER skip")
            p=input()
            if p=="c":
              continue
            else:
              self.fooditems_rec()
              return
       self.fooditems_rec()
     else:
        self.recommend_items()
        item_columns = dataf.columns[2:]
        Pmax_item = dataf[item_columns].max().idxmax()
        print("Recommendations : ")
       # print(f"ALWAYS BUY {Pmax_item}")
        item_columns = self.df.columns[2:]
        max_item = self.df[item_columns].max().idxmax()
        print(f"MOST POPULR {max_item} ")
        for key in self.items:
          print(f"item code : {key:>2}   | item name : {self.items[key][0]:<17} | price : {self.items[key][1]:>4}")
          if key==19:
            p="f"
            print("pree c to seeing more items   ")
            print("Just press ENTER skip")
            p=input()

            if p=="c":
                 pass
            if p=="f":
              self.fooditems_rec()
              break
            
        print("-" * 60)
        self.fooditems_rec()

# ---------- Recommendation Logic ----------
    
   def recommend_items(self):

    # Reload the latest info.csv to capture new data
    self.df = pd.read_csv("info.csv")

    user_item_matrix = self.df.iloc[:, 2:].values

    svd = TruncatedSVD(n_components=5, random_state=42)
    reduced_matrix = svd.fit_transform(user_item_matrix)
    predicted_matrix = np.dot(reduced_matrix, svd.components_)

    user_index = self.df[self.df['userid'] == self.username].index[0]
    predicted_scores = predicted_matrix[user_index, :]

    sorted_item_indices = np.argsort(predicted_scores)[::-1]

    top_n = 5
    recommendations = []

    for idx in sorted_item_indices[:top_n]:
        col_name = self.df.columns[idx + 2]  # Skip userid and password
        for code in self.items:
            name = self.items[code][0]
            price = self.items[code][1]
            if name.lower() == col_name.lower():
                recommendations.append({
                    "name": name,
                    "price": price
                })
                break

    return recommendations 

# Entry point for standalone use (terminal-based)
def main():
    while True:
        obj = restrec()
        obj.login_signup()

# Safe import: only runs when executing v1.py directly
if __name__ == "__main__":
    main()

# Used by Flask app (web_app.py)
def recommend(username):
    # TODO: use real logic based on user's row in info.csv
    return ["Coke", "Fries"]