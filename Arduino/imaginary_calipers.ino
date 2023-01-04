// print out a random number over serial whenever the reset button 
// is pressed to simulate a measurement being sent from the calipers

void setup() {
  Serial.begin(9600);
  randomSeed(analogRead(0));
  Serial.println("   0.966              2");
  //Serial.println("   0.966");
  pinMode(13, OUTPUT);
  pinMode(2,INPUT_PULLUP);
}

void loop() {
//  digitalWrite(13, HIGH);
//  delay(500);
//  digitalWrite(13, LOW);
//  delay(500);
  if(!digitalRead(2)) {
    printReading();
    delay(300);
  }
}

void printReading() {
  Serial.print(" ");
  bool prevNum = 0;
  int ran=random(0,9);
  
  if (ran>0) {Serial.print(" ");}
  else {
    Serial.print("1");
    prevNum=1;
  }
  ran=random(0,9);
  if (ran==0 && !prevNum) {Serial.print(" ");}
  else {Serial.print(ran);}
  ran=random(2,9);
  Serial.print(ran);
  Serial.print(".");
  ran=random(0,9);
  Serial.print(ran);
  ran=random(0,9);
  Serial.print(ran);
  ran=random(0,9);
  Serial.println(ran);
  Serial.println("              2");
}
