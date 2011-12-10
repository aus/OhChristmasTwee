char serIn;
String cmd;

// PWM
int red1Pin   = 3;
int green1Pin = 5;
int blue1Pin  = 6;

// PWM
int red2Pin   = 9;
int green2Pin = 10;
int blue2Pin  = 11;

// Analog
int red3Pin   = 14;
int green3Pin = 15;
int blue3Pin  = 16;

// Reverse the LOW / HIGH if your to match the correct anode / cathode of your RGB LED
const boolean ON = LOW;
const boolean OFF = HIGH;


void setup() {
  pinMode(red1Pin, OUTPUT);
  pinMode(green1Pin, OUTPUT);
  pinMode(blue1Pin, OUTPUT);
  
  pinMode(red2Pin, OUTPUT);
  pinMode(green2Pin, OUTPUT);
  pinMode(blue2Pin, OUTPUT);
  
  pinMode(red3Pin, OUTPUT);
  pinMode(green3Pin, OUTPUT);
  pinMode(blue3Pin, OUTPUT);

  all_off();
  
  Serial.begin(9600);
  Serial.println(">> Serial initialized.");
 
}

void loop () {
  if(Serial.available()) {    
     while (Serial.available()>0){
        serIn = Serial.read();       
        cmd += serIn;
     }
     
     //Debug
     Serial.println(">> Data received!");
     Serial.println(">> Issuing command: " + cmd);
     
     if (cmd.compareTo("red") == 0) { 
        LED12(255,0,0);
        LED3(ON,OFF,OFF);
     }else if (cmd.compareTo("green") == 0) {
        LED12(0,255,0);
        LED3(OFF,ON,OFF);
     } else if (cmd.compareTo("blue") == 0) {
        LED12(0,0,255);
        LED3(OFF,OFF,ON);
     } else if (cmd.compareTo("white") == 0) {
        LED12(255,255,255);
        LED3(ON,ON,ON);
     } else if (cmd.compareTo("black") == 0) {
        LED12(0,0,0);
        LED3(OFF,OFF,OFF);
     } else if (cmd.compareTo("cyan") == 0) {
        LED12(0,255,255);
        LED3(OFF,ON,ON);
     } else if (cmd.compareTo("magenta") == 0) {
        LED12(255,0,255);
        LED3(ON,OFF,ON);
     } else if (cmd.compareTo("yellow") == 0) {
        LED12(255,255,0);
        LED3(ON,ON,OFF);
     } else if (cmd.compareTo("purple") == 0) {
        LED12(128,0,128);
     } else if (cmd.compareTo("warmwhite") == 0) {
        LED12(128,128,128);
     } else if (cmd.compareTo("orange") == 0) {
        LED12(255,100,0);
     } else {
        Serial.println("!! Color not found.");
     }
     
  }
       
       
  delay(500);
  
  //clear cmd buffer
  cmd = "";
}

void LED12(int r, int g, int b) {

  // Comment this section out if you have a reverse anode / cathode RGB
  r = 255 - r;
  g = 255 - g;
  b = 255 - b;
  //
  
  all_off();
  
  analogWrite(red1Pin, r);
  analogWrite(green1Pin, g);
  analogWrite(blue1Pin, b);
  
  analogWrite(red2Pin, r);
  analogWrite(green2Pin, g);
  analogWrite(blue2Pin, b);
}

void LED3(boolean r, boolean g, boolean b) {

  // NON-PWM
  
  digitalWrite(red3Pin, r);
  digitalWrite(green3Pin, g);  
  digitalWrite(blue3Pin, b);  
}

void all_off() {
 // Analog Off: Change to 0 if your cathode / anode is different
 int AN_OFF = 255;
	
 analogWrite(red1Pin, AN_OFF);
 analogWrite(red2Pin, AN_OFF);
 digitalWrite(red3Pin, OFF);
	
 analogWrite(green1Pin, AN_OFF);
 analogWrite(green2Pin, AN_OFF);
 digitalWrite(green3Pin, OFF);

 analogWrite(blue1Pin, AN_OFF);
 analogWrite(blue2Pin, AN_OFF);
 digitalWrite(blue3Pin, OFF);

}
