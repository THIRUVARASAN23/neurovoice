const int FP1_PIN = A0;
const int FP2_PIN = A1;
const int A0_PIN  = A2;

// 1 = Serial Plotter waveform
// 0 = Labeled Serial Monitor readings
#define PLOT_MODE 1

void setup() {
  Serial.begin(4800);
}

void loop() {
  int fp1 = analogRead(FP1_PIN);
  int fp2 = analogRead(FP2_PIN);
  int a0Value = analogRead(A0_PIN);

#if PLOT_MODE
  // Plotter: labels appear as trace names
  Serial.print("FP1:");
  Serial.print(fp1);
  Serial.print("\tFP2:");
  Serial.print(fp2);
  Serial.print("\tA0:");
  Serial.println(a0Value);
#else
  // Monitor: readable labeled values
  Serial.print("FP1: ");
  Serial.print(fp1);
  Serial.print(" | FP2: ");
  Serial.print(fp2);
  Serial.print(" | A0: ");
  Serial.println(a0Value);
#endif

  delay(4);
}