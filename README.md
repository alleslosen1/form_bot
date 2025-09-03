Skewable Google form auto filler bot, only works for no-sign-in forms.

Currently only supports radio buttons, checkboxes, and dropdowns

Usage
-----
1. Run the python script
2. Enter total number of questions
3. Enter the weights of each question
      > For radio button or dropdown questions, enter 1 1 1 for equal distribution or 1 1 9 for extreme 3rd option skew distribution. 
        Values are all relative and doesn't matter, 1 1 1 and 54 54 54 have the same outcome

      > For checkbox questions, start input with a 'd' followed by the probability of each checkbox being selected
        (e.g. d 50 50 50 for a checkbox question with 3 options, and each option having a 50% of being selected) 
5. Enter 'x' to complete
6. Let the script run
