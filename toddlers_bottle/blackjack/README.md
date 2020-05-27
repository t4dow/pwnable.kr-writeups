#### blackjack

We are given a [link](https://cboard.cprogramming.com/c-programming/114023-simple-blackjack-program.html)
to a blackjack program written in C. The goal is to get a million dollars in
winnings.

We start with $500. Reaching a million if we play fairly will take forever.
After looking at the code, we can see the following snippet of code

```c
void cash_test() //Test for if user has cash remaining in purse
{
     if (cash <= 0) //Once user has zero remaining cash, game ends and prompts user to play again
     {
        printf("You Are Bankrupt. Game Over");
        cash = 500;
        askover();
     }
} // End Function

int betting() //Asks user amount to bet
{
    printf("\n\nEnter Bet: $");
    scanf("%d", &bet);

    if (bet > cash) //If player tries to bet more money than player has
    {
        printf("\nYou cannot bet more money than you have.");
        printf("\nEnter Bet: ");
        scanf("%d", &bet);
        return bet;
    }
    else return bet;
} // End Function
```

The `betting` function makes sure that the amount we bet is not more than the
amount of cash we currently have. The problem is, you can enter the bet twice
and the program won't check if you're second bet is valid or not.

The other problem is that, `bet` and `cash` are both signed integers. So if we
enter a large negative number, the check will pass. And if we lose the round, we
will get an increase in the cash we hold.

I set my value of `cash` to `INT_MAX` and the program printed out the flag. To
calculate the amount to bet:

```c
#include <stdio.h>
#include <limits.h>

int main() {
    int x = 500;
    int result = INT_MAX;

    printf("%d\n", result - x);
}
```

If we play with this amount, we should get the flag.

```sh
Cash: $500
-------
|H    |
|  7  |
|    H|
-------

Your Total is 7

The Dealer Has a Total of 8

Enter Bet: $-2147483147


Would You Like to Hit or Stay?
Please Enter H to Hit or S to Stay.
S

You Have Chosen to Stay at 7. Wise Decision!

The Dealer Has a Total of 15
The Dealer Has a Total of 22
Dealer Has the Better Hand. You Lose.

You have 0 Wins and 1 Losses. Awesome!

Would You Like To Play Again?
Please Enter Y for Yes or N for No
Y
YaY_I_AM_A_MILLIONARE_LOL
```
