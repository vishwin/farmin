unsigned long elapsed;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(2, INPUT);
  //pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  //digitalWrite(LED_BUILTIN, !digitalRead(2));
  elapsed=millis();
  unsigned long revs=0;
  boolean stuck=true;
  while (millis()-elapsed<2000) {
    boolean ping=!digitalRead(2);
    if (ping && stuck) {
      continue;
    }
    else if (!ping) {
      stuck=false;
      continue;
    }
    revs++;
    stuck=true;
  }
  Serial.print(revs);
}
