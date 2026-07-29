# price_quantity_total candidate review

候选总数：150

当前展示前 30 条，用于人工抽查。

## 1. gsm8k_train_04493

### Categories

price_quantity_total

### Scores

```json
{
  "price_quantity_total": 8
}
```

### Match reasons

```json
{
  "price_quantity_total": [
    "contains_money_signal",
    "contains_transaction_signal",
    "contains_unit_price_relation",
    "contains_payment_or_change_relation",
    "multi_step_calculation"
  ]
}
```

### Problem

Jane bought 2 skirts for $13 each. She also bought 3 blouses for $6 each. She paid the cashier $100. How much change did she receive?

### Response

```text
The 2 skirts cost $13 x 2 = $26.
The 3 blouses cost $6 x 3 = $18.
The total cost for 2 skirts and 3 blouses is $26 + $18 = $44.
Jane received $100 - $44 = $56 change.
#### 56
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 2. gsm8k_train_02018

### Categories

price_quantity_total

### Scores

```json
{
  "price_quantity_total": 8
}
```

### Match reasons

```json
{
  "price_quantity_total": [
    "contains_money_signal",
    "contains_transaction_signal",
    "contains_unit_price_relation",
    "contains_payment_or_change_relation",
    "multi_step_calculation"
  ]
}
```

### Problem

Jed’s family wants to buy 6 different board games. Each board game costs $15 and Jed paid using a $100 bill. If the cashier gave Jed only $5 bills for his change, how many bills did Jed receive?

### Response

```text
Jed paid $15 x 6 = $90 for the 6 board games.
He has $100 - $90 = $10 change.
Therefore, Jed received$ 10/$5 = 2 $5 bills.
#### 2
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 3. gsm8k_train_05505

### Categories

price_quantity_total, remaining_change

### Scores

```json
{
  "price_quantity_total": 8,
  "remaining_change": 5
}
```

### Match reasons

```json
{
  "price_quantity_total": [
    "contains_money_signal",
    "contains_transaction_signal",
    "contains_unit_price_relation",
    "contains_payment_or_change_relation",
    "multi_step_calculation"
  ],
  "remaining_change": [
    "contains_quantity_change",
    "contains_sequence_or_relation",
    "multi_step_calculation",
    "three_or_more_operations"
  ]
}
```

### Problem

Thomas owns 200 books. He decides to sell them and use the money to buy records. Each book sells for $1.5. A record costs $3. If he buys 75 records, how much money does he have left over?

### Response

```text
He makes $300 selling the books because 200 x 1.5 = 300
He spends $225 on records because 75 x 3 = 225
He has $75 left because 300 - 225 = 75
#### 75
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 4. gsm8k_train_02804

### Categories

price_quantity_total, remaining_change

### Scores

```json
{
  "price_quantity_total": 8,
  "remaining_change": 4
}
```

### Match reasons

```json
{
  "price_quantity_total": [
    "contains_money_signal",
    "contains_transaction_signal",
    "contains_unit_price_relation",
    "contains_payment_or_change_relation",
    "multi_step_calculation"
  ],
  "remaining_change": [
    "contains_quantity_change",
    "contains_sequence_or_relation",
    "multi_step_calculation"
  ]
}
```

### Problem

Todd has $20. He buys 4 candy bars that cost $2 each. How much money in dollars does Todd have left?

### Response

```text
The candy bars cost 4*2= $8.
Todd has 20-8= $12 left.
#### 12
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 5. gsm8k_train_00240

### Categories

price_quantity_total

### Scores

```json
{
  "price_quantity_total": 8
}
```

### Match reasons

```json
{
  "price_quantity_total": [
    "contains_money_signal",
    "contains_transaction_signal",
    "contains_unit_price_relation",
    "contains_payment_or_change_relation",
    "multi_step_calculation"
  ]
}
```

### Problem

Frank has 7 one-dollar bills, 4 five-dollar bills, 2 ten-dollar bills, and 1 twenty-dollar bill. He goes to buy peanuts, which cost $3 a pound. He buys what he wants and has $4 in change. He plans to eat the peanuts all in one week. How many pounds does he eat on average per day?

### Response

```text
Frank has $7 in one dollar bills because 7 x 1 = 7
Frank has $20 in five dollar bills because 4 x 5 = 20
Frank has $20 in ten dollar bills because 2 x 10 = 20
Frank has 67 dollars in total because 7 + 20 + 20 + 20 = 67
Frank spent $63 because 67 - 4 = 63
Frank bought 21 pounds of peanuts because 63 / 3 = 21
He eats 3 pounds a day on average because 21 / 7 = 3
#### 3
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 6. gsm8k_train_01927

### Categories

price_quantity_total

### Scores

```json
{
  "price_quantity_total": 8
}
```

### Match reasons

```json
{
  "price_quantity_total": [
    "contains_money_signal",
    "contains_transaction_signal",
    "contains_unit_price_relation",
    "contains_payment_or_change_relation",
    "multi_step_calculation"
  ]
}
```

### Problem

James buys 10 boxes of Capri-sun.  Each box has 6 pouches in it.  If he paid $12 how many cents does each pouch cost?

### Response

```text
He bought 10*6=60 pouches
It cost 12*100=1200 cents
So each pouch cost 1200/60=20 cents
#### 20
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 7. gsm8k_train_02847

### Categories

price_quantity_total, remaining_change

### Scores

```json
{
  "price_quantity_total": 8,
  "remaining_change": 5
}
```

### Match reasons

```json
{
  "price_quantity_total": [
    "contains_money_signal",
    "contains_transaction_signal",
    "contains_unit_price_relation",
    "contains_payment_or_change_relation",
    "multi_step_calculation"
  ],
  "remaining_change": [
    "contains_quantity_change",
    "contains_sequence_or_relation",
    "multi_step_calculation",
    "three_or_more_operations"
  ]
}
```

### Problem

Chris wanted to buy a new video game that costs $60 as well as an assortment of candy that costs $5.  To earn the money, he agreed to babysit his little sister for $8 per hour.  If he works 9 hours, how much money will be left over after he makes his purchases?

### Response

```text
He wants to buy a $60 game and $5 of candy so 60 + 5 = $65
He will make $8 per hour of babysitting and will work 9 hours so 8 * 9 = $72
He made $72 and spent $65 so 72-65 = $7 left over
#### 7
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 8. gsm8k_train_07115

### Categories

price_quantity_total

### Scores

```json
{
  "price_quantity_total": 8
}
```

### Match reasons

```json
{
  "price_quantity_total": [
    "contains_money_signal",
    "contains_transaction_signal",
    "contains_unit_price_relation",
    "contains_payment_or_change_relation",
    "multi_step_calculation"
  ]
}
```

### Problem

John buys 3 barbells and gives $850 and gets $40 in change.  How much did each barbell cost?

### Response

```text
The total price of the barbells was 850-40=$810
So each one cost 810/3=$270
#### 270
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 9. gsm8k_train_03016

### Categories

price_quantity_total, remaining_change

### Scores

```json
{
  "price_quantity_total": 8,
  "remaining_change": 5
}
```

### Match reasons

```json
{
  "price_quantity_total": [
    "contains_money_signal",
    "contains_transaction_signal",
    "contains_unit_price_relation",
    "contains_payment_or_change_relation",
    "multi_step_calculation"
  ],
  "remaining_change": [
    "contains_quantity_change",
    "contains_sequence_or_relation",
    "multi_step_calculation",
    "three_or_more_operations"
  ]
}
```

### Problem

Sam has 19 dimes and 6 quarters. She buys 4 candy bars for 3 dimes each and 1 lollipop for 1 quarter. How much money, in cents, does she have left?

### Response

```text
The candy bars cost 4*3=12 dimes.
Sam has 19-12=7 dimes left.
Sam has 6-1=5 quarters left.
Sam has 7*10+5*25=195 cents left.
#### 195
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 10. gsm8k_train_02895

### Categories

price_quantity_total, remaining_change

### Scores

```json
{
  "price_quantity_total": 8,
  "remaining_change": 4
}
```

### Match reasons

```json
{
  "price_quantity_total": [
    "contains_money_signal",
    "contains_transaction_signal",
    "contains_unit_price_relation",
    "contains_payment_or_change_relation",
    "multi_step_calculation"
  ],
  "remaining_change": [
    "contains_quantity_change",
    "contains_sequence_or_relation",
    "multi_step_calculation"
  ]
}
```

### Problem

Ian spent half the money he made on doing online surveys. If he worked 8 hours doing surveys and on average he's able to earn $18 per hour doing surveys, how much money does he have left?

### Response

```text
Ian is able to earn $18 per hour doing surveys. If he worked 8 hours doing surveys, then he earned $18*8 = $144
If he spent half of what he earned, then he spent $144 * 50% = $72
If Ian spent $72 of his earnings, then he has $144 - $72 = $72 left
#### 72
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 11. gsm8k_train_05007

### Categories

price_quantity_total

### Scores

```json
{
  "price_quantity_total": 8
}
```

### Match reasons

```json
{
  "price_quantity_total": [
    "contains_money_signal",
    "contains_transaction_signal",
    "contains_unit_price_relation",
    "contains_payment_or_change_relation",
    "multi_step_calculation"
  ]
}
```

### Problem

James buys 3 packs of candy.  He pays with a $20 bill and gets $11 change.  How much did each pack of candy cost?

### Response

```text
The candy cost 20-11=$9
So he pays 9/3=$3 per candy
#### 3
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 12. gsm8k_train_04771

### Categories

price_quantity_total, remaining_change

### Scores

```json
{
  "price_quantity_total": 8,
  "remaining_change": 4
}
```

### Match reasons

```json
{
  "price_quantity_total": [
    "contains_money_signal",
    "contains_transaction_signal",
    "contains_unit_price_relation",
    "contains_payment_or_change_relation",
    "multi_step_calculation"
  ],
  "remaining_change": [
    "contains_quantity_change",
    "contains_sequence_or_relation",
    "multi_step_calculation"
  ]
}
```

### Problem

Ed booked a hotel while he was on vacation. Staying at the hotel cost was $1.50 per hour every night and $2 per hour every morning. If Ed had $80 and he stayed in the hotel for 6 hours last night and 4 hours this morning, how much money was he left with after paying for his stay at the hotel?

### Response

```text
Ed spent $1.50 x 6 = $9 for staying in the hotel last night.
He spent $2 x 4 = $8 for staying in the hotel this morning
So, the total money he spent in the hotel is $9 + $8 = $17.
Therefore, he still has $80 - $17 = $63 left after staying in the hotel.
#### 63
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 13. gsm8k_train_06913

### Categories

price_quantity_total

### Scores

```json
{
  "price_quantity_total": 8
}
```

### Match reasons

```json
{
  "price_quantity_total": [
    "contains_money_signal",
    "contains_transaction_signal",
    "contains_unit_price_relation",
    "contains_payment_or_change_relation",
    "multi_step_calculation"
  ]
}
```

### Problem

Sam is stocking up on canned tuna. He got 9 cans at the supermarket, and had 5 coupons for 25 cents off a single can per coupon. He paid $20 and got $5.50 in change. How many cents does a can of tuna cost?

### Response

```text
His total without the coupons was $20 - $5.50 = $14.50
He had 5 coupons that each saved him 25 cents, so the full price of all the tuna is $14.50 + 5*$0.25 =$15.75.
He bought 9 cans of tuna, so each can costs $15.75 / 9 = $1.75
As 1 dollar has 100 cents 1.75 * 100 = 175 cents
#### 175
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 14. gsm8k_train_02784

### Categories

price_quantity_total

### Scores

```json
{
  "price_quantity_total": 8
}
```

### Match reasons

```json
{
  "price_quantity_total": [
    "contains_money_signal",
    "contains_transaction_signal",
    "contains_unit_price_relation",
    "contains_payment_or_change_relation",
    "multi_step_calculation"
  ]
}
```

### Problem

Jude bought three chairs for his house, all at the same price. He also bought a table that costs $50 and two sets of plates at $20 for each set. After giving the cashier $130, Jude got a $4 change. How much did each of the chairs cost?

### Response

```text
The two sets of plates amount to $20 x 2 = $40.
So the table and the two sets of plates amount to $50 + $40 = $90 in all.
Since Jude received a $4 change, then he paid a total of $130 - $4 = $126 for the chairs, tables, and plates.
Thus, the three chairs cost $126 - $90 = $36.
Therefore, each chair cost $36/3 = $12.
#### 12
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 15. gsm8k_train_02235

### Categories

price_quantity_total, remaining_change

### Scores

```json
{
  "price_quantity_total": 8,
  "remaining_change": 5
}
```

### Match reasons

```json
{
  "price_quantity_total": [
    "contains_money_signal",
    "contains_transaction_signal",
    "contains_unit_price_relation",
    "contains_payment_or_change_relation",
    "multi_step_calculation"
  ],
  "remaining_change": [
    "contains_quantity_change",
    "contains_sequence_or_relation",
    "multi_step_calculation",
    "three_or_more_operations"
  ]
}
```

### Problem

Susie babysits every day for 3 hours a day at the rate of $10 per hour. She spent 3/10 of the money she earned from last week to buy a make-up set. She then spent 2/5 of her money on her skincare products. How much is left from her earnings last week, in dollars?

### Response

```text
Susie earned $10 x 3 = $30 per day.
Last week, she earned a total of $30 x 7 = $210.
She spent $210 x 3/10 = $63 on make-up.
While she spent $210 x 2/5 = $84 on her skincare products.
Thus, she spent a total of $63 + $84 = $147 from her earnings.
Therefore, Susie is left with $210 - $147 = $63 from her earnings last week.
#### 63
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 16. gsm8k_train_07307

### Categories

price_quantity_total

### Scores

```json
{
  "price_quantity_total": 8
}
```

### Match reasons

```json
{
  "price_quantity_total": [
    "contains_money_signal",
    "contains_transaction_signal",
    "contains_unit_price_relation",
    "contains_payment_or_change_relation",
    "multi_step_calculation"
  ]
}
```

### Problem

Roxanne bought 2 cups of lemonade for $2 each and 2 sandwiches for $2.50 each. How much change must she get from a $20 bill?

### Response

```text
Two cups of lemonade amount to $2 x 2 = $4.
Two sandwiches amount to $2.50 x 2 = $5.
So, the total amount that Roxanne had to pay was $4 + $5 = $9.
Thus, her change must be $20 - $9 = $11.
#### 11
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 17. gsm8k_train_02789

### Categories

price_quantity_total, remaining_change

### Scores

```json
{
  "price_quantity_total": 8,
  "remaining_change": 4
}
```

### Match reasons

```json
{
  "price_quantity_total": [
    "contains_money_signal",
    "contains_transaction_signal",
    "contains_unit_price_relation",
    "contains_payment_or_change_relation",
    "multi_step_calculation"
  ],
  "remaining_change": [
    "contains_quantity_change",
    "contains_sequence_or_relation",
    "multi_step_calculation"
  ]
}
```

### Problem

Dr. Jones earns $6,000 a month. His house rental is $640 each month; his monthly food expense is $380; his electric and water bill costs 1/4 of what he makes, and his insurances cost 1/5 of what he makes. How much money does he have left after paying those four bills?

### Response

```text
Dr. Jones pays $6000 / 4 =$ 1500 for his electric and water bill.
He pays $6000 / 5 = $1200 for his insurances.
The total amount he pays for the bills and insurances is $1500 + $1200 = $2700.
The remaining money from his earning after paying off the bills and insurance is $6000 - $2700 = $3300.
The total amount he needs to pay for the rent and food expenses is $640 + $380 = $1020.
So, Dr. Jones has $3300 - $1020 = $2280 left
#### 2280
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 18. gsm8k_train_04200

### Categories

price_quantity_total, remaining_change

### Scores

```json
{
  "price_quantity_total": 8,
  "remaining_change": 5
}
```

### Match reasons

```json
{
  "price_quantity_total": [
    "contains_money_signal",
    "contains_transaction_signal",
    "contains_unit_price_relation",
    "contains_payment_or_change_relation",
    "multi_step_calculation"
  ],
  "remaining_change": [
    "contains_quantity_change",
    "contains_sequence_or_relation",
    "multi_step_calculation",
    "three_or_more_operations"
  ]
}
```

### Problem

Jenn is saving up money to buy a bike. She has 5 jars full of quarters. Each jar can hold 160 quarters. If the bike costs 180 dollars, how much money will she have left over after buying it?

### Response

```text
Jenn has 5 * 160 = 800 quarters.
The quarters are worth 800 * 0.25 = 200 dollars.
After buying the bike she will have 200 - 180 = 20 dollars left.
#### 20
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 19. gsm8k_train_06688

### Categories

price_quantity_total

### Scores

```json
{
  "price_quantity_total": 8
}
```

### Match reasons

```json
{
  "price_quantity_total": [
    "contains_money_signal",
    "contains_transaction_signal",
    "contains_unit_price_relation",
    "contains_payment_or_change_relation",
    "multi_step_calculation"
  ]
}
```

### Problem

John goes to the store and pays with a 20 dollar bill.  He buys 3 sodas and gets $14 in change.  How much did each soda cost?

### Response

```text
He paid 20-14=$6
So each soda cost 6/3=$2
#### 2
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 20. gsm8k_train_03445

### Categories

price_quantity_total, remaining_change

### Scores

```json
{
  "price_quantity_total": 8,
  "remaining_change": 5
}
```

### Match reasons

```json
{
  "price_quantity_total": [
    "contains_money_signal",
    "contains_transaction_signal",
    "contains_unit_price_relation",
    "contains_payment_or_change_relation",
    "multi_step_calculation"
  ],
  "remaining_change": [
    "contains_quantity_change",
    "contains_sequence_or_relation",
    "multi_step_calculation",
    "three_or_more_operations"
  ]
}
```

### Problem

Josie's mom gave her a $20 bill and asked her to go to the store for a few items.  The list included a carton of milk for $4.00, a loaf of bread for $3.50, a box of laundry detergent for $10.25 and 2 pounds of bananas that were $0.75 per pound.  Her mom also gave her a coupon for $1.25 off of the laundry detergent.  At checkout, the clerk told her the milk was 1/2 off today.  How much money did Josie have left over after she bought all of the groceries?

### Response

```text
The milk cost $4.00 but was on sale for 1/2 off so 4*.50 = $2.00
She bought 2 pounds of bananas at $0.75 per pound so 2 *.75 = $1.50
She had a $1.25 coupon off of laundry detergent so 10.25 - 1.25 = $9.00
When you add all of her purchases together then 2 + 1.50 +3.50 + 9.00 = $16.00
She paid with a $20 bill so 20-16 = $4 left over
#### 4
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 21. gsm8k_train_00179

### Categories

percentage_fraction, price_quantity_total

### Scores

```json
{
  "percentage_fraction": 4,
  "price_quantity_total": 8
}
```

### Match reasons

```json
{
  "percentage_fraction": [
    "strong_percentage_or_fraction_signal",
    "multi_step_calculation"
  ],
  "price_quantity_total": [
    "contains_money_signal",
    "contains_transaction_signal",
    "contains_unit_price_relation",
    "contains_payment_or_change_relation",
    "multi_step_calculation"
  ]
}
```

### Problem

Simon wanted to buy flowers that his mom could plant for Mother's Day.  The garden center was offering 10% off all purchases.  He bought 5 pansies at $2.50 each, one hydrangea that cost $12.50 and 5 petunias that cost $1.00 each.  If he paid with a $50 bill, how much change would Simon receive back from his purchase?

### Response

```text
5 pansies at $2.50 each is 5*2.50 = $12.50
5 petunias at $1.00 each 5*1 = $5.00
All total he spends 12.50+12.50+5.00 = $30.00
The sale is 10% off so 30*.10 = $3.00
The purchase total now comes to 30-3 = $27.00
He pays with a $50 bill so 50-27 = $23.00
#### 23
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 22. gsm8k_train_06877

### Categories

price_quantity_total, remaining_change

### Scores

```json
{
  "price_quantity_total": 8,
  "remaining_change": 5
}
```

### Match reasons

```json
{
  "price_quantity_total": [
    "contains_money_signal",
    "contains_transaction_signal",
    "contains_unit_price_relation",
    "contains_payment_or_change_relation",
    "multi_step_calculation"
  ],
  "remaining_change": [
    "contains_quantity_change",
    "contains_sequence_or_relation",
    "multi_step_calculation",
    "three_or_more_operations"
  ]
}
```

### Problem

Selena got a tip today that amounted to $99. She pampered herself by eating at a 5-star hotel. She indulged herself with 2 steak meals that cost $24 each plate. She also ordered 2 types of burgers which cost $3.5 each, and 3 cups of ice cream which cost $2 each. How much money will Selena be left with?

### Response

```text
Selena was charged $24 x 2 = $48 for the steaks.
She was charged $3.5 x 2 = $7 for the burgers.
She was charged $2 x 3 = $6 for the cups of ice cream.
She was charged $48 + $7 + $6 = $61 in total.
Therefore, Selena was left with $99 - $61 = $38.
#### 38
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 23. gsm8k_train_05703

### Categories

price_quantity_total

### Scores

```json
{
  "price_quantity_total": 8
}
```

### Match reasons

```json
{
  "price_quantity_total": [
    "contains_money_signal",
    "contains_transaction_signal",
    "contains_unit_price_relation",
    "contains_payment_or_change_relation",
    "multi_step_calculation"
  ]
}
```

### Problem

Donny went to the gas station to gas up his tank. He knows his truck holds 150 liters of fuel. His truck already contained 38 liters. How much change will he get from $350 if each liter of fuel costs $3?

### Response

```text
He needs 150 - 38 = 112 liters more to have a full tank of gas.
Donny will pay 112 x $3 = $336 for a full tank of gas.
His will get $350 - $336 = $14 change."
#### 14
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 24. gsm8k_train_03842

### Categories

price_quantity_total

### Scores

```json
{
  "price_quantity_total": 8
}
```

### Match reasons

```json
{
  "price_quantity_total": [
    "contains_money_signal",
    "contains_transaction_signal",
    "contains_unit_price_relation",
    "contains_payment_or_change_relation",
    "multi_step_calculation"
  ]
}
```

### Problem

Laura bought 2 pairs of pants for $54 each and 4 shirts for $33 each. She gave $250 to the cashier. So how much change did she take?

### Response

```text
54*2=$108 is the price of 2 pairs of pants.
4*33=$132 is the price of 4 shirts.
108+132=$240 is the total price.
So the cashier gave 250-240=$10 change to Laura.
#### 10
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 25. gsm8k_train_05072

### Categories

price_quantity_total, remaining_change

### Scores

```json
{
  "price_quantity_total": 8,
  "remaining_change": 5
}
```

### Match reasons

```json
{
  "price_quantity_total": [
    "contains_money_signal",
    "contains_transaction_signal",
    "contains_unit_price_relation",
    "contains_payment_or_change_relation",
    "multi_step_calculation"
  ],
  "remaining_change": [
    "contains_quantity_change",
    "contains_sequence_or_relation",
    "multi_step_calculation",
    "three_or_more_operations"
  ]
}
```

### Problem

A football club has a balance of $100 million. The club then sells 2 of its players at $10 million each, and buys 4 more at $15 million each. How much money is left in the club register in millions of dollars?

### Response

```text
The 2 players are sold for a total of 2*10 = $20 million
So the club has 100 + 20 = $120 million
The cost of buying 4 more players at $15 million each is 4*15 = $60 million
So the club now has 120 – 60 = $60 million
#### 60
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 26. gsm8k_train_02125

### Categories

percentage_fraction, price_quantity_total, remaining_change

### Scores

```json
{
  "percentage_fraction": 4,
  "price_quantity_total": 8,
  "remaining_change": 5
}
```

### Match reasons

```json
{
  "percentage_fraction": [
    "strong_percentage_or_fraction_signal",
    "multi_step_calculation"
  ],
  "price_quantity_total": [
    "contains_money_signal",
    "contains_transaction_signal",
    "contains_unit_price_relation",
    "contains_payment_or_change_relation",
    "multi_step_calculation"
  ],
  "remaining_change": [
    "contains_quantity_change",
    "contains_sequence_or_relation",
    "multi_step_calculation",
    "three_or_more_operations"
  ]
}
```

### Problem

James earns $10 per week as an allowance. After saving all his money for four weeks, he spends half of it on a new video game. He then spends a quarter of what is left to buy a new book. How much money does he have left?

### Response

```text
He starts out with $10 * 4 = $40.
James spend $40 / 2 = $20 on the video game.
After buying the game, he has $40 - $20 = $20 left.
He spent $20 / 4 = $5 on the book.
He has $20 - $5 = $15 left.
#### 15
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 27. gsm8k_train_03963

### Categories

price_quantity_total

### Scores

```json
{
  "price_quantity_total": 8
}
```

### Match reasons

```json
{
  "price_quantity_total": [
    "contains_money_signal",
    "contains_transaction_signal",
    "contains_unit_price_relation",
    "contains_payment_or_change_relation",
    "multi_step_calculation"
  ]
}
```

### Problem

Lucas went to the store with $20 and needed to buy 3 avocados that cost $2 each. How much change does he bring home?

### Response

```text
The avocados cost 6 because 3 x 2 = 6
He brings home $4 in change because 20 - 6 =14
#### 14
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 28. gsm8k_train_01188

### Categories

price_quantity_total

### Scores

```json
{
  "price_quantity_total": 8
}
```

### Match reasons

```json
{
  "price_quantity_total": [
    "contains_money_signal",
    "contains_transaction_signal",
    "contains_unit_price_relation",
    "contains_payment_or_change_relation",
    "multi_step_calculation"
  ]
}
```

### Problem

A bag of dozen apples costs $14 and Brian has already spent $10 on kiwis and half that much on bananas. What's the maximum number of apples Brian can buy if he left his house with only $50 and needs to pay the $3.50 subway fare each way?

### Response

```text
Brian requires a total of $3.50 + $3.50 = $7 to pay for the round trip subway fare
We also know he has spent half (1/2) the amount he spent on kiwis on bananas, so he'll spend (1/2) * $10 = $5 on bananas
So far in total he has spent $7 for his subway fare + $5 on bananas + $10 on kiwis = $7 + $5 + $10 = $22
If he left his house with only $50, then all he will have left for apples would be $50 - $22 = $28
If a bag of apples costs $14, then Brian would only be able to buy a maximum of $28/$14 = 2 bags of apples
If each bag of apples has a dozen (12) apples, then (2) two bags will have 12*2= 24 apples
#### 24
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 29. gsm8k_train_05631

### Categories

price_quantity_total, remaining_change

### Scores

```json
{
  "price_quantity_total": 8,
  "remaining_change": 5
}
```

### Match reasons

```json
{
  "price_quantity_total": [
    "contains_money_signal",
    "contains_transaction_signal",
    "contains_unit_price_relation",
    "contains_payment_or_change_relation",
    "multi_step_calculation"
  ],
  "remaining_change": [
    "contains_quantity_change",
    "contains_sequence_or_relation",
    "multi_step_calculation",
    "three_or_more_operations"
  ]
}
```

### Problem

Sara got her first paycheck of two weeks of work. She had worked 40 hours a week at $11.50 per hour. The first thing she did was buy a new set of tires for her car for $410. How much money was she left with?

### Response

```text
Sara worked 40 * 2 = 80 hours over two weeks.
She earned 11.50 * 80 = $920
After buying new tires, she had $920 - 410 = $510 left.
#### 510
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 30. gsm8k_train_03109

### Categories

price_quantity_total, remaining_change

### Scores

```json
{
  "price_quantity_total": 8,
  "remaining_change": 5
}
```

### Match reasons

```json
{
  "price_quantity_total": [
    "contains_money_signal",
    "contains_transaction_signal",
    "contains_unit_price_relation",
    "contains_payment_or_change_relation",
    "multi_step_calculation"
  ],
  "remaining_change": [
    "contains_quantity_change",
    "contains_sequence_or_relation",
    "multi_step_calculation",
    "three_or_more_operations"
  ]
}
```

### Problem

Annie has $120. The restaurant next door sells hamburgers for $4 each. The restaurant across the street sells milkshakes for $3 each. Annie buys 8 hamburgers and 6 milkshakes. How much money, in dollars, does she have left?

### Response

```text
Annie spends 4*8=32 dollars on hamburgers.
Annie spends 3*6=18 dollars on milkshakes.
Annie spends 32+18=50 dollars on hamburgers and milkshakes.
Annie has 120-50=70 dollars left.
#### 70
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

