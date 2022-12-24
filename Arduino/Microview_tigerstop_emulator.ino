#include <GCodeParser.h>
#include <MicroView.h>

MicroViewWidget *slider;
GCodeParser GCode = GCodeParser();

#define MAX_BUF (64) // What is the longest message Arduino can store?

float pos = 0.0; // position variable in inches

void setup() {
  Serial.begin(9600);
  uView.begin();
  uView.clear(ALL);
  uView.display();
  delay(700);
  uView.clear(PAGE);
  uView.display();
  slider = new MicroViewSlider(0, 0, 0, 125);
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

void processCommand() {
  GCode.ParseLine();
  // Code to process the line of G-Code here…
  //Serial.print("Command Line: ");
  //Serial.println(GCode.line);
  GCode.RemoveCommentSeparators();
  //Serial.print("Comment(s): ");
  //Serial.println(GCode.comments);

  if (GCode.HasWord('X'))
  {
    //Serial.print("Process X code: ");
    //Serial.println((float)GCode.GetWordValue('X'));
    pos = GCode.GetWordValue('X');
    slider->setValue(pos);
    uView.setCursor(0, 20);
    uView.print(pos);
    uView.rectFill(0,30,64,17,WHITE,NORM);
    uView.display();
    delay(500);
    uView.rectFill(0,30,64,17,BLACK,NORM);
    uView.display();
  }
}
