# Daily Documentation
## Week 1
### Day 1 - 2026-01-29
Today I discussed my initial ideas with Mr. Small and how this independent study will actually work. I created this GitHub repository and began doing some planning, I created my initial [6-6-6 plan](./6-6-6-Plan.md).

## Week 2
### Day 2 - 2026-02-02
Today I worked on my GitHub repository more. I added an initial BOM to my [project proposal](./Project-Proposal.md) and created [Daily-Documentation.md](Daily-Documentation.md)

### Day 3 - 2026-02-04
Today I really didn't feel like working on the GitHub repo so I started on some [Python code](./Code/main.py).

### Day 4 - 2026-02-06
I think my proposal is all ready, just need to find a specific thermal printer to buy. Today I mostly just worked on my Health 2 online stuff during class.

## Week 3
### Day 5 - 2026-02-10
Today I once again just worked on Health 2 online stuff while waiting for Mr. Small, he told me he was gonna look at the project proposal this weekend but he was busy, hopefully next class?

### Day 6 - 2026-02-12
Today I worked more on the Python code because I was tired
why do i only ever feel like doing code when im tired

Next class I think I'll start prototyping, assuming Mr. Small looks at my project proposal over the weekend.

## Week 4
### Day 7 - 2026-02-17
Today I talked to Mr. Small and discussed my project and ordering a thermal printer for the project. I also worked on the Python code a bit more.

### Day 8 - 2026-02-19
Worked on Arduino code for most of the time, once I got the Arduino IDE working on my laptop.
I'm tired, my birthday was yesterday, I stayed up kinda late

## Week 5
### Day 9 - 2026-02-23
Today I did wiring for the character LCD and got the display fully working! I finished the [display Arduino code](./Code/arduinoSelfStudyCode.ino) and worked on the [Python code](./Code/main.py) a bit more.  
![No Messages Waiting](/Media/2026-02-23-no-messages-waiting.jpg)   
![Countdown](/Media/2026-02-23-countdown-test.jpg)   
[Countdown Test Video](/Media/2026-02-23-Countdown-Test.mp4)   

### Day 10 - 2026-02-25
Today I tried to get some motor stuff running for testing, but I instead just shorted everything, including my laptop's USB-A port, thought I fully fried my laptop, it wouldn't turn back on, not even the keyboard backlight or display would light up. Fixed it by holding the power button for a minute, then waiting 30 minutes. Luckily, my laptop survived, it powered on after half-an-hour. Didn't get much done other than fail to get motors running and shorting stuff and nearly killing my rather expensive laptop.

### Day 11 - 2026-02-27
Today I just spent all of class diagnosing wiring issues, I was really struggling getting stuff to work. It appears that last class I fried the Arduino, it wouldn't do anything. I was trying to get motors to spin all class before I realized "Oh, I probably fried the H-Bridge too" so next class I'll replace the H-Bridge and run some tests.  
![Dead Arduino](/Media/2026-02-27-dead-arduino.jpg)  

## Week 6
### Day 12 - 2026-03-03
Yup, that H-Bridge was dead, after replacing it everything works!  
![Dead H-Bridge](/Media/2026-03-03-dead-h-bridge.jpg)  
Supposed to have a deliverable this week, dunno how possible that's gonna be since I don't yet have the printer, although maybe the code + fully working wiring could count as a deliverable? I'll have to ask!  

![Wiring on Table](/Media/2026-03-03-wiring-on-table.jpg)   
![Wiring Top View](/Media/2026-03-03-wiring-top-view.jpg)   
[Motor Test Video](/Media/2026-03-03-Motor-Test.mp4)   

### Day 13 - 2026-03-05
So today I realized two things, one is that I'll either need an Arduino Mega or a second Arduino Uno to add the thermal printer and possibly a servo if I add it. The other thing I realized is that most thermal printers don't have an autocutter, including mine, so I'll need to somehow mechanically cut the paper as it comes out of the thermal printer, it has a serrated edge that you are supposed to yank the paper against. I also permanently changed my USB permissions on my laptop for the Arduino serial so I don't need to do `sudo chmod a+rw /dev/ttyACM0` every time I plug in the Arduino.

    Current ideas:  
    - have some feeder wheels to yank it against the serrated edge  
    - have a razor blade that slides against the paper with a linear actuator with the paper under tension

## Week 7
### Day 14 - 2026-03-09
I mainly just worked on a personal project today during class because I'm still waiting on the thermal printer (Supposed to show up next week). Next class I might work on figuring out wiring up a second Arduino for running the printer.

### Day 15 - 2026-03-11
Honestly just worked on my Health 2 online stuff and also my personal project, really just waiting on the thermal printer for prototyping.
  
### Day 16 - 2026-03-13
Thermal printer has been delayed again, will be here on March 20th apparently. Since I really don't wanna do nothing for another week I think I'll try to begin on CAD.

## Week 8
### Day 17 - 2026-03-17
CAD

### Day 18 - 2026-03-19
more CAD

## Week 9
### Day 19 - 2026-03-30
Today I worked on a bit more CAD and also got an update on shipping for my thermal printer, it's arriving today! It keeps getting delayed but it should finally show up, then I can get it wired and finally begin making a housing for it.

### Day 20 - 2026-04-01
Today I FINALLY got my thermal printer, I did some test prints and got it working. I had to do a really jank solution to get it running as it needed 9v to work properly, but we only have 4 and 8 battery packs, so I had to get an 8 battery pack and then put wires to jump where two more batteries would be. I also tested how I would actually cut the paper, I found a box cutter blade segment works rather well, I think I'll have my friend Kevin design a motorized thing for moving the razor blade along the paper, as he is much better at moving, motorized systems than I am.
![Thermal Printer](/Media/2026-04-01-thermal-printer.jpg)  
![Cutter Test](/Media/2026-04-01-cutter-test.jpg)  


### Day 21 - 2026-04-03
I was sick at home


## Week 10
### Day 22 - 2026-04-09
Tested the cutter system that Kevin helped me design, it works, somewhat, but there are some issue I need to deal with. Firstly, it is running at 9v, the motor has so much torque that the hard stop against the motor case doesn't stall the motor, it instead powers through the hard stop and breaks it off. Secondly, it has no idea if it has reached the end of the gear rack, but I might not need to fix this. I'll brainstorm how to fix this next class
![Cutter Mechanism](/Media/2026-04-09-cutter-mechanism.jpg)  
![It broke :c](/Media/2026-04-09-it-broke.jpg)  

## Week 11
### Day 23 - 2026-04-13
Today I just did some CAD, trying to figure out solutions to my problems. Namely, I designed a tip cover for the blade, hopefully this will help it cut easier and need less torque.
![Tip Cover On](/Media/2026-04-13-cover-on.png)  
![Tip Cover Off](/Media/2026-04-13-cover-off.png)  

### Day 24 - 2026-04-15
Today I cleaned up the CAD a bit, extended the rail the rack runs along, beefed up the hard stop, and added some mounting stuff.
![CAD Update](/Media/2026-04-15-cad-update.png)  
At the end of class, I was able to start printing some stuff.
![Slicer Screenshot](/Media/2026-04-15-slicer-screenshot.png)  

### Day 25 - 2026-04-17
Today I was visiting OSU, so I wasn't in class, but my parts I started printing are done of course.

## Week 12
### Day 26 - 2026-04-22
Today I tested some of my new printed parts, and it still isn't cutting reliably, aghhhh
![Cutter Test](/Media/2026-04-22-Cutter-Test.mp4)  
