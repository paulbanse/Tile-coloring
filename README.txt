This experiment was designed to run on Otree version 5.9. 

To run the validation study, start a otree server:
  otree prodserver
    or
  otree devserver

Then on the experiment webpage (for devserver default is http://localhost:8000/) click "Validation", and then create a session following standard Otree procedure.  

After the experiment, a database "db.sqlite3" is created. Easiest procedure is to extract it from within the Otree browser interface (Data tab -> All Apps -> plain). 

Additional information for data analysis:
  
  Science is of value 0 or 1, 1 coding for when the participants were tested in a scientific context -> this was systematically 0 in the actual expriment
  sampleStart is of value 0 or 1, 1 coding for when the participant is being tested for sample or number of study, importantly due to otree limitation sample Start on the fifth round is already changed
  baseNumberOfClicks is used internally on the familiarization parts to count the number of samples or studies achieved in 30 seconds
  theoreticalTarget is the theoretical estimation of the perfect target for a participant to be able to reach, totalling 3*baseNumberOfClicks
  strSubList is the list in string of all the sample sizes used during a round
  letterList is the list in string of all the charater used to create studies during a round

