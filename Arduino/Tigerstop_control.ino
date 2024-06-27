#include <HashMap.h>
#include <GCodeParser.h>

GCodeParser GCode = GCodeParser();

#define VERSION 1.1
#define MAX_BUF (64) // What is the longest message Arduino can store?

char buffer[MAX_BUF]; // where we store the message until we get a semicolon ';'
int sofar; // how much is in the buffer
float px; // location

const int LEDpin = 13;  // bright blue status LED to indicate when buttons are being manipulated

// FIXME change these to the minimum required values in order to maximize speed
const int holdTime = 30; // time to hold button down, in milliseconds
const int pauseTime = 30; // time to wait before pressing the next one
const int waitBetweenMoves = 1000; // makes sure it's been at least this long

long lastMoveTime = 0;
//             {    rows       } {     columns    }
//              0  1  2  3  4  5  6   7   8   9
int pins [10] { 2, 3, 4, 5, 6, 7, A0, A1, A2, A3 };
// gonna have to start thinking of this as 0 zero indexed...
// (rather than the 1 indexed pins in the schematic)

char *buttons [6][4] =
{
  "PgmLst", "Increm", "Stop", "&", // & and $ are merely unique placeholders (no actual button on the keypad)
  "7", "8", "9", "-",
  "4", "5", "6", "+",
  "1", "2", "3", "*",
  "0", ".", "=", "/",
  "Start", "Space", "Clear", "$"
};

const byte HASH_SIZE = 24; // 6*4 = 24...
//storage
HashType<char*, int> xRawArray[HASH_SIZE];
HashType<char*, int> yRawArray[HASH_SIZE];
//handles the storage [search,retrieve,insert]
HashMap<char*, int> xPins = HashMap<char*, int>( xRawArray , HASH_SIZE );
HashMap<char*, int> yPins = HashMap<char*, int>( yRawArray , HASH_SIZE );


void setup() {
  pinMode(LEDpin, OUTPUT);
  digitalWrite(LEDpin, HIGH);
  for (int i = 0; i < 10; i++) {
    pinMode(pins[i], OUTPUT);
  }
  Serial.begin(9600);
  Serial.println(F("Tigerstop serial interface ")); Serial.print(VERSION);
  Serial.println(F("Greatland Window"));
  Serial.println();
  Serial.println(F("Send M77 for help"));
  Serial.println();
  delay(1000);
  digitalWrite(LEDpin, LOW);

  buildHashMaps();

  //  xPins.debug();
  //  Serial.println();
  //  Serial.println();
  //  yPins.debug();
  //  Serial.println();
  //  Serial.println();

  // need to think through start sequence: maybe stop-start-delay-start just in case to perform homing,
  // and then go through the buttons to select unit system just in case it was left in millimeters?
  //pressButton("Start");
  // DEMO
//  pressButton("1");
//  pressButton("2");
//  pressButton("3");
//  pressButton(".");
//  pressButton("4");
//  pressButton("5");
//  pressButton("Start");
//  delay(2000);
//  pressButton("Stop");

}

void loop() {
  if (Serial.available() > 0)
  {
    if (GCode.AddCharToLine(Serial.read()))
    {
      processCommand();
    }
  }
}

void goTo(float pos) {
  long xthousand = pos * 1000;
  //Serial.println(xthousand);
  //  // this is going to be a really dumb way of doing it but I'm in a hurry...
  //  if (pos >= 100 && pos <= 125) {
  //    pressButton('1'); // all we need
  //    Serial.println("1");
  //  }
  //  if (pos >= 10) {
  //    int tensDigit = pos / 10; // think that'll truncate it correctly
  //    char[1] digit;
  //
  //    pressButton(digit);
  //    Serial.println(tensDigit);
  //  }
  //  int onesDigit = pos / 100;
  //  pressButton(digit);
  //  Serial.println(onesDigit);
  //
  // REVERSE ORDER REMEMBER???
  int thousanthsDigit = (xthousand % 10);
  int hundrethsDigit = (xthousand / 10) % 10;
  int tenthsDigit = (xthousand / 100) % 10;
  int onesDigit = (xthousand / 1000) % 10;
  int tensDigit = (xthousand / 10000) % 10;
  int hundredsDigit = (xthousand / 100000) % 10;

//  Serial.print(hundredsDigit);
//  Serial.print(tensDigit);
//  Serial.print(onesDigit);
//  Serial.print(".");
//  Serial.print(tenthsDigit);
//  Serial.print(hundrethsDigit);
//  Serial.print(thousanthsDigit);
//  Serial.println();

//  int a = 1; // example of converting int to char!
//  char b[2];
//  String str;
//  str = String(a);
//  str.toCharArray(b, 2);
    // length of char needs to be fitting for value
//    char tempChar[2];
//    String temp_str = String(hundredsDigit);
//    temp_str.toCharArray(tempChar, 2);
//    pressButton(tempChar);
//    temp_str = String(tensDigit);
//    temp_str.toCharArray(tempChar, 2);
//    pressButton(tempChar);
//    temp_str = String(onesDigit);
//    temp_str.toCharArray(tempChar, 2);
//    pressButton(tempChar);
//    pressButton("."); // decimal
//    temp_str = String(tenthsDigit);
//    temp_str.toCharArray(tempChar, 2);
//    pressButton(tempChar);
//    temp_str = String(hundrethsDigit);
//    temp_str.toCharArray(tempChar, 2);
//    pressButton(tempChar);
//    temp_str = String(thousanthsDigit); // note: something results in a round down error on the thousandths
//    temp_str.toCharArray(tempChar, 2);
//    pressButton(tempChar);

  //pressButton("Stop");
  //delay(500); // extra special delay
  //pressButton("0");
  pressButton("0");
  pressButton("0");
  pressInt(hundredsDigit); // we don't need readings over 100
  pressInt(tensDigit);
  pressInt(onesDigit);
  pressButton("."); // decimal
  pressInt(tenthsDigit);
  pressInt(hundrethsDigit);
  pressInt(thousanthsDigit);
  pressButton("Start"); // START! FINALLY
}

void pressInt(int digit) {
  // this is the last straw, I'll just use a switch case
  switch (digit) {
    case 1:
      pressButton("1");
      break;
    case 2:
      pressButton("2");
      break;
    case 3:
      pressButton("3");
      break;
    case 4:
      pressButton("4");
      break;
    case 5:
      pressButton("5");
      break;
    case 6:
      pressButton("6");
      break;
    case 7:
      pressButton("7");
      break;
    case 8:
      pressButton("8");
      break;
    case 9:
      pressButton("9");
      break;
    default:
      pressButton("0");
      break;
  }
}

void processCommand() {
  GCode.ParseLine();
  // Code to process the line of G-Code here…
  //Serial.print("Command Line: ");
  //Serial.println(GCode.line);
  GCode.RemoveCommentSeparators();
  //Serial.print("Comment(s): ");
  //Serial.println(GCode.comments);

  if (GCode.HasWord('G'))
  {
    //    Serial.print("Process G code: ");
    //    Serial.println((int)GCode.GetWordValue('G'));
  }
  if (GCode.HasWord('M'))
  {
    if (GCode.GetWordValue('M') == 77) {
      help();
    }
    //    Serial.print("Process M code: ");
    //    Serial.println((int)GCode.GetWordValue('M'));
  }
  if (GCode.HasWord('X'))
  {
    //Serial.print("Process X code: ");
    //Serial.println((float)GCode.GetWordValue('X'));
    if (millis() < (lastMoveTime + waitBetweenMoves)) {
      delay(waitBetweenMoves); 
      // ensure that it's definitely been long enough
      if (GCode.GetWordValue('X') > 4) {
        goTo(GCode.GetWordValue('X'));
        lastMoveTime = millis();
      }
      
    }
    else { // start typing directly
      if (GCode.GetWordValue('X') > 4) {
        goTo(GCode.GetWordValue('X'));
        lastMoveTime = millis();
      }
    }
  }
}


void buildHashMaps() {
  int k = 0; // this counter basically goes to 24
  for (int i = 0; i < 6; i++) {
    for (int j = 0; j < 4; j++) {
      yPins[k]((buttons[i][j]), pins[i]);
      xPins[k]((buttons[i][j]), pins[j + 6]);
      k++;
    }
  }
}

void pressButton(char* button) {
  // TODO remove this debugging printout
//  Serial.print("*");
//  Serial.println(button);
  int a = xPins.getValueOf(button); // gets physical pin values from array
  int b = yPins.getValueOf(button);
  digitalWrite(LEDpin, HIGH);
  digitalWrite(a, HIGH);
  digitalWrite(b, HIGH);
  delay(holdTime);
  digitalWrite(LEDpin, LOW);
  digitalWrite(a, LOW);
  digitalWrite(b, LOW);
  delay(pauseTime);
}

void changeCalibration(int thousanths) {
  // TODO press some buttons
}


// FIXME UPDATE HELP MESSAGES
/*
   display helpful information
*/
void help() {
  Serial.print(F("Tigerstop serial interface "));
  Serial.println(VERSION);
  Serial.println(F("Commands:"));
  Serial.println(F("G01 X[inches]; - linear move"));
  Serial.println(F("M77; - this help message"));
  Serial.println(F("M99 B[char]; - press specific single button"));
  Serial.println(F("M100 C[thousandths]; - change calibration up/down"));
}


///*
//   prepares the input buffer to receive a new message and
//   tells the serial connected device it is ready for more.
//*/
//void ready() {
//  sofar = 0; // clear input buffer
//  Serial.print(F("> ")); // signal ready to receive input
//}
//
///*
//   Look for character /code/ in the buffer and read the float that immediately follows it.
//   @return the value found.  If nothing is found, /val/ is returned.
//   @input code the character to look for.
//   @input val the return value if /code/ is not found.
// */
//float parseNumber(char code, float val) {
//  char *ptr = buffer; // start at the beginning of buffer
//  while ((long)ptr > 1 && (*ptr) && (long)ptr < (long)buffer + sofar) { // walk to the end
//    if (*ptr == code) { // if you find code on your walk,
//      return atof(ptr + 1); // convert the digits that follow into a float and return it
//    }
//    ptr = strchr(ptr, ' ') + 1; // take a step from here to the letter after the next space
//  }
//  return val;  // end reached, nothing found, return default val.
//}
//
///*
//   Read the input buffer and find any recognized commands. One G or M command per line.
//*/
//void processCommand() {
//  // look for commands that start with 'G'
//  int cmd = parsenumber('G', -1);
//  switch (cmd) {
//    case 1: // move it
//      move(parsenumber('X', 125.000)); break; // 125 because it's better than trying to move to 0
//    case 4: pause(parsenumber('P', 0) * 1000); break; // wait a while
//    default: break;
//  }
//  // look for commands that start with 'M'
//  cmd = parsenumber('M', -1);
//  switch (cmd) {
//    case 77: help(); break;
//    case 114: where(); break; // prints px, py, fr, and mode.
//    default: break;
//  }
//
//  // if the string has no G or M commands it will get here and the Arduino will silently ignore it
//}
//
//
///*
//   delay for the appropriate number of microseconds
//   @input ms how many milliseconds to wait
//*/
//void pause(long ms) {
//  delay(ms / 1000);
//  delayMicroseconds(ms % 1000); // delayMicroseconds doesn't work for values > ~16k.
//}
//
///*
//   print the current position
//*/
//void where() {
//  output("X", px);
//}
//
