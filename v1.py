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
     self.items= {2:['biriyani',199,['coke','grilled_fish']],
          3: ['dosa',10 ,['chutney', 'sambar']],
          4: ['naan',15 ,['chutney', 'sambar']],
          5: ['tandoori_chicken',299, ['chutney', 'sambar']],
          6: ['chapati',12 ,['chutney', 'sambar']],
          7: ['bhel_puri',49 ,['chutney', 'sambar']],
          8: ['chutney',29, ['dosa', 'naan']],
          9: ['sambar', 29,['dosa', 'naan']],
          10: ['burger',189, ['fries', 'coke']],
          11: ['pizza',299, ['fries', 'coke']],
          12: ['sandwich', 169,['fries', 'coke']],
          13: ['pancake',196, ['fries', 'coke']],
          14: ['hotdog',99, ['fries', 'coke']],
          15: ['ice_cream',69, ['fries', 'coke']],
          16: ['cheeseburger',259, ['fries', 'coke']],
          17: ['hot_wings',299, ['fries', 'coke']],
          18: ['fries',99, ['coke', 'sauce']],
          19: ['coke',69, ['fries', 'sauce']],
          20: ['sauce',9, ['fries', 'coke']],
          21: ['sushi',198, ['fried_rice', 'pasta']],
          22: ['fried_rice',189, ['sushi', 'pasta']],
          23: ['pasta',149, ['sushi', 'fried_rice']],
          24: ['salad',99, ['steak', 'tacos']],
          25: ['steak',499, ['salad', 'tacos']],
          26: ['tacos',219, ['salad', 'steak']],
          27: ['fried_chicken',599, ['samosa', 'smoothie']],
          28: ['lassi',99, ['samosa', 'smoothie']],
          29: ['samosa',29, ['lassi', 'fried_chicken']],
          30: ['smoothie',149, ['lassi', 'samosa']],
          31: ['fruit_salad',189, ['grilled_fish', 'falafel']],
          32: ['grilled_fish',259, ['fruit_salad', 'falafel']],
          33: ['falafel',199, ['fruit_salad', 'grilled_fish']] }
     try:
       self.infofile=pd.read_csv('info.csv')
       self.df=pd.DataFrame(self.infofile)
     except pd.errors.EmptyDataError:
           print("The CSV file is empty or cannot be read.")
           return

   def login_signup(self):

      print("Welcome to Los Pollos Hermanos")
      print("Press one for sigh up ")
      choice=int(input("Press two for log in  "))
      if choice==1:
          i=0
          while i==0:
           self.username=input(str("Enter a user name must be with contain a alphabet "))
           password=input(str("Enter a password * must be with contain a alphabet "))
           search_value = self.username
           search_column ='userid'
           results = self.df[self.df[search_column] == search_value]
           if results.empty:
             with open('info.csv','a',newline='') as file:
               writer = csv.writer(file)
               newacd=[self.username,password,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
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
              print("try another one brother the user name already exisit")
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
     #billingdata=pd.DataFrame.from_dict(items, orient='index', columns=['Food Item', 'Price', 'Pairings'])

     j=1
     while j==1:
       
       code=int(input("Enter the item code "))
       if code==0:
          break
       quantity=int(input("enter the quantity "))
       print("Press 0(ZERO) to Bill the items ")
       if code in self.puchasedItem:
         self.puchasedItem[code][2]+=quantity
         self.totalPrice+=self.puchasedItem[code][1]*quantity
       else:
          self.puchasedItem[code] =[self.items[code][0], self.items[code][1], code,quantity]
          self.totalPrice+=quantity*self.puchasedItem[code][1]
       for key in self.puchasedItem:
          print(f"item purchased  : {self.puchasedItem[key][0]:<10} |price {self.puchasedItem[key][1]:<4}| quatity {self.puchasedItem[key][2]} |Rs {self.puchasedItem[key][1]*self.puchasedItem[key][2]}")
       print( f"TOTAL Rs : {self.totalPrice}") 
     
     for i in self.puchasedItem:
                item_code = self.puchasedItem[i][2]
                quantity_purchased = self.puchasedItem[i][3]
                food_item_name = self.items[item_code][0]
                self.df.loc[self.df['userid'] == self.username, food_item_name] += quantity_purchased
                self.df.to_csv('info.csv', index=False)
                print("Thank you for shopping with us")
           
          

   def display_menu(self,ON,dataf):
     print("Los Pollos Hermanos")
     if ON==False:
       p="c"
       for key in self.items:
          print(f"item code : {key:>2}   | item name : {self.items[key][0]:<17} | price : {self.items[key][1]:>4}")
          if key==19:
            p="f"
            print("pree c to see more items   ")
            print("press any key to continue")
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
        print(f"ALWAYS BUY {Pmax_item}")
        item_columns = self.df.columns[2:]
        max_item = self.df[item_columns].max().idxmax()
        print(f"MOST POPULR {max_item} ")
        for key in self.items:
          print(f"item code : {key:>2}   | item name : {self.items[key][0]:<17} | price : {self.items[key][1]:>4}")
          if key==19:
            p="f"
            print("pree c to seeing more items   ")
            print("press any other not to see")
            p=input()

            if p=="c":
              continue
            else:
              self.fooditems_rec()
        print("-" * 60)
        self.fooditems_rec()


        
   def recommend_items(self):
       # Step 1: Create user-item matrix
       user_item_matrix = self.df.iloc[:, 2:].values  # Selecting columns related to food items
       
       #Step 2: Apply SVD
       svd = TruncatedSVD(n_components=5, random_state=42)  # 5 components for the reduced matrix
       reduced_matrix = svd.fit_transform(user_item_matrix)
       
       # Step 3: Calculate predictions
       predicted_matrix = np.dot(reduced_matrix, svd.components_)
       
       # Step 4: Recommend items based on the predicted scores
       user_index = self.df[self.df['userid'] == self.username].index[0]
       predicted_scores = predicted_matrix[user_index, :]
       
       # Sort the items based on predicted scores
       sorted_item_indices = np.argsort(predicted_scores)[::-1]
       
       # Display top N recommendations (for simplicity, top 5)
       print("Recommended Items for you:")
       top_n = 10
       for idx in sorted_item_indices[:top_n]:
          print(f"{self.df.columns[idx+2]:<20} | Predicted Score: {predicted_scores[idx]:>6 }")

obj=restrec()
obj.login_signup()




