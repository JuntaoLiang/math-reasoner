# equation_multistep candidate review

候选总数：150

当前展示前 30 条，用于人工抽查。

## 1. gsm8k_train_07214

### Categories

price_quantity_total, equation_multistep

### Scores

```json
{
  "price_quantity_total": 6,
  "equation_multistep": 8
}
```

### Match reasons

```json
{
  "price_quantity_total": [
    "contains_money_signal",
    "contains_transaction_signal",
    "contains_unit_price_relation",
    "multi_step_calculation"
  ],
  "equation_multistep": [
    "contains_explicit_quantity_relation",
    "multi_step_calculation",
    "response_uses_equation",
    "three_or_more_operations",
    "multiple_relation_signals"
  ]
}
```

### Problem

Mike and John dined at the Taco Palace restaurant.  They each ordered the Taco Grande Plate as their main meal, but Mike also ordered a side salad for $2, a plate of cheesy fries for $4, and a diet cola for $2.  As a result, Mike's lunch bill was twice as large as John's bill.  What was the combined total cost, in dollars, of Mike and John's lunch?

### Response

```text
Let "x" be the cost in dollars of the Taco Grande Plate.
Since twice the cost of John's Taco Plate equals the cost of Mike's Taco Plate plus added items, then 2x = x+2+4+2.
Simplifying the equation, we get 2x = x+8.
Subtracting x from each side of the equation, we are left with x=8 dollars as the cost of the Taco Grande Plate.
Thus the combined total cost of Mike and John's lunch is 8+8+2+4+2=24 dollars.
#### 24
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 2. gsm8k_train_03574

### Categories

equation_multistep

### Scores

```json
{
  "equation_multistep": 8
}
```

### Match reasons

```json
{
  "equation_multistep": [
    "contains_explicit_quantity_relation",
    "multi_step_calculation",
    "response_uses_equation",
    "three_or_more_operations",
    "multiple_relation_signals"
  ]
}
```

### Problem

Jennifer bought twice as many candies as Emily and three times as many as Bob bought. If Emily bought 6 candies, how many candies did Bob buy?

### Response

```text
Jennifer bought twice as many as Emily (who bought 6 candies) which is 6*2 = 12 candies
12 candies (that Jennifer bought) is three times as much as what Bob bought which means 3*what Bob bought = 12
Dividing both sides of the equation by 3 gives: Number of candies Bob bought = 12/3 = 4 candies
#### 4
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 3. gsm8k_train_01338

### Categories

equation_multistep

### Scores

```json
{
  "equation_multistep": 8
}
```

### Match reasons

```json
{
  "equation_multistep": [
    "contains_explicit_quantity_relation",
    "multi_step_calculation",
    "response_uses_equation",
    "three_or_more_operations",
    "multiple_relation_signals"
  ]
}
```

### Problem

Bonny just bought her 13th pair of shoes, which is 5 less than twice as many pairs of shoes as Becky owns.  Bobby has 3 times as many pairs of shoes as Becky has.  How many shoes does Bobby have?

### Response

```text
Let x be the number of pairs of shoes that Becky owns.
Since 13 pairs is 5 less than twice as many pairs as Becky owns, then the relationship is 2x-5=13.
Adding 5 to each side of the equation, we get 2x=18.
Solving for x, we get x=9.
Since Bobby has 3 times as many pairs of shoes as Becky has, then Becky has 3*9=27 pairs of shoes.
#### 27
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 4. gsm8k_train_04815

### Categories

equation_multistep

### Scores

```json
{
  "equation_multistep": 8
}
```

### Match reasons

```json
{
  "equation_multistep": [
    "contains_explicit_quantity_relation",
    "multi_step_calculation",
    "response_uses_equation",
    "three_or_more_operations",
    "multiple_relation_signals"
  ]
}
```

### Problem

Mindy has 7 less than 9 times as many emails waiting for her as phone messages. If she has a total of 93 emails and phone messages combined, how many emails does she have?

### Response

```text
Let e be the number of emails Mindy has and m be the number of phone messages? We know that e + m = 93 and e = 9m - 7.
Substituting the second equation into the first equation, we get 9m - 7 + m = 93
Combining like terms, we get 10m - 7 = 93
Adding 7 to both sides of the equation, we get 10m = 100
Dividing both sides by 10, we get m = 10
Substituting this value back into the equation e = 9m - 7, we get e = 9 * 10 - 7 = 90 - 7 = 83
#### 83
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 5. gsm8k_train_02922

### Categories

equation_multistep

### Scores

```json
{
  "equation_multistep": 8
}
```

### Match reasons

```json
{
  "equation_multistep": [
    "contains_explicit_quantity_relation",
    "multi_step_calculation",
    "response_uses_equation",
    "three_or_more_operations",
    "multiple_relation_signals"
  ]
}
```

### Problem

Martin rings the small bell 4 times more than 1/3 as often as the big bell. If he rings both of them a combined total of 52 times, how many times does he ring the big bell?

### Response

```text
Let s be the number of times the small bell rings, and b be the number of times the big bell rings. We know that s + b = 52 and s = 4 + 1/3b.
Substituting the second equation into the first equation, we get 4 + 1/3b + b = 52
Subtracting 4 from both sides, we get 1/3b + b = 48
Combining like terms, we get 4/3b = 48
Dividing both sides of the equation by 4/3, we get b = 36
#### 36
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 6. gsm8k_train_02980

### Categories

equation_multistep

### Scores

```json
{
  "equation_multistep": 8
}
```

### Match reasons

```json
{
  "equation_multistep": [
    "contains_explicit_quantity_relation",
    "multi_step_calculation",
    "response_uses_equation",
    "three_or_more_operations",
    "multiple_relation_signals"
  ]
}
```

### Problem

Barbeck has two times as many guitars as Steve, but Davey has three times as many guitars as Barbeck. If there are 27 guitars altogether, how many guitars does Davey have?

### Response

```text
Let x = the number of guitars Steve has.
Barbeck has 2x guitars, and Davey has 3 * 2x = 6x guitars.
2x + 6x + x = 27
9x = 27
x = 27 / 9 = 3 so Steve has 3 guitars.
Barbeck has 2 * 3 = 6 guitars.
And Davey has 3 * 6 = 18 guitars.
#### 18
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 7. gsm8k_train_03031

### Categories

equation_multistep

### Scores

```json
{
  "equation_multistep": 8
}
```

### Match reasons

```json
{
  "equation_multistep": [
    "contains_explicit_quantity_relation",
    "multi_step_calculation",
    "response_uses_equation",
    "three_or_more_operations",
    "multiple_relation_signals"
  ]
}
```

### Problem

Together 3 friends watched 411 short videos. Kelsey watched 43 more than Ekon. Ekon watched 17 less than Uma. How many videos did Kelsey watch?

### Response

```text
Let U = the number of videos Uma watched
Ekon = U - 17
Kelsey = (U - 17) + 43 = U + 26
U + U - 17 + U + 26 = 411
3U + 9 = 411
3U = 402
U = 134
Kelsey = 134 + 26 = 160 videos
Kelsey watched 160 videos.
#### 160
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 8. gsm8k_train_05905

### Categories

equation_multistep

### Scores

```json
{
  "equation_multistep": 8
}
```

### Match reasons

```json
{
  "equation_multistep": [
    "contains_explicit_quantity_relation",
    "multi_step_calculation",
    "response_uses_equation",
    "three_or_more_operations",
    "multiple_relation_signals"
  ]
}
```

### Problem

Bill and Phil are firehouse Dalmatians. Bill has one less than twice as many spots as Phil. If they have 59 spots combined, how many spots does Bill have?

### Response

```text
If b is the number of spots Bill has and p is the number of spots Phil has, we know that b + p = 59. We also know that b = 2p - 1.
We can substitute the second equation into the first equation to get: 2p - 1 + p = 59
Combining like terms, we get 3p - 1= 59
Adding 1 to both sides, we get 3p = 60
Dividing both sides by 3, we get p = 20
Substituting this back into the equation b = 2p - 1, we get b = 2*20 - 1 = 40 - 1 = 39
#### 39
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 9. gsm8k_train_07416

### Categories

equation_multistep

### Scores

```json
{
  "equation_multistep": 8
}
```

### Match reasons

```json
{
  "equation_multistep": [
    "contains_explicit_quantity_relation",
    "multi_step_calculation",
    "response_uses_equation",
    "three_or_more_operations",
    "multiple_relation_signals"
  ]
}
```

### Problem

It took Dad 5 more than twice as long to vacuum upstairs then to vacuum downstairs. He vacuumed for a total of 38 minutes. How many minutes did he vacuum upstairs?

### Response

```text
Let D = time in minutes to vacuum downstairs
Upstairs = 2D + 5 minutes
3D + 5 = 38
3D = 33
D = 11 minutes
Upstairs = (2 * 11) + 5 = 27 minutes
Dad took 27 minutes to vacuum upstairs.
#### 27
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 10. gsm8k_train_06293

### Categories

equation_multistep

### Scores

```json
{
  "equation_multistep": 7
}
```

### Match reasons

```json
{
  "equation_multistep": [
    "contains_explicit_quantity_relation",
    "multi_step_calculation",
    "response_uses_equation",
    "three_or_more_operations"
  ]
}
```

### Problem

Allen is 25 years younger than his mother. In 3 years, the sum of their ages will be 41. What is the present age of Allen's mother?

### Response

```text
In 3 years, the sum of their present ages will be added by 3 (from Allen) + 3 (from her mother) = 6.
So, the sum of their present ages is 41 - 6 = 35.
Let x be the present age of Allen's mother and x - 25 be the present age of Allen.
So the equation using the sum of their present ages is x + x - 25 = 35.
By combining like terms, the equation becomes 2x = 60.
Hence, Allen's mother is x = 60/2 = 30 years old now.
#### 30
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 11. gsm8k_train_02457

### Categories

equation_multistep

### Scores

```json
{
  "equation_multistep": 7
}
```

### Match reasons

```json
{
  "equation_multistep": [
    "contains_explicit_quantity_relation",
    "multi_step_calculation",
    "response_uses_equation",
    "three_or_more_operations"
  ]
}
```

### Problem

Balki is counting the number of raisins in boxes of cereal. He counted 437 total raisins in 5 boxes. In one box he counted 72 raisins. In a second box he counted 74 raisins. The other three boxes had the same number each. How many were in each of the other three boxes?

### Response

```text
Let x = the number of raisins in each of the other 3 boxes. Then 72 + 74 + 3x = 437 raisins
Combining like terms we get 146 + 3x = 437 raisins
Subtracting 146 from both sides we get 3x = 291 raisins
Dividing both sides by 3, we get x = 291 / 3 = 97 raisins
#### 97
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 12. gsm8k_train_00110

### Categories

remaining_change, equation_multistep

### Scores

```json
{
  "remaining_change": 5,
  "equation_multistep": 7
}
```

### Match reasons

```json
{
  "remaining_change": [
    "contains_quantity_change",
    "contains_sequence_or_relation",
    "multi_step_calculation",
    "three_or_more_operations"
  ],
  "equation_multistep": [
    "contains_explicit_quantity_relation",
    "multi_step_calculation",
    "response_uses_equation",
    "three_or_more_operations"
  ]
}
```

### Problem

Alyssa, Keely, and Kendall ordered 100 chicken nuggets from a fast-food restaurant. Keely and Kendall each ate twice as many as Alyssa. How many did Alyssa eat?

### Response

```text
To figure out this problem we need to turn it into an equation. Let’s make A the number of nuggets Alyssa ate. We know all three girls ate 100 nuggets total, so 100 nuggets = A (how many Alyssa ate) + 2A (how many Keely ate) + 3A (how many Kendall ate) or 100 = A + 2A + 3A which is 100 = 5A
Then we will divide each side by 5 to figure out how many nuggets Alyssa ate, 100/5 = 5A/5 or 20 = A.
#### 20
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 13. gsm8k_train_01538

### Categories

equation_multistep

### Scores

```json
{
  "equation_multistep": 7
}
```

### Match reasons

```json
{
  "equation_multistep": [
    "contains_explicit_quantity_relation",
    "multi_step_calculation",
    "response_uses_equation",
    "three_or_more_operations"
  ]
}
```

### Problem

Antoinette weighs 7 less kilograms than twice Rupert's weight. Together they weigh 98 kilograms. How many kilograms does Antoinette weigh?

### Response

```text
Let R = Rupert's weight
Antoinette = 2R - 7
R + 2R - 7 = 98
3R = 105
Rupert = 35 kg
Antoinette = 2 * 35 - 7 = 63 kg
Antoinette weighs 63 kilograms.
#### 63
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 14. gsm8k_train_05210

### Categories

equation_multistep

### Scores

```json
{
  "equation_multistep": 7
}
```

### Match reasons

```json
{
  "equation_multistep": [
    "contains_explicit_quantity_relation",
    "multi_step_calculation",
    "response_uses_equation",
    "three_or_more_operations"
  ]
}
```

### Problem

Samantha, Aira, and Joe received 6 rubber bands each after they divided their bands equally.  If Samantha had 5 more bands than Aira and Aira had 1 fewer band than Joe, how many rubber bands did Aira have?

### Response

```text
Samantha, Aira, and Joe have 6 x 3 = 18 rubber bands altogether.
If we let x be the number of bands that Aira had, then Samantha had x + 5.
Since Aira had 1 fewer band than Joe, then Joe had x + 1.
Since the total number of bands is 18, then the equation is x + (x + 5) + (x + 1) = 18.
By simplifying the left side of the equation, we have 3x + 6 = 18.
Putting all the constant terms on the right side gives 3x = 12.
So the value of x is 12/3 = 4. Hence, Aira had 4 rubber bands.
#### 4
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 15. gsm8k_train_01369

### Categories

equation_multistep

### Scores

```json
{
  "equation_multistep": 7
}
```

### Match reasons

```json
{
  "equation_multistep": [
    "contains_explicit_quantity_relation",
    "multi_step_calculation",
    "response_uses_equation",
    "three_or_more_operations"
  ]
}
```

### Problem

Tamara is 3 times Kim's height less 4 inches. Tamara and Kim have a combined height of 92 inches. How many inches tall is Tamara?

### Response

```text
Let K = Kim's height
Tamara = 3K - 4
K + 3K - 4 = 92
4K - 4 = 92
4K = 96
Kim = 24 inches
Tamara = (3 * 24) - 4 = 68 inches
Tamara is 68 inches tall.
#### 68
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 16. gsm8k_train_02247

### Categories

equation_multistep

### Scores

```json
{
  "equation_multistep": 7
}
```

### Match reasons

```json
{
  "equation_multistep": [
    "contains_explicit_quantity_relation",
    "multi_step_calculation",
    "response_uses_equation",
    "three_or_more_operations"
  ]
}
```

### Problem

The lifespan of a hamster is 6 years less than that of a bat. The lifespan of a frog is 4 times that of a hamster. Altogether, the lifespan of the animals is 30 years. What is the lifespan of the bat?

### Response

```text
Let’s set up an equation by calling the lifespan of a bat x, and therefore the lifespan of the hamster x – 6, and the lifespan of the frog 4 (x – 6) which add together to equal 30, like this: x + x – 6 + 4 (x – 6) = 30.
That gives us 6x – 30 = 30 and we should add 30 to each side to try to isolate the x.
Now we have 6x = 60, which we will divide by 6, 6x / 6 = 60 / 6.
This gives us x = 10. The bat has a lifespan of 10 years.
#### 10
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 17. gsm8k_train_00719

### Categories

equation_multistep

### Scores

```json
{
  "equation_multistep": 7
}
```

### Match reasons

```json
{
  "equation_multistep": [
    "contains_explicit_quantity_relation",
    "multi_step_calculation",
    "response_uses_equation",
    "three_or_more_operations"
  ]
}
```

### Problem

Jake and Penny are hunting snakes. Jake's snake is 12 inches longer than Jenny's snake. If the two snakes have a combined length of 70 inches, how long is Jake's snake?

### Response

```text
Let j be the length of Jake's snake and p be length of Penny's snake. We know that j + p = 70, and j = p + 12.
We can substitute the second equation into the first equation to get p + 12 + p = 70
Combining like terms, we get 2p + 12 = 70
Subtracting 12 from both sides, we get 2p = 58
Dividing both sides by 2, we get p = 58 / 2 = 29 inches. Penny's snake is 29 inches.
Substituting that length in to the equation j = p + 12, we get j = 29 inches + 12 inches = 41 inches
#### 41
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 18. gsm8k_train_07341

### Categories

equation_multistep

### Scores

```json
{
  "equation_multistep": 7
}
```

### Match reasons

```json
{
  "equation_multistep": [
    "contains_explicit_quantity_relation",
    "multi_step_calculation",
    "response_uses_equation",
    "three_or_more_operations"
  ]
}
```

### Problem

John and Yasmin's dad is named Gabriel. If John has twice the number of children that her sister has and Gabriel has six grandkids, how many children does Yasmin have?

### Response

```text
We don't know Yasmin's number of children yet, but let's represent it as Y.
If John has twice the number of children Yasmin has, then John has 2*Y = 2Y kids
If Gabriel has 6 grandkids between John's and Yasmin's children, then we can represent this as 6 = 2Y + Y
If we solve the latest equation then we learn that 6=3Y
Given that Y represents how many kids Yasmin has, then solving for Y we know that Y=6/3 or Y=2 kids
#### 2
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 19. gsm8k_train_06409

### Categories

equation_multistep

### Scores

```json
{
  "equation_multistep": 7
}
```

### Match reasons

```json
{
  "equation_multistep": [
    "contains_explicit_quantity_relation",
    "multi_step_calculation",
    "response_uses_equation",
    "three_or_more_operations"
  ]
}
```

### Problem

Annie is building a diorama for her history class. The amount of time she spent building it is equal to three times the amount of time she spent planning it minus 5 minutes. If she spent 67 minutes on the diorama total, how many minutes did she spend building it?

### Response

```text
Let p be the planning time in minutes and b be the building time. We know that b = 3p - 5 and b + p = 67
Substituting the first equation into the second equation, we get 3p - 5 + p = 67
Combining like terms, we get 4p - 5 = 67
Adding 5 to both sides, we get 4p = 72
Dividing both sides by 4, we get p = 18
Substituting this value into b = 3p - 5, we find that b = 3 * 18 - 5 = 49
#### 49
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 20. gsm8k_train_03293

### Categories

equation_multistep

### Scores

```json
{
  "equation_multistep": 7
}
```

### Match reasons

```json
{
  "equation_multistep": [
    "contains_explicit_quantity_relation",
    "multi_step_calculation",
    "response_uses_equation",
    "three_or_more_operations"
  ]
}
```

### Problem

A special school for deaf and blind students has a deaf student population three times the size of blind student population. If the number of deaf students is 180, how many students are there altogether?

### Response

```text
Call the number of blind students b. There are 180 deaf students, which is three times the number of blind students, so 3b = 180
Multiplying both sides of the equation by 1/3 gives b = (1/3)*180 = 60
The total number of students is 180 + 60 = 240
#### 240
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 21. gsm8k_train_01008

### Categories

equation_multistep

### Scores

```json
{
  "equation_multistep": 7
}
```

### Match reasons

```json
{
  "equation_multistep": [
    "contains_explicit_quantity_relation",
    "multi_step_calculation",
    "response_uses_equation",
    "three_or_more_operations"
  ]
}
```

### Problem

Rajesh walked 10 kilometers less than 4 times the distance that Hiro walked. Together they walked 25 kilometers. How many kilometers did Rajesh walk?

### Response

```text
Let H = distance Hiro walked
4H - 10 = distance Rajesh walked
H + 4H - 10 = 25
5H - 10 = 25
5H = 35
Hiro walked 7 km so Rajesh walked 4(7) - 10 = 18 km
Rajesh walked 18 kilometers.
#### 18
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 22. gsm8k_train_06241

### Categories

equation_multistep

### Scores

```json
{
  "equation_multistep": 7
}
```

### Match reasons

```json
{
  "equation_multistep": [
    "contains_explicit_quantity_relation",
    "multi_step_calculation",
    "response_uses_equation",
    "three_or_more_operations"
  ]
}
```

### Problem

Leonard is 4 years younger than Nina who is half as old as Jerome. If the sum of their ages is 36, what is Leonard's age?

### Response

```text
Let x be the age of Nina.
So, Leonard's age is x - 4.
And Jerome's age is 2x.
Since the sum of their ages is 36, then the equation is x + x - 4 + 2x = 36.
By combining like terms, the equation becomes 4x = 40.
So the value of x which represents the age of Nina is x = 40/4 = 10.
Therefore, Leonard is 10 - 4 = 6 years old.
#### 6
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 23. gsm8k_train_03332

### Categories

remaining_change, equation_multistep

### Scores

```json
{
  "remaining_change": 7,
  "equation_multistep": 7
}
```

### Match reasons

```json
{
  "remaining_change": [
    "contains_quantity_change",
    "contains_sequence_or_relation",
    "multi_step_calculation",
    "contains_both_sequence_and_relation",
    "three_or_more_operations"
  ],
  "equation_multistep": [
    "contains_explicit_quantity_relation",
    "multi_step_calculation",
    "response_uses_equation",
    "three_or_more_operations"
  ]
}
```

### Problem

Hasan is packing up his apartment because he’s moving across the country for a new job. He needs to ship several boxes to his new home. The movers have asked that Hasan avoid putting more than a certain weight in pounds in any cardboard box. The moving company has helpfully provided Hasan with a digital scale that will alert him if a package is too heavy. Hasan is in the kitchen, and he fills a cardboard box with 38 dinner plates. When he checks the box, the scale reports his box is too heavy. Hasan knows each of his plates weighs 10 ounces. He removes a single plate from the box and checks the movers’ scale again. The scale reports his box is still too heavy. Hasan repeats the process again and again. When he has removed enough plates, the movers’ scale shows the box is now an acceptable weight for shipping. Hasan deduces that each shipping box can hold 20 pounds before the scale says the box is too heavy.  How many plates did Hasan need to remove from the shipping box?

### Response

```text
Let x be the number of plates removed from the box.
Hasan figured out the movers' weight limit was 20 pounds. Since a pound is equal to 16 ounces, each box can hold 20 * 16, or 320 ounces.
Each plate weighs 10 ounces, so the weight of the plates in the box after Hasan removes enough plates to satisfy the movers' weight limit is (38 - x) * 10 ounces
Since these two values are equal, we can write the equation (38 - x) * 10 = 320.
Dividing both sides by 10 leaves 38-x = 32.
Adding x to both sides gives 38 – x + x = 32 +x, or, 38 = 32 +x
Subtracting 32 from both sides gives the value of x, which is the number of plates removed from the box, 38 -32 = 32 + x – 32, or, 6 = x
#### 6
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 24. gsm8k_train_00793

### Categories

equation_multistep

### Scores

```json
{
  "equation_multistep": 7
}
```

### Match reasons

```json
{
  "equation_multistep": [
    "contains_explicit_quantity_relation",
    "multi_step_calculation",
    "response_uses_equation",
    "three_or_more_operations"
  ]
}
```

### Problem

The Chrysler Building has 11 more floors than the Leeward Center. Together they have a total of 35 floors. How many floors does the Chrysler Building have?

### Response

```text
Let L = Leeward Center
Chrysler = L + 11
L + L + 11 = 35
2L + 11 = 35
2L = 24
Leeward = 12 floors
Chrysler = 12 + 11 = 23 floors
The Chrysler Building has 23 floors.
#### 23
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 25. gsm8k_train_01418

### Categories

equation_multistep

### Scores

```json
{
  "equation_multistep": 7
}
```

### Match reasons

```json
{
  "equation_multistep": [
    "contains_explicit_quantity_relation",
    "multi_step_calculation",
    "response_uses_equation",
    "three_or_more_operations"
  ]
}
```

### Problem

The sum of Mario and Maria's ages now is 7. Mario is 1 year older than Maria. How old is Mario?

### Response

```text
If x is Maria's age, then Mario's age is x + 1.
The equation that represents the sum of their ages is x + x + 1 = 7.
By combining like terms, the equation becomes 2x = 6.
Hence, the value of x which represents the age of Maria is 6/2=3.
So Mariu is 3 + 1 = 4 years old.
#### 4
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 26. gsm8k_train_04985

### Categories

equation_multistep

### Scores

```json
{
  "equation_multistep": 7
}
```

### Match reasons

```json
{
  "equation_multistep": [
    "contains_explicit_quantity_relation",
    "multi_step_calculation",
    "response_uses_equation",
    "three_or_more_operations"
  ]
}
```

### Problem

Bill and Joan both work for a library. 5 years ago, Joan had 3 times as much experience as Bill. Now she has twice as much experience as Bill. How many years of experience does Bill have now?

### Response

```text
Let b be Bill's years of experience and j be Joan's years of experience. We know that j - 5 = 3(b - 5) and j = 2b.
Substituting the second equation into the first equation, we get 2b - 5 = 3(b - 5)
Multiplying through the parentheses, we get 2b - 5 = 3b - 15
Adding 15 to both sides, we get 2b + 10 = 3b
Subtracting 2b from both sides, we get 10 = b
#### 10
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 27. gsm8k_train_02097

### Categories

equation_multistep

### Scores

```json
{
  "equation_multistep": 7
}
```

### Match reasons

```json
{
  "equation_multistep": [
    "contains_explicit_quantity_relation",
    "multi_step_calculation",
    "response_uses_equation",
    "three_or_more_operations"
  ]
}
```

### Problem

Beth went shopping. She bought 15 more cans of peas than twice the number of cans of corn that she bought. If she bought 35 cans of peas, how many cans of corn did she buy?

### Response

```text
Let the number of cans of corn she bought be a
Twice the number of corn cans is 2*a = 2a
The 35 cans of peas were 15 more than twice the number of corn cans which means 15+2a = 35
Solving the equation: 2a = 20
a = 20/2 = 10 cans of corn
#### 10
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 28. gsm8k_train_03763

### Categories

equation_multistep

### Scores

```json
{
  "equation_multistep": 7
}
```

### Match reasons

```json
{
  "equation_multistep": [
    "contains_explicit_quantity_relation",
    "multi_step_calculation",
    "response_uses_equation",
    "three_or_more_operations"
  ]
}
```

### Problem

Between them, Mark and Sarah have 24 traffic tickets. Mark has twice as many parking tickets as Sarah, and they each have an equal number of speeding tickets. If Sarah has 6 speeding tickets, how many parking tickets does Mark have?

### Response

```text
First figure out how many total speeding tickets the two people got by adding the 6 speeding tickets Sarah got to the equal number (6) that Mark got: 6 + 6 = 12
Now subtract the combined number of speeding tickets from the total number of tickets to find the combined number of parking tickets: 24 - 12 = 12
Now express Mark's number of parking tickets in terms of the number of parking tickets Sarah got: m = 2s
We know that m + s = 12, so substitute in the value of m from the previous step to get 2s + s = 12
Combine like terms to get 3s = 12
Divide both sides of the equation to get s = 4
Now multiply the number of parking tickets Sarah got by 2 to find the number Mark got: 4 * 2 = 8
#### 8
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 29. gsm8k_train_02918

### Categories

remaining_change, equation_multistep

### Scores

```json
{
  "remaining_change": 5,
  "equation_multistep": 7
}
```

### Match reasons

```json
{
  "remaining_change": [
    "contains_quantity_change",
    "contains_sequence_or_relation",
    "multi_step_calculation",
    "three_or_more_operations"
  ],
  "equation_multistep": [
    "contains_explicit_quantity_relation",
    "multi_step_calculation",
    "response_uses_equation",
    "three_or_more_operations"
  ]
}
```

### Problem

If two piles of toys added together make 120 toys in total, and the larger of the two piles is twice as big as the smaller one, how many toys are in the larger pile?

### Response

```text
First, we set up the equation 3x=120, dividing both sides by three to find that x=40
Then we multiply X by 2 to find that 40*2= 80
As 80/2=40, and 40+80=120, we find the sizes of the two piles as the larger pile is twice as big as the smaller pile, confirming that 80 is the answer.
#### 80
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

## 30. gsm8k_train_00753

### Categories

equation_multistep

### Scores

```json
{
  "equation_multistep": 7
}
```

### Match reasons

```json
{
  "equation_multistep": [
    "contains_explicit_quantity_relation",
    "multi_step_calculation",
    "response_uses_equation",
    "three_or_more_operations"
  ]
}
```

### Problem

The length of a rectangle is four times its width. If the area is 100 m2. what is the length of the rectangle?

### Response

```text
Let L be the length and W be the width of the rectangle.
Hence L = 4* W
We now use the area to write 80 = L * W
Substitute L by 4 W in the equation above 80 = 4*W × W = 4 W^2
Solve for W and find L
4 W^2 = 100
W^2 = 25, W = 5 and
L = 4*5 = 20 m
#### 20
```

### Manual review

- Relevant: 
- Primary category: 
- Notes: 

---

