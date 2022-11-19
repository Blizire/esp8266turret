
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <Servo.h>

// servo 0 - 180 degs
Servo yAxisServo;
Servo xAxisServo;
int xPos = 0;
int yPos = 0;

String header;

WiFiServer server(5050);

void setup()
{  
  Serial.begin(115200);
  Serial.println();

  WiFi.begin("hackme", "zodiacthecat254!!!");

  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println();

  Serial.print("Connected, IP address: ");
  Serial.println(WiFi.localIP());

  yAxisServo.attach(5);
  xAxisServo.attach(4);

  server.begin();
}

int validatePos(int pos)
{
   if ( pos > 180 )
  {
    pos = 180;  
  }

  if ( xPos < 0 )
  {
    pos = 0;  
  }
  return pos;
}

void loop() 
{
  WiFiClient client = server.available();
  if (!client)
  {
    return;
  }

  String req = client.readStringUntil('\r');
  /*
  Serial.println(req);
  Serial.println("servo : " + req.substring(5,6));
  Serial.println("pos   : " + req.substring(7,10));
  Serial.println(atoi(req.substring(7,10).c_str()));
  */
  
  String s = "HTTP/1.1 200 OK\r\n";
  client.print(s);
  
  String servo_select = req.substring(5,6);
  int servo_select_pos = atoi(req.substring(7,10).c_str());
  
  if( servo_select == "x" )
  {
    xPos = servo_select_pos;
  }

  if( servo_select == "y" )
  {
    yPos = servo_select_pos;
  } 
  
  xPos = validatePos(xPos);
  yPos = validatePos(yPos);

  xAxisServo.write(xPos);
  yAxisServo.write(yPos);
}
